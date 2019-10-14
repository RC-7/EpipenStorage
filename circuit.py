class circuit():
    def __init__(self,peltierUseTime,hoursInMonth):

        self.MCU_off=0.38*10**-3             #All in mA

        self.MCU_on=(76+31)*10**-3           #Double check this

        self.sensorOff=40*10**-3             #Not sure if need a sensor On??

        self.sensorOn=20

        self.peltTIme=peltierUseTime
        
        self.totalTime=hoursInMonth

        self.ePaperWrite=8

        self.ePaperWriteStandby=5*10**-3

        self.ePaperWriteTime=0.5/(60**2)

        self.batteryTest=4.25           #Need this constantly on?? If can have it just do it!!

        self.peltierOn=200*2

        self.peltierOff=74*10**-6

        self.timeWriteSD=1*10**-3/(60**2)       #Micro second

        self.startupMCU=5*10**-3/(60**2)





    def calculateTotalPower(self):
        
        totalP=0

        totalP=self.peltierOn*self.peltTIme

        totalP=totalP+self.peltierOff*(self.totalTime-self.peltTIme)

        totalP=totalP+(self.totalTime*2-self.totalTime*2*self.startupMCU)*self.MCU_on*self.timeWriteSD             #Negating time to read ADC

        totalP=totalP+(self.totalTime*2-self.totalTime*2*self.startupMCU)*self.MCU_off

        totalP=totalP+self.sensorOff*(self.totalTime-self.peltTIme)*2       #Two sensors used

        totalP=totalP+self.sensorOn*(self.peltTIme)*2

        totalP=totalP+self.ePaperWrite*self.totalTime*self.ePaperWriteTime           #update every hour, ask if okay, half

        totalP=totalP+self.batteryTest*self.totalTime

        return totalP