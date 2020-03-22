
class Jet():
    """Jet creation"""

    def __init__(self):
        self.p4 = 0
        self.parton = 0
        self.id = 0
        self.mref = 0

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

    def get_parton(self):
        return self.parton

    def get_id(self):
        return self.id

    def get_mref(self):
        return self.mref

    def set_mref(self, m):
        self.mref = m

    def set_p4(self, p4):
        self.p4 = p4

    def set_id(self, jid):
        self.id = jid

    def set_parton(self, partons):
        a_min = 100
        for parton in partons:
            a = self.get_p4().Angle(parton.get_p4().Vect())

            if a <= a_min:
                a_min = a
                self.parton = parton


if __name__ == '__main__':
    pass
