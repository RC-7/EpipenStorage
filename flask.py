import math
from temperatureModel import tempModel
import pandas
import numpy as np
import matplotlib.pyplot as plt

from peltier import peltier


class flask():
    def __init__(self, modelNumber, thr, delta, power):
        self.tempInner = 8  # Set initial temperature to middle of range we want
        self.radius = 2/100
        self.wallThickness = 0.1
        self.length = 16/100  # has a margin, need 14.8 only
        self.areaOuter = 2*math.pi*self.radius*self.length + \
            2*math.pi*self.radius**2  # has top and bottom
        self.areainner = 2*math.pi*self.radius*self.length+2 * \
            math.pi*self.radius**2
        self.volumeInner = math.pi*self.radius**2*self.length
        self.model = tempModel(modelNumber)
        self.density = 1.1839
        self.specificHeat = 1004
        self.k = {0: 24.36,  # Assumes this is temp range inside will be opperating at
                  5: 24.74,
                  10: 25.12,
                  15: 25.50,
                  20: 25.87,
                  25: 26.24,
                  30: 26.62,
                  35: 26.82,
                  40: 27.35,
                  45: 27.5,
                  50: 28.08}
        self.peltierTime = 0
        self.maxPeltPower = 0.2
        self.secondsOn = []

        self.peltierPower = power

        self.innerR = 1.8/100

        self.peltier = peltier()

        self.outfile = "Model"+str(modelNumber)+".csv"

        self.threshold = thr
        self.delta = delta

        self.U = (0.001*self.k[int(self.tempInner/5)*5]*10**(-3)) / \
            self.radius  # Made 1-100th

    def updateOverallCoefficient(self):

        self.U = (0.001*self.k[int(self.tempInner/5)*5]*10**(-3))/self.radius

    def updateTemp(self, ambient):
        self.updateOverallCoefficient()

        self.tempInner = self.model.newTemp(
            [self.tempInner, ambient, self.U, self.areainner, (self.volumeInner*self.density), 1])

        if(self.tempInner > self.threshold):

            self.peltier.on = True

        elif(self.tempInner < 3):
            self.peltier.on = True

        else:

            self.peltier.on = False

        # Updates the temperature using the peltier
        self.tempInner = self.peltierEffect(ambient, self.tempInner)

        with open("TempSim/"+self.outfile, 'a') as f:
            f.write(str(self.tempInner)+","+str(ambient)+"\n")

    # Changes the internal temperature based on the peltier for the period it is off and on
    def peltierEffect(self, ambient, internal):
        secondsInHourOn = 0.1
        newtemp = 0
        temp = 0
        cooling = False
        heating = False

        rAir = (math.log(self.innerR/(self.innerR-0.01))) / \
            (2*math.pi*self.k[int(internal/5)*5]*10**(-3)*0.16)

        self.peltier.updateConductivity(ambient, internal)

        totalR = self.peltier.rn+self.peltier.rp+rAir*2

        newtemp = 0

        Q = (abs(ambient-internal))/totalR

        dT = Q*rAir

        if(ambient > internal):
            newtemp = internal+dT
        else:
            newtemp = internal-dT

        if((newtemp < (self.threshold))and(newtemp > 3)):

            return newtemp
        else:
            temp = newtemp
            if(temp > (self.threshold)):
                cooling = True
            if(temp < 3):
                heating = True

            while (cooling):

                newtemp = temp

                Q = self.peltierPower*(secondsInHourOn)

                dT = Q/(self.specificHeat*(self.volumeInner*self.density))

                newtemp = newtemp-dT

                if (newtemp < (self.threshold-self.delta)):

                    self.peltierTime = self.peltierTime+secondsInHourOn
                    self.secondsOn.append(secondsInHourOn)

                    if(self.peltierPower > self.maxPeltPower):
                        self.maxPeltPower = self.peltierPower

                    self.peltierPower = 0.2

                    return newtemp

                secondsInHourOn = secondsInHourOn+0.1

            while (heating):

                newtemp = temp

                Q = self.peltierPower*(secondsInHourOn)

                dT = Q/(self.specificHeat*(self.volumeInner*self.density))

                newtemp = newtemp+dT

                if (newtemp > 3):

                    self.peltierTime = self.peltierTime+secondsInHourOn
                    self.secondsOn.append(secondsInHourOn)

                    if(self.peltierPower > self.maxPeltPower):
                        self.maxPeltPower = self.peltierPower

                    self.peltierPower = 0.2

                    return newtemp

                secondsInHourOn = secondsInHourOn+0.1

    def visualisedata(self):

        dataFile = pandas.read_csv(
            "TempSim/"+self.outfile, names=["Internal", "Ambient"])
        df = pandas.DataFrame(dataFile)

        fig, axes = plt.subplots(nrows=2, ncols=1)
        axes[0].axhline(y=3, color='r', linestyle='-')
        axes[0].axhline(y=15, color='r', linestyle='-')
        line = df.plot(ax=axes[0], kind='line', y='Internal')
        line = df.plot(ax=axes[1], kind='line', y='Ambient')

        for ax in axes.flat:
            ax.set(xlabel='x-label', ylabel='y-label')

        plt.show()

    def visualiseTempDiff(self):

        diff = []
        with open("TempSim/"+self.outfile, 'r') as f:
            for line in f:
                temps = line.split(",")
                if((float(temps[0]) > 15)):
                    diff.append((float(temps[0])-15))

                elif(float(temps[0]) < 3):
                    diff.append((3-float(temps[0])))
                else:
                    diff.append(0)

        plt.plot(diff)
        plt.show()

    # Visualise power needed for a peltier to heat the flask in the next minute
    def visualisePeltierPowerNeeded(self, time):

        P = []
        totalP = 0
        with open("TempSim/"+self.outfile, 'r') as f:
            for line in f:
                temps = line.split(",")
                if((float(temps[0]) > 15)):
                    Q = self.specificHeat * \
                        (self.volumeInner*self.density)*(float(temps[0])-15)
                    P.append(Q/(time))
                    totalP = totalP+Q/(time)

                elif(float(temps[0]) < 3):
                    Q = self.specificHeat * \
                        (self.volumeInner*self.density)*(3-float(temps[0]))
                    P.append(Q/(time))
                    totalP = totalP+Q/(time)
                else:
                    P.append(0)

        # plt.plot(P)
        # plt.show()

        np.savetxt("PowerUsage/"+self.outfile, P, fmt="%s")

        with open("PowerUsage/Summary", "a") as f:
            f.write("Model "+self.outfile[5]+","+str(totalP)+"\n")

        with open("PowerUsage/MaxP", "a") as f:
            f.write("Model "+self.outfile[5]+","+str(max(P))+"\n")

    def recordPeltierTime(self):
        with open("PowerUsage/finalDelta", "a") as f:

            f.write("Model "+self.outfile[5]+","+str((self.threshold))+","+str(
                self.delta)+","+str(self.maxPeltPower)+","+str((self.peltierTime)/(60**2))+"\n")
