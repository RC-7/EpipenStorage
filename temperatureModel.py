
class tempModel():
    def __init__(self, modelNumber):
        self.model=modelNumber
        # self.models=[""]              #Add list of model names assigned

        self.modelMethod = {1:self.paperModel,2:self.ownModel,3:self.simplifiedPaper}



    def paperModel(self,temps):
        pass
    def ownModel(self,temps):
        pass
    def simplifiedPaper(self,temps):
        pass



    def newTemp(self,temps):
        return self.modelMethod[self.model](temps)          #Inner then ambient
        
    



