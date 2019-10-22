

class peltier():
    def __init__(self):

        self.kn = 0
        self.kp = 0
        self.rn = 0
        self.rp = 0

        self.on = False

    def updateConductivity(self, ambient, internal):

        self.kn = 0.0000334545*ambient**2-0.023350303*ambient+5.606333
        self.kp = 0.0000361558*internal**2-0.026351342*internal+6.22162


        self.rn = (3*10**-3)/((self.kn*(6*4*10**-6))*10**0)
        self.rp = (3*10**-3)/((self.kp*(6*4*10**-6))*10**0)

