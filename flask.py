import math
from temperatureModel import tempModel
import pandas
import numpy as np
import matplotlib.pyplot as plt

from peltier import peltier

class flask():
    def __init__(self,modelNumber):
        self.tempInner=8            #Set initial temperature to middle of range we want
        self.radius=2/100              #initial estimate, 1.2 for eppi pen, rest for peltier and other wall
        self.wallThickness=0.1
        self.length=16/100              #has a margin, need 14.8 only
        self.areaOuter=2*math.pi*self.radius*self.length+2*math.pi*self.radius**2            #has top and bottom
        self.areainner=2*math.pi*self.radius*self.length+2*math.pi*self.radius**2            #change to be inner area and below
        self.volumeInner=math.pi*self.radius**2*self.length
        self.model=tempModel(modelNumber)
        self.density=1.1839                     #Make depd on temperature, units kg/m^3
        self.specificHeat=1005                 #Make depd on temperature,
        self.k={0:24.36,            #Assumes this is temp range inside will be opperating at
        5:24.74,
        10:25.12,
        15:25.50,
        20:25.87,
        25:26.24,
        30:26.62,
        35:26.82,
        40:27.35,
        45:27.5,
        50:28.08}

        self.innerR=1.8/100

        self.peltier=peltier()
        # self.U=(0.01*self.k[int(self.tempInner/5)*5])/self.radius  
        self.outfile="Model"+str(modelNumber)+".txt"



        self.U=(0.001*self.k[int(self.tempInner/5)*5])/self.radius              #Made 1-100th


    def updateOverallCoefficient(self):
        
        self.U=(0.001*self.k[int(self.tempInner/5)*5]*10**(-3))/self.radius


    def updateTemp(self,ambient):              
        self.updateOverallCoefficient()
        
        self.tempInner=self.model.newTemp([self.tempInner,ambient, self.U,self.areainner,(self.volumeInner*self.density),self.specificHeat ])
        
        if(self.tempInner>13):              #Chose this more intelligently
        #     # print(self.tempInner)
            self.tempInner=self.peltierEffect(ambient,self.tempInner)
            # self.tempInner=self.tempInner-0.068
            # print("-------")
            # print(self.tempInner)

            # self.tempInner=self.tempInner-4

        with open("TempSim/"+self.outfile,'a') as f:                               #should maybe write in chunks? If slow do that with threading
            f.write(str(self.tempInner)+","+str(ambient)+"\n")      #Fix! See below


    def peltierEffect(self,ambient,internal):
        
        seondsInHourOn=1
        newtemp=0

        rAir=(math.log(self.innerR/(self.innerR-0.01)))/(2*math.pi*self.k[int(internal/5)*5]*10**(-3)*0.16)

        # print(rAir)

              #Fox this, will conduct for the rest of that hour if not on! 

        self.peltier.updateConductivity(ambient,internal)

        

        totalR=self.peltier.rn+self.peltier.rp+rAir

        # print(totalR)

        newtemp=0

        # Q=(abs(ambient-internal))/totalR

        # # print(Q)÷
        # # print(Q)
        # dT=Q*rAir

        # # if(not self.peltier.on):  
            
        # if(ambient>internal):
        #     newtemp=internal+dT
        # else:
        #     newtemp=internal-dT

            # return newtemp

        # else:
            
        if(self.peltier.on): 
            # print("here")
            Q=0.2*(seondsInHourOn)
            # dT=Q/(self.density*self.volumeInner*self.specificHeat)

            dT=Q/(self.specificHeat*(self.volumeInner*self.density))
            # print(dT)

            # dT=Q*rAir
            newtemp=newtemp-dT

        return newtemp
        




    def visualisedata(self):

        dataFile = pandas.read_csv("TempSim/"+self.outfile, names=["Internal","Ambient"])
        df = pandas.DataFrame(dataFile)

        fig, axes = plt.subplots(nrows=2, ncols=1)
        axes[0].axhline(y=3, color='r', linestyle='-')
        axes[0].axhline(y=15, color='r', linestyle='-')
        line=df.plot(ax=axes[0],kind='line',y='Internal')
        line=df.plot(ax=axes[1],kind='line',y='Ambient')
        
        plt.show()

    def visualiseTempDiff(self):

        diff=[]
        with open("TempSim/"+self.outfile, 'r') as f:
            for line in f:
                temps=line.split(",")
                if((float(temps[0])>15)):
                    diff.append((float(temps[0])-15))
                    
                elif(float(temps[0])<3):
                    diff.append((3-float(temps[0])))
                else:
                    diff.append(0)

        plt.plot(diff)
        plt.show()


    def visualisePeltierPowerNeeded(self,time):         #Visualise power needed for a peltier to heat the flask in the next minute

        P=[]
        totalP=0
        with open("TempSim/"+self.outfile, 'r') as f:
            for line in f:
                temps=line.split(",")
                if((float(temps[0])>15)):
                    Q=self.specificHeat*(self.volumeInner*self.density)*(float(temps[0])-15)
                    P.append(Q/(time))
                    totalP=totalP+Q/(time)
                    
                elif(float(temps[0])<3):
                    Q=self.specificHeat*(self.volumeInner*self.density)*(3-float(temps[0]))
                    P.append(Q/(time))
                    totalP=totalP+Q/(time)
                else:
                    P.append(0)



        #Uncomment and make figure for later analysis
        # plt.plot(P)
        # plt.show()


        np.savetxt("PowerUsage/"+self.outfile, P, fmt="%s")

        with open("PowerUsage/Summary","a") as f:
            f.write("Model "+self.outfile[5]+","+str(totalP)+"\n")

        with open("PowerUsage/MaxP","a") as f:
            f.write("Model "+self.outfile[5]+","+str(max(P))+"\n")

        




