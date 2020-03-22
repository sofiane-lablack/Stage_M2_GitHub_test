from particles.dijets import Dijet


class DijetsPairs(Dijet):
    '''For a given dijets pair, it associates the chi2 and the jet-jet angles'''

    def __init__(self, dijet1, dijet2):
        self.dj1 = dijet1
        self.dj2 = dijet2

        self.chi2 = 0
        self.sum_angle = 0

        self.compute()

    def compute(self):
        self.compute_chi()
        # self.compute_jet_jet_angle_sum()

    def compute_chi(self):
        '''Compute the Chi2 of a giving dijet pair'''

        mref = self.dj1.get_mref()
        m1 = self.dj1.get_mass()
        m2 = self.dj2.get_mass()

        self.chi2 = (m1 - mref)**2 + (m2 - mref)**2
    # def compute_jet_jet_angle_sum(self):
    #     '''Compute the jet-jet angles sum
    #         dj1 = j1 et j2  --> angle1 = angle between j1 and j2
    #         dj2 = j3 et j4  --> angle2 = angle between j3 and j4
    #         jet-jet angles sum = angle1 + angle2'''

    #     angle1 = self.dj1.get_angle()
    #     angle2 = self.dj2.get_angle()

    #     self.sum_angle = angle1 + angle2

    def get_chi2(self):
        '''Access the chi2 of the pairing'''
        return self.chi2

    # def get_jet_jet_angle(self):
    #     '''Access the jet-jet angle sum'''
    #     return self.sum_angle

    def get_dijet1(self):
        return self.dj1

    def get_dijet2(self):
        return self.dj2


    # def is_equal_to(self, pair):

    #     return bool(((self.get_dijet1().get_name() == pair.get_dijet1().get_name()) or\
    #         (self.get_dijet2().get_name() == pair.get_dijet1().get_name())) and\
    #        ((self.get_dijet1().get_name() == pair.get_dijet2().get_name()) or\
    #         (self.get_dijet2().get_name() == pair.get_dijet2().get_name())))
