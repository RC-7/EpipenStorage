
from circuit import circuit
import csv
import matplotlib.pyplot as plt

def main():

    hours = [744, 672, 744, 720, 744, 720, 744, 744, 720, 744, 720, 744]
    model=0
    index=0
    res={}
    res["Model 1"]=[]
    res["Model 2"]=[]
    res["Model 3"]=[]
    res["Model 4"]=[]

    with open("PowerUsage/monthly.csv", 'r') as p:
        #reads csv into a list of lists
        listOptimal = [list(map(float,rec)) for rec in csv.reader(p, delimiter=',')]


    for my_list in listOptimal:    
        # print(my_list)
        if(my_list[3]==9):
            model+=1
        circ = circuit(my_list[2], (hours[int(my_list[3])% 12]))
        # powerUsage.append(circ.calculateTotalPower())
        res["Model "+str(model)].append(circ.calculateTotalPower())
        index+=1

        # for element in my_list:
        #     print(element)
    # print(res["Model 2"])
    x = ["Oct","Nov","Dec","Jan","Feb","Mar","Apr","May","June","Jul",'Aug']
    plt.plot(x,res["Model 1"])
    plt.plot(res["Model 2"])
    plt.plot(res["Model 3"])
    plt.plot(res["Model 4"])    # plt.xlabel("Time (h)")
    plt.ylabel("Energy used (mAh)")
    plt.legend(["Model 1", "Model 2", "Model 3", "Model 4"])
    plt.savefig('../results/energyOOOOOptomised', transparent=True, bbox_inches=0,dpi=100)
    plt.show()





if __name__ == "__main__":
    main()