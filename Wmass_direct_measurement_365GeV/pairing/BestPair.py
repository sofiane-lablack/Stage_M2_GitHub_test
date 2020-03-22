from pairing.dijetsPairs import DijetsPairs

class BestPair(DijetsPairs):
    '''For the three different possible pairings : (12)(34), (13)(24) and (14)(23)
        the chi square (with respect to the mPDG = 80.385) is computed.
        For the dijet pair with the smallest Chi2 is selected if the sum of the jet-jet angles is
        not the smallest and if both W mass lie in [60, 110] GeV windows.
    '''

    def __init__(self, pair1, pair2, pair3):
        self.p1 = pair1
        self.p2 = pair2
        self.p3 = pair3

        self.first_chi2 = 0
        self.second_chi2 = 0
        self.third_chi2 = 0

        self.best_pair = 0

        self.good_pairing = 0
        self.wrong_pairing = 0

        self.find_best_pair()


    def get_best_pair(self):
        '''Return the selected dijet pair'''
        return self.best_pair

    def get_wrong_pairing(self):
        return self.wrong_pairing

    def get_good_pairing(self):
        return self.good_pairing

    def get_perfect_pairing(self):
        return self.p1

    def smallest_chi2(self):
        '''Select the pair with the smallest chi2'''

        chi_pair = {self.p1: self.p1.get_chi2(),
                    self.p2: self.p2.get_chi2(),
                    self.p3: self.p3.get_chi2()}

        import operator
        chi_pair = sorted(chi_pair.items(), key=operator.itemgetter(1))
        self.first_chi2 = chi_pair[0][0]
        self.second_chi2 = chi_pair[1][0]
        self.third_chi2 = chi_pair[2][0]


    def is_in_mass_range(self, mass):
        '''The dijet selected pair should have the masses between 60 and 110 GeV.'''

        if 60.0 <= mass <= 110:
            return True


    def find_best_pair(self):
        '''Find the best dijets pair, corresponding to criteria '''

        self.smallest_chi2()

        dj1 = self.first_chi2.get_dijet1()
        dj2 = self.first_chi2.get_dijet2()

        # if self.conditions(dj1, dj2):
        self.best_pair = self.first_chi2

            # if self.best_pair.is_equal_to(self.p1):
            #     self.good_pairing = self.first_chi2
            #     self.wrong_pairing = None
            # else:
            #     self.good_pairing = None
            #     self.wrong_pairing = self.first_chi2
        # else:
        #     dj1_bis = self.second_chi2.get_dijet1()
        #     dj2_bis = self.second_chi2.get_dijet2()

        #     if self.conditions(dj1_bis, dj2_bis):
        #         self.best_pair = self.second_chi2

        #         if self.best_pair.is_equal_to(self.p1):
        #             self.good_pairing = self.second_chi2
        #             self.wrong_pairing = None
        #         else:
        #             self.wrong_pairing = self.second_chi2
        #             self.good_pairing = None

        # else:
        #     self.best_pair = None
        #     self.good_pairing = None
        #     self.wrong_pairing = None

        # The pairing use the same jet several times -> discarded event
        if self.best_pair:
            if not self.verif_pairing():
                return 0


    def conditions(self, dj1, dj2):
        '''Function to test the pairing conditions'''
        is_ok = False
        if self.is_in_mass_range(dj1.get_mass()) and self.is_in_mass_range(dj2.get_mass()):
            is_ok = True

        return is_ok


    def verif_pairing(self):
        '''The pairing should contain only once at time the jet 1, 2, 3, 4
        if the pairs contain the same jet twice, the event is discarded'''

        j1, j2 = self.best_pair.get_dijet1().get_jets()
        j3, j4 = self.best_pair.get_dijet2().get_jets()

        j_list = [j1.get_id(), j2.get_id(), j3.get_id(), j4.get_id()]
        if len(set(j_list)) == 4:
            return True
