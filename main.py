from temperatureModel import tempModel
from flask import flask



def main():
    fl=flask(3)


    with open("temp.csv") as f:
        for temp in f:
            # temperature=float(temp)
            # print(temp)
            fl.updateTemp(float(temp))

    
    fl.visualisedata()
            




if __name__ == "__main__":
    main()