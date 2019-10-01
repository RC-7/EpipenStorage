from temperatureModel import tempModel
from flask import flask



def main():


    for i in range(4):
        fl=flask(i+1)


        with open("temp.csv") as f:
            for temp in f:
                # temperature=float(temp)
                # print(temp)
                fl.updateTemp(float(temp))

        
        # fl.visualisedata()
        # fl.visualiseTempDiff()

        fl.visualisePeltierPowerNeeded(60**2)
            




if __name__ == "__main__":
    main()