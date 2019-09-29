import math
class tempModel():
    def __init__(self, modelNumber):
        self.model=modelNumber
        self.timeInterval=60
        # self.models=[""]              #Add list of model names assigned

        self.modelMethod = {1:self.paperModel,2:self.ownModel,3:self.simplifiedPaper}



    def paperModel(self,temps):
        pass
    def ownModel(self,temps):
        pass
    def simplifiedPaper(self,temps):
        newTemp=(temps[0]-temps[1])*math.exp(((-temps[2]*temps[3]/(100**3))/(temps[4]*temps[5]))*self.timeInterval)+temps[1]
        print (newTemp)
        return newTemp



    def newTemp(self,temps):
        return self.modelMethod[self.model](temps)          #Inner then ambient
        
    



