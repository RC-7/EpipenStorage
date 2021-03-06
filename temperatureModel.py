import math

class tempModel():
    def __init__(self, modelNumber):
        self.model = modelNumber
        self.timeInterval = 60*60

        self.modelMethod = {1: self.paperModel, 2: self.fourierModel,
                            3: self.simplifiedPaper, 4: self.resistorAnalogue}

        self.convectionCoeff = 10
        self.density = 1.29
        self.specificHeat = 10
        self.y = 0.15
        self.lambdaVals = self.initLambda()
        self.k = {0: 24.36,  # Assumes this is temp range inside will be opperating at to be [0,50]
                  5: 24.74,
                  10: 25.12,
                  15: 25.50,
                  20: 25.87,
                  25: 26.24,
                  30: 26.62,
                  35: 26.82,
                  40: 27.35,
                  45: 27.5,
                  50: 28.08}

        self.outerR = 2/100
        self.innerR = 1.8/100
        self.stainlessK = 14.4

        self.rSteelOuter = (
            math.log(self.outerR/(self.outerR-0.01)))/(2*math.pi*self.stainlessK*0.16)
        self.rSteelInner = (
            math.log(self.innerR/(self.innerR-0.01)))/(2*math.pi*self.stainlessK*0.16)
        self.rAir = (math.log(self.innerR/(self.innerR-0.01))) / \
            (2*math.pi*25*10**-3*0.16)
        self.rVac = (math.log(self.innerR/(self.innerR-0.01))) / \
            (2*math.pi*25*10**-5*0.16)  # Show how this changes things!!

        self.totalR = self.rSteelInner+self.rSteelOuter+self.rAir+self.rVac

        self.outerwall = 12  # Initial conditions of flask
        self.innerWall = 10

    def initLambda(self):
        lambdas = []
        solved = False
        lastLambda = 0
        a = 0.16  # a is length of flask in m

        for i in range(31):
            solved = False
            step = (((2*i-1)*math.pi/(2*a))-((i-1)*math.pi/(a)))/10000
            lastLambda = ((i-1)*math.pi/(a))+step
            while(not solved):
                if(math.tan(lastLambda*a)-self.convectionCoeff/(self.specificHeat*lastLambda) < 0.001):
                    lambdas.append(lastLambda)
                    solved = True
                if(lastLambda > ((2*i-1)*math.pi/(2*a))):

                    break
                lastLambda = lastLambda+step

        return lambdas

    def paperModel(self, temps):
        a = 0.16

        newtemp = temps[1]

        for i in range(31):
            B = (temps[0]-temps[1])*math.sin(a*self.lambdaVals[i])/(self.lambdaVals[i])\
                / ((math.sin(2*self.lambdaVals[i])*a)/(4*self.lambdaVals[i])+(a)/(2))

            exponent = (-1*self.k[int(temps[0]/5)*5]*10**(0)*(self.lambdaVals[i]
                                                              ** 2)*self.timeInterval)/(self.density*self.specificHeat)

            newtemp = newtemp+B * \
                math.cos(self.lambdaVals[i]*self.y)*math.exp(exponent)

        return newtemp

    def fourierConvectionSolution(self, temps, outerR, k, c):

        newTemp = temps[1]+math.exp(-k*self.timeInterval)*(temps[0]-temps[1])

        return newTemp

    def fourierModel(self, temps):

        stainlessK = 14.4  # conduction coeficient Stainless steel
        outerR = 2/100
        innerR = 1.8/100
        initial = temps[0]

        self.specificHeat = 1004

        temps[0] = self.outerwall
        self.outerwall = self.fourierConvectionSolution(
            temps, outerR, stainlessK, 502)  # Temp on inside of outer wall
        temps[1] = self.outerwall
        temps[0] = self.innerWall

        self.innerWall = self.fourierConvectionSolution(temps, outerR, self.k[int(
            temps[0]/5)*5]*10**(-7), self.specificHeat)  # Temp on outisde of inner wall, change back to -7
        temps[1] = self.innerWall
        temps[0] = initial
        innerTemp = self.fourierConvectionSolution(
            temps, innerR-0.002, stainlessK, 502)  # Temp on inside of inner wall
        temps[1] = innerTemp
        newTemp = self.fourierConvectionSolution(temps, innerR-0.002, self.k[int(
            temps[0]/5)*5]*10**(-3), self.specificHeat)  # Air temp

        return newTemp

    def simplifiedPaper(self, temps):
        newTemp = (temps[0]-temps[1])*math.exp(((-temps[2]*temps[3] /
                                                 (100**3))/(temps[4]*temps[5]))*self.timeInterval)+temps[1]
        return newTemp

    def resistorAnalogue(self, temps):

        self.rAir = (math.log(self.innerR/(self.innerR-0.01))) / \
            (2*math.pi*self.k[int(temps[0]/5)*5]*10**(-3)*0.16)

        self.rVac = (math.log(self.innerR/(self.innerR-0.01)))/(2*math.pi*self.k[int(
            temps[0]/5)*5]*10**(-5)*0.16)

        self.rSteelOuter = (
            math.log(self.outerR/(self.outerR-0.01)))/(2*math.pi*self.stainlessK*0.16)
        self.rSteelInner = (
            math.log(self.innerR/(self.innerR-0.01)))/(2*math.pi*self.stainlessK*0.16)

        self.totalR = self.rSteelInner+self.rSteelOuter+self.rAir+self.rVac

        Q = (abs(temps[1]-temps[0]))/self.totalR
        dT = Q*self.rAir

        if(temps[1] > temps[0]):
            newtemp = temps[0]+dT
        else:
            newtemp = temps[0]-dT
        return newtemp

    def newTemp(self, temps):  # Method to call relavent temperature model.

        return self.modelMethod[self.model](temps)
