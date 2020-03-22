'''Generic class for particles generation : lepton, missing energy, parton'''


class Particle():
    """Lepton object creation"""

    def __init__(self, p4 = 0):
        self.p4 = p4

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


    def set_p4(self, p4):
        self.p4 = p4

    # Getter
    def get_p4(self):
        return self.p4

    def get_E(self):
        return self.p4.E()

    def get_theta(self):
        return self.p4.Theta()

    def get_phi(self):
        return self.p4.Phi()

    def get_boost(self):
        return self.p4.Beta() * self.p4.Gamma()



if __name__ == '__main__':
    pass
