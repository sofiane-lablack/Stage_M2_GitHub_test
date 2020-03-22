''' This class allows to treat about the leptonic W decay in the semi-leptonic channel'''


from event.mass import compute_mass

class LeptonicDecay(object):
    '''Compute the W leptonic mass from the leptonic decay'''

    def __init__(self, lepton = 0, misenergy = 0):
        self.lepton = lepton
        self.misenergy = misenergy

        self.true_mass = 0
        self.mass = 0
        self.masses_difference = 0

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    # Setter
    def set_lepton(self, lepton):
        '''set only the lepton'''
        self.lepton = lepton

    def set_misenergy(self, missen):
        '''set only the missing energy'''
        self.misenergy = missen

    def set_decay(self, lepton, missen):
        '''set both the lepton and the missing energy at the same time'''
        self.lepton = lepton
        self.misenergy = missen

    def set_true_mass(self, true_mass):
        '''Set the mass of the simulated W boson (true)'''
        self.true_mass = true_mass

    # Compute method
    def compute(self):
        self.mass = compute_mass(self.lepton, self.misenergy)
        self.masses_difference = self.mass - self.true_mass

    # Getter
    def get_mass(self):
        '''Return the W mass'''
        return self.mass

    def get_masses_difference(self):
        '''Return the difference between computed and simulated mass'''
        return self.masses_difference
