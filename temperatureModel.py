import math
class tempModel():
    def __init__(self, modelNumber):
        self.model=modelNumber
        self.timeInterval=60
        # self.models=[""]              #Add list of model names assigned

        self.modelMethod = {1:self.paperModel,2:self.ownModel,3:self.simplifiedPaper}

        
        self.convectionCoeff=10
        self.specificHeat=1.005  
        self.lambdaVals = self.initLambda()
                   #Make depd on temperature,




    # [self.tempInner,ambient, self.U,self.areainner,(self.volumeInner*self.density),self.specificHeat ]

    def initLambda(self):
        lambdas=[]
        solved=False
        lastLambda=0
        a=0.16                        #a is length of flask
        
        for i in range(31):         #can do more for both!
            step=(((2*i-1)*math.pi/(2*a))-((i-1)*math.pi/(a)))/100                  
            lastLambda=((i-1)*math.pi/(a))+step
            while(not solved):
                if(math.tan(lastLambda*a)-self.convectionCoeff/(self.specificHeat*lastLambda)<0.01):
                    lambdas.append(lastLambda)
                if(lastLambda>((2*i-1)*math.pi/(2*a))):
                    
                    break
                lastLambda=lastLambda+step
        
        return lambdas






    def paperModel(self,temps):
        pass


        # for i in range(31):





    
    def ownModel(self,temps):
        pass



    def simplifiedPaper(self,temps):
        newTemp=(temps[0]-temps[1])*math.exp(((-temps[2]*temps[3]/(100**3))/(temps[4]*temps[5]))*self.timeInterval)+temps[1]
        print (newTemp)
        return newTemp



    def newTemp(self,temps):
        return self.modelMethod[self.model](temps)          #Inner then ambient
        
    



