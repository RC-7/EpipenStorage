import csv
import matplotlib.pyplot as plt

def analysePeltier(modelResults,result):

    model="Model 1"
    


    # with open("tempTest.csv",'r') as f:
    with open("PowerUsage/finalThresh.csv",'r') as f:
        # next(f)
        for line in f:
            res=line.strip().split(",")

            if(float(res[2]) !=-1):
                if (model==res[0]):
                    # mA=float(res[4])*float(res[3])*(10**3)
                    # mA=float(res[4])
                    # if(mA<modelResults[res[0]]["mAh"]):
                        # modelResults[res[0]]["mAh"]=mA
                    result[model].append(float(res[4]))
                    modelResults[res[0]]["Thresh"]=float(res[1])
                    modelResults[res[0]]["Delta"]=float(res[2])
                    modelResults[res[0]]["Power"]=float(res[3])
                    # modelResults[res[0]]["Time"]=float(res[4])/(float(res[3])*(10**3))
                    modelResults[res[0]]["Time"]=float(res[4])
                        # modelResults[res[0]]["timeThresh"]=float(res[5])
                        
                else:
                    # mA=float(res[4])*float(res[3])*(10**3)
                    # mA=float(res[4])
                    model=res[0]
                    result[model].append(float(res[4]))
                    # modelResults[res[0]]["mAh"]=mA
                    # modelResults[res[0]]["mAh"]=mA
                    modelResults[res[0]]["Thresh"]=float(res[1])
                    modelResults[res[0]]["Delta"]=float(res[2])
                    modelResults[res[0]]["Power"]=float(res[3])
                    # modelResults[res[0]]["Time"]=float(res[4])/(float(res[3])*(10**3))
                    modelResults[res[0]]["Time"]=float(res[4])
                    # modelResults[res[0]]["timeThresh"]=float(res[5])



def saveResults(modelResults):
    
    w = csv.writer(open("PowerUsage/SummaryPeltier.csv", "a"))
    for key, val in modelResults.items():
        w.writerow([key, val])


            




def main():
    # modelResults = {'Model 1' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0,'mAh':float('inf'),'timeThresh':0},
    #             'Model 2' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0,'mAh':float('inf'),'timeThresh':0},
    #             'Model 3' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0,'mAh':float('inf'),'timeThresh':0},
    #             'Model 4' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0,'mAh':float('inf'),'timeThresh':0}}

    modelResults = {'Model 1' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0},
                'Model 2' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0},
                'Model 3' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0},
                'Model 4' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0}}


    res={}
    res["Model 1"]=[]
    res["Model 2"]=[]
    res["Model 3"]=[]
    res["Model 4"]=[]
    
    analysePeltier(modelResults,res)

    kVals = []
    
    thresh=10

    while(thresh<15.5):
        kVals.append(thresh)
        thresh+=0.5

    print(kVals)

    plt.plot(kVals,res["Model 1"])
    plt.plot(kVals,res["Model 2"])
    plt.plot(kVals,res["Model 3"])
    plt.plot(kVals,res["Model 4"])
    plt.xlabel("Upper threshold ($^\circ$C)")
    plt.ylabel("Time peltier is in operation (h)")
    plt.legend(["Model 1", "Model 2", "Model 3", "Model 4"])
    plt.savefig('../results/thresh', transparent=True, bbox_inches=0,dpi=100)
    # plt.show()

    # saveResults(modelResults)


if __name__ == "__main__":
    main()