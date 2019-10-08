from temperatureModel import tempModel
from flask import flask


def main():

    value = 0

    deltas = []
    while(value < 3):
        deltas.append(value)
        value = value+0.2

    models = [1, 2, 3, 4]
    power = [0.2, 0.3, 0.4, 0.5]

    for i in models:
        for delta in deltas:
            for k in range(10, 16):
                for p in power:

                    # Timestep model runs for as input too maybe?
                    fl = flask(i, k, delta, p)

                    with open("temp.csv") as f:
                        for temp in f:
                            # temperature=float(temp)
                            # print(temp)
                            fl.updateTemp(float(temp))

                    # fl.visualisedata()
                    fl.recordPeltierTime()
                    # fl.visualiseTempDiff()

                    # fl.visualisePeltierPowerNeeded(60**2)


if __name__ == "__main__":
    main()
