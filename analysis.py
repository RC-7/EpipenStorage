import csv

def analysePeltier(modelResults):

    model="Model 1"
    


    with open("tempTest.csv",'r') as f:
        next(f)
        for line in f:
            res=line.strip().split(",")

            if(float(res[2]) !=0):
                if (model==res[0]):
                    mA=float(res[4])*float(res[3])*(10**3)
                    if(mA<modelResults[res[0]]["mAh"]):
                        modelResults[res[0]]["mAh"]=mA
                        modelResults[res[0]]["Thresh"]=float(res[1])
                        modelResults[res[0]]["Delta"]=float(res[2])
                        modelResults[res[0]]["Power"]=float(res[3])
                        modelResults[res[0]]["Time"]=float(res[4])
                        
                else:
                    mA=float(res[4])*float(res[3])*(10**3)
                    model=res[0]
                    modelResults[res[0]]["mAh"]=mA
                    modelResults[res[0]]["mAh"]=mA
                    modelResults[res[0]]["Thresh"]=float(res[1])
                    modelResults[res[0]]["Delta"]=float(res[2])
                    modelResults[res[0]]["Power"]=float(res[3])
                    modelResults[res[0]]["Time"]=float(res[4])



def saveResults(modelResults):
    w = csv.writer(open("PowerUsage/SummaryPeltier.csv", "a"))
    for key, val in modelResults.items():
        w.writerow([key, val])


            




def main():
    modelResults = {'Model 1' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0,'mAh':float('inf')},
                'Model 2' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0,'mAh':float('inf')},
                'Model 3' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0,'mAh':float('inf')},
                'Model 4' : {'Thresh':0, 'Delta':0, 'Power':0,'Time':0,'mAh':float('inf')}}
    analysePeltier(modelResults)

    saveResults(modelResults)


if __name__ == "__main__":
    main()