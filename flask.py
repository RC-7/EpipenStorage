import math
from temperatureModel import tempModel

class flask():
    def __init__(self,modelNumber):
        self.tempInner=8            #Set initial temperature to middle of range we want
        self.radius=2              #initial estimate, 1.2 for eppi pen, rest for peltier and other wall
        self.wallThickness=0.1
        self.length=16              #has a margin, need 14.8 only
        self.areaOuter=2*math.pi*self.radius*self.length+2*math.pi*self.radius**2            #has top and bottom
        self.areainner=2*math.pi*self.radius*self.length+2*math.pi*self.radius**2            #change to be inner area and below
        self.volumeInner=math.pi*self.radius**2*self.length
        self.model=tempModel(modelNumber)
        self.density=1.1839                     #Make depd on temperature, units kg/m^3
        self.specificHeat=1.005                 #Make depd on temperature,
        self.k={0:24.36,
        5:24.74,
        10:25.12,
        15:25.50,
        20:25.87,
        25:26.24,
        30:26.62,
        40:27.35,
        45:27.5,
        50:28.08}
        self.U=(0.01*self.k[int(self.tempInner/5)*5])/self.radius


    def updateOverallCoefficient(self):
        self.U=(0.01*self.k[int(self.tempInner/5)*5]*10**(-3))/self.radius




    def updateTemp(self,ambient):              
        self.updateOverallCoefficient()
        print((self.volumeInner*self.density)/(100**3))
        self.tempInner=self.model.newTemp([self.tempInner,ambient, self.U,self.areainner,(self.volumeInner*self.density)/(100**3),self.specificHeat ])

       
