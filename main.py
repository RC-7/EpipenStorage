from temperatureModel import tempModel
from flask import flask
from circuit import circuit


def main():


    hours=[744,672,744,720,744,720,744,744,720,744,720,744]

    month=9

    value = 0

    powerUsage=[]

    

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
    models=[1]

    kVals=[15]

    for i in models:
        for delta in deltas:
            # for k in range(13, 16):
            for k in kVals:
                

                # Timestep model runs for as input too maybe?
                fl = flask(i, k, delta, 0.2)

                with open("temp.csv") as f:
                    for temp in f:
                        # temperature=float(temp)
                        # print(temp)
                        fl.updateTemp(float(temp))
                        value+=1

                        if (value>hours[month]):
                            circ=circuit(fl.peltierTime/(60**2),hours[month])
                            powerUsage.append(circ.calculateTotalPower())
                            value=0
                            month=(month+1)%12
                            fl.peltierTime=0




                
                print(max(powerUsage))
                powerUsage=[]
                fl.visualisedata()
                # fl.recordPeltierTime()
                # fl.visualiseTempDiff()

                    # fl.visualisePeltierPowerNeeded(60**2)     #Loop times here for post analysis, maybe also do a calc for time given P


if __name__ == "__main__":
    main()
