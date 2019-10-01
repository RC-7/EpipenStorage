import math
class tempModel():
    def __init__(self, modelNumber):
        self.model=modelNumber
        self.timeInterval=60*60
        # self.models=[""]              #Add list of model names assigned

        self.modelMethod = {1:self.paperModel,2:self.ownModel,3:self.simplifiedPaper}

        
        self.convectionCoeff=10
        self.density=1.1839                     #Make depd on temperature, units kg/m^3
        self.specificHeat=10
        self.y=0.15  
        self.lambdaVals = self.initLambda()
        self.k={0:24.36,            #Assumes this is temp range inside will be opperating at
        5:24.74,
        10:25.12,
        15:25.50,
        20:25.87,
        25:26.24,
        30:26.62,
        35:26.82,
        40:27.35,
        45:27.5,
        50:28.08}
                   #Make depd on temperature,


        #calculate so not just assuming these inital conditions also move to flask class

        self.outerwall=8

        self.innerWall=8




    

    def initLambda(self):
        lambdas=[]
        solved=False
        lastLambda=0
        a=0.16                        #a is length of flask
        
        for i in range(31):         #can do more for both!
            solved=False
            step=(((2*i-1)*math.pi/(2*a))-((i-1)*math.pi/(a)))/10000                  
            lastLambda=((i-1)*math.pi/(a))+step
            while(not solved):
                if(math.tan(lastLambda*a)-self.convectionCoeff/(self.specificHeat*lastLambda)<0.001):
                    lambdas.append(lastLambda)
                    solved=True
                if(lastLambda>((2*i-1)*math.pi/(2*a))):
                    # print("nooooooo")
                    break
                lastLambda=lastLambda+step

        return lambdas






    def paperModel(self,temps):
        a=0.16  

        newtemp=temps[1]
        # print(temps[1])

        for i in range(31):
            #beginning assumes uniform distro, can do some stuff and change that if i want
            B = (temps[0]-temps[1])*math.sin(a*self.lambdaVals[i])/(self.lambdaVals[i])\
                /((math.sin(2*self.lambdaVals[i])*a)/(4*self.lambdaVals[i])+(a)/(2))     


            exponent=(-1*self.k[int(temps[0]/5)*5]*10**(0)*(self.lambdaVals[i]**2)*self.timeInterval)/(self.density*self.specificHeat)
           
        # print(exponent)

            newtemp=newtemp+B*math.cos(self.lambdaVals[i]*self.y)*math.exp(exponent)

        # print(newtemp)

        return newtemp

    # [self.tempInner,ambient, self.U,self.areainner,(self.volumeInner*self.density),self.specificHeat ]

    def fourierConvectionSolution(self,temps,outerR,k):
        a=(k*2*math.pi*0.16)/(temps[4]*math.log(outerR/(outerR-0.002)))            #uses length of container
        # newTemp=temps[1]*(1-math.exp(-a*self.timeInterval))+math.exp(-a*self.timeInterval)*temps[0]
        newTemp=temps[1]+math.exp(-a*self.timeInterval)*(temps[0]-temps[1])
        return newTemp


    
    def ownModel(self,temps):

        stainlessK=14.4             #conduction coeficient Stainless steel, maybe make temp dependant
        outerR=2/100
        innerR=1.8/100

        initial=temps[0]

        temps[0]=self.outerwall

        self.outerwall=self.fourierConvectionSolution(temps,outerR,stainlessK)  #Temp on inside of outer wall

        temps[1]=self.outerwall

        temps[0]=self.innerWall

        self.innerWall=self.fourierConvectionSolution(temps,outerR,self.k[int(temps[0]/5)*5]*10**(-9))  #Temp on inside of outer wall

        temps[1]=self.innerWall

        temps[0]=initial

        innerTemp=self.fourierConvectionSolution(temps,innerR-0.002,self.k[int(temps[0]/5)*5]*10**(-3))  #Temp on inside of outer wall

        temps[1]=innerTemp

        newTemp=self.fourierConvectionSolution(temps,innerR-0.002,self.k[int(temps[0]/5)*5]*10**(-3))  #Temp on inside of outer wall

        return self.innerWall





    def simplifiedPaper(self,temps):
        newTemp=(temps[0]-temps[1])*math.exp(((-temps[2]*temps[3]/(100**3))/(temps[4]*temps[5]))*self.timeInterval)+temps[1]
        # print (newTemp)
        return newTemp



    def newTemp(self,temps):
        return self.modelMethod[self.model](temps)          #Inner then ambient
        
    



