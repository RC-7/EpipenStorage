from temperatureModel import tempModel
from flask import flask
from circuit import circuit
import matplotlib.pyplot as plt
import pandas


def visualiseAllTemp():

    dataFile = pandas.read_csv(
        "../results/step.csv", names=["Model 1", "Model 2", "Model 3", "Model 4"])
    df = pandas.DataFrame(dataFile)

    fig, axes = plt.subplots(nrows=2, ncols=2)
    axes[0][0].axhline(y=3, color='r', linestyle='-')
    axes[0][0].axhline(y=15, color='r', linestyle='-')

    axes[0][1].axhline(y=3, color='r', linestyle='-')
    axes[0][1].axhline(y=15, color='r', linestyle='-')

    axes[1][0].axhline(y=3, color='r', linestyle='-')
    axes[1][0].axhline(y=15, color='r', linestyle='-')

    axes[1][1].axhline(y=3, color='r', linestyle='-')
    axes[1][1].axhline(y=15, color='r', linestyle='-')
    line = df.plot(ax=axes[0][0], kind='line', y='Model 1')
    line = df.plot(ax=axes[0][1], kind='line', y='Model 2')
    line = df.plot(ax=axes[1][0], kind='line', y='Model 3')
    line = df.plot(ax=axes[1][1], kind='line', y='Model 4')

    for ax in axes.flat:
        ax.set(xlabel='Time (h)', ylabel='Internal temperature ($^\circ$C))')

    # plt.savefig('../results/InternalWithPelt', transparent=True, bbox_inches=0,dpi=100)

    plt.show()


def visualiseMultisim():  # Used to plot multisim results

    dataFile = pandas.read_csv(
        "../Multisim/BatteryDraw.csv", names=["Battery Voltage", "LED Current"])
    df = pandas.DataFrame(dataFile)
    ax = df.plot("Battery Voltage", legend=False)
    # ax.axvline(x=3.55, color='r', linestyle='--')
    ax.set_ylabel("Current draw(A)")
    ax.set_xlabel("Battery Voltage (V)")
    plt.savefig('../results/BatteryDraw',
                transparent=True, bbox_inches=0, dpi=100)

    plt.show()


def main():

    hours = [744, 672, 744, 720, 744, 720, 744, 744, 720, 744, 720, 744]

    month = 9

    value = 0

    powerUsage = []

    modelUsage = []

    deltas = [0]
    # Uncomment below to run a simulation using different delta perameters
    # while(value < 3):
    #     deltas.append(value)
    #     value = value+0.5

    # Uncomment below to run a simulation using different time thresholds
    # timeThresh=[]
    # value=1
    # while(value < 10):
    #     timeThresh.append(value)
    #     value = value+0.5

    # power = [0.2]

    models = [1, 2, 3, 4]

    kVals = [15]
    pelt = []

    # Uncomment below to run a simulation using different temperature thresholds
    # thresh=10
    # kVals = []
    # while(thresh<15.5):
    #     kVals.append(thresh)
    #     thresh+=0.5
    # visualiseAllTemp()

    visualiseMultisim()

    for i in models:
        month = 9
        for delta in deltas:
            for k in kVals:

                # Change 0.2 to change the power of the Peltier device used
                fl = flask(i, k, delta, 0.2)

                with open("temp.csv") as f:  # Change to step.csv to view the step response
                    for temp in f:
                        fl.updateTemp(float(temp))
                        value = value + 1

                        if (value > hours[month % 12]):

                            circ = circuit(  # Calculates the monthly energy usage of the device
                                (fl.peltierTime/(60**2)), hours[month % 12])
                            powerUsage.append(circ.calculateTotalPower())
                            value = 0
                            month = (month+1)

                            fl.peltierTime = 0

                            # if((month % 12) == 2):            #Saves the time that the peltier is on during the worst month
                            #     pelt.append(fl.secondsOn)

                            fl.secondsOn = []

                # modelUsage.append(powerUsage)
                powerUsage = []

                # Uncomment below to visualise various aspects of the device, used in finding optimal perameters and viewing the device's functioning
                # Uncomment to stop visualising the flask's internal temperature during the simulation
                fl.visualisedata()
                # fl.recordPeltierTime()
                # fl.visualiseTempDiff()


if __name__ == "__main__":
    main()
