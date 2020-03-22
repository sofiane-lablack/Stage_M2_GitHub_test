# This class allows to build dijets objects
from math import degrees

from event.mass import compute_mass

class Dijet():

    def __init__(self, jet1, jet2):
        self.name = jet1.get_id() + jet2.get_id()
        self.jet1 = jet1
        self.jet2 = jet2

        self.mass = 0
        self.true_mass = 0
        self.masses_difference = 0
        self.angle = 0

        self.mref = jet1.get_mref()

        self.compute()

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    # Getter
    def get_name(self):
        return self.name

    def get_mref(self):
        return self.mref

    def get_mass(self):
        return self.mass

    def get_masses_difference(self):
        '''Return the difference between computed and simulated mass'''
        return self.masses_difference

    def get_jets(self):
        return self.jet1, self.jet2

    def get_angle(self):
        return self.angle

    # Setter
    def set_true_mass(self, true_mass):
        '''Set the mass of the simulated W boson (true)'''
        self.true_mass = true_mass

    # Compute methods
    def compute(self):
        self.mass = compute_mass(self.jet1, self.jet2)
        self.angle = degrees(self.jet1.get_p4().Angle(self.jet2.get_p4().Vect()))

        if self.true_mass != 0:
            self.masses_difference = self.mass - self.true_mass
