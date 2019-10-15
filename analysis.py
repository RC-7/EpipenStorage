import csv
import matplotlib.pyplot as plt
import numpy as np

def analysePeltier(modelResults,result):

    model="Model 1"
    


    # with open("tempTest.csv",'r') as f:
    with open("PowerUsage/varPower",'r') as f:
        next(f)
        for line in f:
            res=line.strip().split(",")

            if((float(res[1]) ==15)and (float(res[2]) ==0)):
                if (model==res[0]):
                    # mA=float(res[4])*float(res[3])*(10**3)
                    mA=float(res[4])
                    if(mA<modelResults[res[0]]["mAh"]):
                        modelResults[res[0]]["mAh"]=mA
                        modelResults[res[0]]["Thresh"]=float(res[1])
                        modelResults[res[0]]["Delta"]=float(res[2])
                        modelResults[res[0]]["Power"]=float(res[3])
                        modelResults[res[0]]["Time"]=float(res[4])/(float(res[3])*(10**3))
                        # modelResults[res[0]]["Time"]=float(res[4])
                        modelResults[res[0]]["timeThresh"]=float(res[5])
                    result[model].append(mA)

                        
                else:
                    # mA=float(res[4])*float(res[3])*(10**3)
                    # mA=float(res[4])
                    model=res[0]
                    # result[model].append(float(res[4])/(float(res[3])*(10**3)))
                    result[model].append(float(res[4]))
                    # modelResults[res[0]]["mAh"]=mA
                    # modelResults[res[0]]["mAh"]=mA
                    modelResults[res[0]]["Thresh"]=float(res[1])
                    modelResults[res[0]]["Delta"]=float(res[2])
                    modelResults[res[0]]["Power"]=float(res[3])
                    # modelResults[res[0]]["Time"]=float(res[4])/(float(res[3])*(10**3))
                    modelResults[res[0]]["Time"]=float(res[4])
                    modelResults[res[0]]["timeThresh"]=float(res[5])



def saveResults(modelResults):
    
    w = csv.writer(open("PowerUsage/SummaryPeltier.csv", "a"))
    for key, val in modelResults.items():
        w.writerow([key, val])


            




def main():
    modelResults = {'Model 1' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0,'mAh':float('inf'),'timeThresh':0},
                'Model 2' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0,'mAh':float('inf'),'timeThresh':0},
                'Model 3' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0,'mAh':float('inf'),'timeThresh':0},
                'Model 4' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0,'mAh':float('inf'),'timeThresh':0}}

    # modelResults = {'Model 1' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0},
    #             'Model 2' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0},
    #             'Model 3' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0},
    #             'Model 4' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0}}


    res={}
    res["Model 1"]=[]
    res["Model 2"]=[]
    res["Model 3"]=[]
    res["Model 4"]=[]
    
    analysePeltier(modelResults,res)

    kVals = []
    
    # thresh=10

    # while(thresh<15.5):
    #     kVals.append(thresh)
    #     thresh+=0.5

    # print(kVals)


    # kVals = []
    # value=0
    # while(value < 3):
    #     kVals.append(value)
    #     value = value+0.5

    timeThresh=[]
    
    value=1
    while(value < 10):
        timeThresh.append(value)
        value = value+0.5

    print((res["Model 3"]))


    plt.plot(timeThresh,res["Model 1"])
    # plt.plot(timeThresh,res["Model 2"])
    plt.plot(timeThresh,res["Model 3"])
    plt.plot(timeThresh,res["Model 4"])
    plt.xlabel("Time threshold (s)")
    # plt.xlabel("Temperature difference ($^\circ$C)")
    # plt.ylabel("Time peltier is in operation (h)")
    plt.ylabel("Energy supplied to the peltier (mAh)")
    plt.legend(["Model 1", "Model 3", "Model 4"])
    plt.savefig('../results/timeThresh', transparent=True, bbox_inches=0,dpi=100)
    # plt.show()

    # saveResults(modelResults)


    # noTimeThresh=[722.9444444000001,2221.8055560000003,714.0500000000001,727.9055556000001]
    # timeThreshUsed=[722.9388888888889,2223.3611111111113,714.0472222222222,727.9055555555556]
    # labels=["Model 1","Model 2","Model 3","Model 4"]

    # x = np.arange(len(labels))  # the label locations
    # width = 0.35  # the width of the bars

    # fig, ax = plt.subplots()
    # rects1 = ax.bar(x - width/2, noTimeThresh, width, label='Constant Power')
    # rects2 = ax.bar(x + width/2, timeThreshUsed, width, label='Variable Power')
    # ax.set_ylabel("Energy supplied to the peltier (mAh)")
    # ax.set_title('Scores by group and gender')
    # ax.set_xticks(x)
    # ax.set_xticklabels(labels)
    # ax.legend()


    # fig.tight_layout()
    # plt.savefig('../results/timeThreshComp', transparent=True, bbox_inches=0,dpi=100)

    # plt.show()
    


if __name__ == "__main__":
    main()