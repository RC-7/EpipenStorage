from temperatureModel import tempModel
from flask import flask
from circuit import circuit
import matplotlib.pyplot as plt
import pandas
import csv


def visualiseAllTemp():

    dataFile = pandas.read_csv(
            "../results/stepPeltNotOn.csv", names=["Model 1", "Model 2","Model 3","Model 4"])
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

    with open("PowerUsage/monthly.csv", 'r') as p:
        #reads csv into a list of lists
        my_list = [list(map(float,rec)) for rec in csv.reader(p, delimiter=',')]

    # print(my_list[1][1])
 


    powerUsage = []

    modelUsage = []

    deltas = [0]
    # while(value < 3):
    #     deltas.append(value)
    #     value = value+0.2

    # timeThresh=[]
    # value=1
    # while(value < 10):
    #     timeThresh.append(value)
    #     value = value+0.5

    # models = [1, 2, 3, 4]
    # power = [0.2]

    # models = []
    models = [1, 2, 3, 4]

    kVals = [15]
    pelt=[]

    # kVals = []
    
    thresh=8
    index=0
    # while(thresh<15.5):
    #     kVals.append(thresh)
    #     thresh+=0.5
    # visualiseAllTemp()

    # visualiseMultisim()
        

    for i in models:
        month=9
        # print(9)
        # while(my_list[index][3]!=month):
        #     index+=1
        for delta in deltas:
            # for k in range(13, 16):
            for k in kVals:

                # toWrite="Model "+ str(i)+","

                # Timestep model runs for as input too maybe?
                fl = flask(i,  15,  0, 0.2)

                # print(my_list[index][3])
                # print(month% 12)

                with open("step.txt") as f:
                    for temp in f:
                        # temperature=float(temp)
                        # print(temp)
                        fl.updateTemp(float(temp))
                        value =value+ 1
                        

                        if (value > hours[month% 12]):
                            # print(month% 12)
                            # if (my_list[index][3]==(month% 12)):
                            #     # print("yes")
                            #     # print(i)
                            #     pass
                            # else:
                                
                            #     print("no")
                            #     print(my_list[index][3])
                            #     pass
                            index=index+1

                            # fl.threshold=my_list[index][0]
                            # fl.delta=my_list[index][1]
                            # print((fl.peltierTime)/(60**2))

                            # print(fl.delta)

                            # inner=fl.tempInner
                            # fl = flask(i, my_list[index][0], my_list[index][1], 0.2,30)

                            # print(str(fl.peltierTime/(60**2)))
                            # circ = circuit(
                            #     (fl.peltierTime/(60**2)), hours[month% 12])
                            # powerUsage.append(circ.calculateTotalPower())
                            value = 0
                            month = (month+1)
                            # print(month%12)
                            # print(month)
                            
                            # m="MonthlyOptomisation/yearlyOptimal"
                            # with open(m, "a") as f:
                            #     f.write("Model "+str(i)+","+str(k)+","+str(delta)+","+str((fl.peltierTime)/(60**2))+","+str(((month-1)%12))+"\n")
                            #     f.close()

                            # fl.peltierTime = 0
                    


                            # if((month%12)==2):
                            #     pelt.append(fl.secondsOn)

                        #     fl.secondsOn=[]
                circ = circuit((fl.peltierTime/(60**2)), hours[month% 12])
                powerUsage.append(circ.calculateTotalPower())
                # pelt.append(fl.secondsOn)
                        # index=index+1
                # print("--------")
                modelUsage.append(powerUsage)
                pelt.append(fl.secondsOn)
                # print((powerUsage))
                # print(max(powerUsage))
                powerUsage = []
                # fl.visualisedata()
                # fl.recordPeltierTime()
                # fl.visualiseTempDiff()
    # x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    print(modelUsage)
    res={}
    res["Model 1"]=[]
    res["Model 2"]=[]
    res["Model 3"]=[]
    res["Model 4"]=[]

    # with open("PowerUsage/monthly.csv", 'r') as p:
    #     #reads csv into a list of lists
    #     listOptimal = [list(map(float,rec)) for rec in csv.reader(p, delimiter=',')]

    # model=0
    # for my_list in listOptimal:    
    #     # print(my_list)
    #     if(my_list[3]==9):
    #         model+=1
    #     circ = circuit(my_list[2], (hours[int(my_list[3])% 12]))
    #     # powerUsage.append(circ.calculateTotalPower())
    #     res["Model "+str(model)].append(circ.calculateTotalPower())
    #     index+=1




    # x = ["Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","June","Jul"]

    # mods=["Model 1","Model 2","Model 3","Model 4"]

    # diff=[]
    # print(len(modelUsage[0]))

    # for i in range(4):
    #     monthlyDiff=[]
    #     for j in range(len(modelUsage[0])):
    #         # modelUsage[i][j]
    #         # res[mods[i]][j]

    #         monthlyDiff.append(modelUsage[i][j]-res[mods[i]][j])
    #     diff.append(monthlyDiff)

    # print(modelUsage[0])
    # # for i in range(len(modelUsage[0])):
    # #     plt.plot([pt[i] for pt in modelUsage],label = 'id %s'%i)

    # print(modelUsage[0])
    # print(modelUsage[1])
    # print(modelUsage[2])
    # print(modelUsage[3])



    # plt.plot(x,diff[0])
    # plt.plot(diff[1])
    # plt.plot(diff[2])
    # plt.plot(diff[3])
    # plt.xlabel("Month")
    # plt.ylabel("Energy difference (mAh)")
    # plt.legend(["Model 1", "Model 2", "Model 3", "Model 4"])
    # plt.savefig('../results/energySaved', transparent=True, bbox_inches=0,dpi=100)
    # plt.show()

    # fl.visualisePeltierPowerNeeded(60**2)     #Loop times here for post analysis, maybe also do a calc for time given P


        # print(modelUsage[0])
    # for i in range(len(modelUsage[0])):
    #     plt.plot([pt[i] for pt in modelUsage],label = 'id %s'%i)

    # plt.plot(pelt[0])
    plt.plot(pelt[1])
    # plt.plot(pelt[2])
    # plt.plot(pelt[3])
    plt.xlabel("Time (h)")
    plt.ylabel("Time peltier is on (s)")
    plt.legend(["Model 2", "Model 3", "Model 4"])
    # plt.savefig('../results/PeltWorst', transparent=True, bbox_inches=0,dpi=100)
    plt.show()


if __name__ == "__main__":
    main()
