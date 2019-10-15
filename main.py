from temperatureModel import tempModel
from flask import flask
from circuit import circuit
import matplotlib.pyplot as plt
import pandas


def visualiseAllTemp():

    dataFile = pandas.read_csv(
            "../results/step.csv", names=["Model 1", "Model 2","Model 3","Model 4"])
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


def visualiseMultisim():

    dataFile = pandas.read_csv(
            "../Multisim/BatteryDraw.csv", names=["Battery Voltage","LED Current"])
    df = pandas.DataFrame(dataFile)
    ax=df.plot("Battery Voltage",legend=False)
    # ax.axvline(x=3.55, color='r', linestyle='--')
    ax.set_ylabel("Current draw(A)")
    ax.set_xlabel("Battery Voltage (V)")
    plt.savefig('../results/BatteryDraw', transparent=True, bbox_inches=0,dpi=100)

    

    # plt.savefig('../results/InternalWithPelt', transparent=True, bbox_inches=0,dpi=100)

    plt.show()



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

    models = []
    # models = [1, 2, 3, 4]

    kVals = [15]
    pelt=[]

    # kVals = []
    
    # thresh=10

    # while(thresh<15.5):
    #     kVals.append(thresh)
    #     thresh+=0.5
    # visualiseAllTemp()

    visualiseMultisim()
        

    for i in models:
        month=9
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
                        value =value+ 1

                        if (value > hours[month% 12]):
                            # print(str(fl.peltierTime/(60**2)))
                            circ = circuit(
                                (fl.peltierTime/(60**2)), hours[month% 12])
                            powerUsage.append(circ.calculateTotalPower())
                            value = 0
                            month = (month+1)
                            # print(month)
                            fl.peltierTime = 0

                            if((month%12)==2):
                                pelt.append(fl.secondsOn)

                            fl.secondsOn=[]
                        

                # modelUsage.append(powerUsage)
                # print((powerUsage))
                # print(max(powerUsage))
                powerUsage = []
                # fl.visualisedata()
                # fl.recordPeltierTime()
                # fl.visualiseTempDiff()
    # x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    x = ["Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","June","Jul"]

    # print(modelUsage[0])
    # # for i in range(len(modelUsage[0])):
    # #     plt.plot([pt[i] for pt in modelUsage],label = 'id %s'%i)

    # plt.plot(x,modelUsage[0])
    # plt.plot(modelUsage[1])
    # plt.plot(modelUsage[2])
    # plt.plot(modelUsage[3])
    # plt.xlabel("Month")
    # plt.ylabel("Energy used (mAh)")
    # plt.legend(["Model 1", "Model 2", "Model 3", "Model 4"])
    # plt.savefig('../results/energyFinal', transparent=True, bbox_inches=0,dpi=100)
    # # plt.show()

    # fl.visualisePeltierPowerNeeded(60**2)     #Loop times here for post analysis, maybe also do a calc for time given P


        # print(modelUsage[0])
    # for i in range(len(modelUsage[0])):
    #     plt.plot([pt[i] for pt in modelUsage],label = 'id %s'%i)

    plt.plot(pelt[0])
    plt.plot(pelt[1])
    plt.plot(pelt[2])
    plt.plot(pelt[3])
    plt.xlabel("Time (h)")
    plt.ylabel("Time peltier is on (s)")
    # plt.legend(["Model 1", "Model 2", "Model 3", "Model 4"])
    plt.savefig('../results/PeltWorst', transparent=True, bbox_inches=0,dpi=100)
    # plt.show()


if __name__ == "__main__":
    main()
