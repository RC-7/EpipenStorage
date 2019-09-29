import math
from temperatureModel import tempModel

class flask():
    def __init__(self,modelNumber):
        self.tempInner=8            #Set initial temperature to middle of range we want
        self.radius=2              #initial estimate, 1.2 for eppi pen, rest for peltier and other wall
        self.wallThickness=0.1
        self.length=16              #has a margin, need 14.8 only
        self.areaOuter=2*math.pi*self.radius*self.length+2*math.pi*self.radius**2            #has top and bottom
        self.volumeInner=math.pi*self.radius**2*self.length
        self.model=tempModel(modelNumber)


    def updateTemp(self,ambient):
        self.tempInner=self.model.newTemp([self.tempInner,ambient])

       
