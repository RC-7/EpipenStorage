import math
class tempModel():
    def __init__(self, modelNumber):
        self.model=modelNumber
        self.timeInterval=60
        # self.models=[""]              #Add list of model names assigned

        self.modelMethod = {1:self.paperModel,2:self.ownModel,3:self.simplifiedPaper}

        
        self.convectionCoeff=10
        self.density=1.1839                     #Make depd on temperature, units kg/m^3
        self.specificHeat=1.005
        self.y=0.15  
        self.lambdaVals = self.initLambda()
        self.k={0:24.36,            #Assumes this is temp range inside will be opperating at
        5:24.74,
        10:25.12,
        15:25.50,
        20:25.87,
        25:26.24,
        30:26.62,
        40:27.35,
        45:27.5,
        50:28.08}
                   #Make depd on temperature,




    

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





# [self.tempInner,ambient, self.U,self.areainner,(self.volumeInner*self.density),self.specificHeat ]
    def paperModel(self,temps):

        newtemp=temps
        for i in range(31):

            B = ()/()                   #Fix numerator

            exponent=(self.k[int(temps[0]/5)*5]*10**(-3)*(self.lambdaVals[i]**2)*self.timeInterval)/(self.density*self.specificHeat)

            newtemp=newtemp+B*math.cos(self.lambdaVals[i]*self.y)*math.exp(exponent)





    
    def ownModel(self,temps):
        pass



    def simplifiedPaper(self,temps):
        newTemp=(temps[0]-temps[1])*math.exp(((-temps[2]*temps[3]/(100**3))/(temps[4]*temps[5]))*self.timeInterval)+temps[1]
        print (newTemp)
        return newTemp



    def newTemp(self,temps):
        return self.modelMethod[self.model](temps)          #Inner then ambient
        
    



