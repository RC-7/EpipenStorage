from temperatureModel import tempModel
from flask import flask


def main():

    value = 0

    deltas = []
    while(value < 3):
        deltas.append(value)
        value = value+0.5

    timeThresh=[]
    value=1
    while(value < 10):
        timeThresh.append(value)
        value = value+0.5

    models = [1, 2, 3, 4]
    # power = [0.2]

    # models = [2, 3, 4]

    for i in models:
        for delta in deltas:
            for k in range(13, 16):
                for t in timeThresh:

                    # Timestep model runs for as input too maybe?
                    fl = flask(i, k, delta, 0.2,t)

                    with open("temp.csv") as f:
                        for temp in f:
                            # temperature=float(temp)
                            # print(temp)
                            fl.updateTemp(float(temp))

                    # fl.visualisedata()
                    fl.recordPeltierTime()
                    # fl.visualiseTempDiff()

                    # fl.visualisePeltierPowerNeeded(60**2)     #Loop times here for post analysis, maybe also do a calc for time given P


if __name__ == "__main__":
    main()
