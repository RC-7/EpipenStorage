from temperatureModel import tempModel
from flask import flask
from circuit import circuit
import matplotlib.pyplot as plt


def main():

    hours = [744, 672, 744, 720, 744, 720, 744, 744, 720, 744, 720, 744]

    month = 9

    value = 0

    powerUsage = []

    modelUsage = []

    deltas = [0]
    # while(value < 3):
    #     deltas.append(value)
    #     value = value+0.5

    # timeThresh=[]
    # value=1
    # while(value < 10):
    #     timeThresh.append(value)
    #     value = value+0.5

    # models = [1, 2, 3, 4]
    # power = [0.2]

    # models = [1,2,3,4]
    models = [1, 2, 3, 4]

    kVals = [15]

    for i in models:
        for delta in deltas:
            # for k in range(13, 16):
            for k in kVals:

                # toWrite="Model "+ str(i)+","

                # Timestep model runs for as input too maybe?
                fl = flask(i, k, delta, 0.2)

                with open("temp.csv") as f:
                    for temp in f:
                        # temperature=float(temp)
                        # print(temp)
                        fl.updateTemp(float(temp))
                        value += 1

                        if (value > hours[month]):
                            # print(str(fl.peltierTime/(60**2)))
                            circ = circuit(
                                (fl.peltierTime/(60**2)), hours[month])
                            powerUsage.append(circ.calculateTotalPower())
                            value = 0
                            month = (month+1) % 12
                            fl.peltierTime = 0

                modelUsage.append(powerUsage)
                # print((powerUsage))
                # print(max(powerUsage))
                powerUsage = []
                # fl.visualisedata()
                # fl.recordPeltierTime()
                # fl.visualiseTempDiff()
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # print(modelUsage[0])
    # for i in range(len(modelUsage[0])):
    #     plt.plot([pt[i] for pt in modelUsage],label = 'id %s'%i)

    plt.plot(modelUsage[0])
    plt.plot(modelUsage[1])
    plt.plot(modelUsage[2])
    plt.plot(modelUsage[2])
    plt.legend(["Model 1", "Model 2", "Model 3", "Model 4"])

    plt.show()

    # fl.visualisePeltierPowerNeeded(60**2)     #Loop times here for post analysis, maybe also do a calc for time given P


if __name__ == "__main__":
    main()
