from temperatureModel import tempModel
from flask import flask


def main():

    value = 0

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

    models = [1,2,4]

    kVals=[15]

    for i in models:
        for delta in deltas:
            # for k in range(13, 16):
            for k in kVals:
                

                # Timestep model runs for as input too maybe?
                fl = flask(i, k, delta, 0.2)

                with open("test.txt") as f:
                    for temp in f:
                        # temperature=float(temp)
                        # print(temp)
                        fl.updateTemp(float(temp))

                fl.visualisedata()
                # fl.recordPeltierTime()
                # fl.visualiseTempDiff()

                    # fl.visualisePeltierPowerNeeded(60**2)     #Loop times here for post analysis, maybe also do a calc for time given P


if __name__ == "__main__":
    main()
