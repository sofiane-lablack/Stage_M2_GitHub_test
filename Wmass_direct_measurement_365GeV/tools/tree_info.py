'''Return the heppy reconstruction tree information'''

from ROOT import TLorentzVector


class TreeInfo(object):
    """Read and access the heppy reconstructed events"""

    def __init__(self):
        super(TreeInfo, self).__init__()

        evt = 0
        reco_level = 0

    def set_evt(self, evt, reco_level = 0, reco_type = ''):
        '''Information event i'''
        self.evt = evt
        self.reco_level = reco_level
        if reco_type != '':
            self.reco_type = '_' + reco_type
        else:
	    self.reco_type = ''

    def get_ptc(self, ptc_type):
        '''For a given ptc, build the ptc with its reco level'''
        if self.reco_level == 0 :
            ptc = ptc_type
        else:
            ptc = str(self.reco_level + "_" + ptc_type + self.reco_type)
        return ptc


    def get_p4(self, ptc_type):
        '''Build the particle four vector'''

        energy = eval("self.evt." + self.get_ptc(ptc_type) + "_e")
        p_x = eval("self.evt." + self.get_ptc(ptc_type) + "_px")
        p_y = eval("self.evt." + self.get_ptc(ptc_type) + "_py")
        p_z = eval("self.evt." + self.get_ptc(ptc_type) + "_pz")

        return TLorentzVector(p_x, p_y, p_z, energy)
    
    def get_y34(self):
	'''get y34 brqnch from the tree'''
	return self.evt.y34

    def get_file_type(self):
	'''get file type for normalisation '''
	filetype = self.evt.file_type
	return filetype

    def get_reco_jet1_e(self):
	'''get energy of 1st jet '''
	ejet1 = self.evt.reco_jet1_e
	return ejet1

    def get_reco_jet2_e(self):
	'''get energy of 2nd jet '''
	ejet2 = self.evt.reco_jet2_e
	return ejet2

    def get_reco_jet3_e(self):
	'''get energy of 3rd jet '''
	ejet3 = self.evt.reco_jet3_e
	return ejet3

    def get_reco_jet4_e(self):
	'''get energy of 4th jet '''
	ejet4 = self.evt.reco_jet4_e
	return ejet4

    def get_reco_jet1_11_e(self):
	'''get energy of electrons jet1'''
	eelecj1 = self.evt.reco_jet1_11_e
	return eelecj1

    def get_reco_jet1_13_e(self):
	'''get energy of muons jet 1'''
	emuonj1 = self.evt.reco_jet1_13_e
	return emuonj1

    def get_reco_jet1_130_e(self):
	'''get energy of kaon jet 1'''
	ekaonj1 = self.evt.reco_jet1_130_e
	return ekaonj1

    def get_reco_jet1_211_e(self):
	'''get energy of pion jet 1'''
	epionj1 = self.evt.reco_jet1_211_e
	return epionj1

    def get_reco_jet2_11_e(self):
	'''get energy of electrons jet2'''
	eelecj2 = self.evt.reco_jet2_11_e
	return eelecj2

    def get_reco_jet2_13_e(self):
	'''get energy of muons jet 2'''
	emuonj2 = self.evt.reco_jet2_13_e
	return emuonj2

    def get_reco_jet2_130_e(self):
	'''get energy of kaon jet 2'''
	ekaonj2 = self.evt.reco_jet2_130_e
	return ekaonj2

    def get_reco_jet2_211_e(self):
	'''get energy of pion jet 2'''
	epionj2 = self.evt.reco_jet2_211_e
	return epionj2

    def get_reco_jet3_11_e(self):
	'''get energy of electrons jet3'''
	eelecj3 = self.evt.reco_jet3_11_e
	return eelecj3

    def get_reco_jet3_13_e(self):
	'''get energy of muons jet 3'''
	emuonj3 = self.evt.reco_jet3_13_e
	return emuonj3

    def get_reco_jet3_130_e(self):
	'''get energy of kaon jet 3'''
	ekaonj3 = self.evt.reco_jet3_130_e
	return ekaonj3

    def get_reco_jet3_211_e(self):
	'''get energy of pion jet 3'''
	epionj3 = self.evt.reco_jet3_211_e
	return epionj3

    def get_reco_jet4_11_e(self):
	'''get energy of electrons jet4'''
	eelecj4 = self.evt.reco_jet4_11_e
	return eelecj4

    def get_reco_jet4_13_e(self):
	'''get energy of muons jet 4'''
	emuonj4 = self.evt.reco_jet4_13_e
	return emuonj4

    def get_reco_jet4_130_e(self):
	'''get energy of kaon jet 4'''
	ekaonj4 = self.evt.reco_jet4_130_e
	return ekaonj4

    def get_reco_jet4_211_e(self):
	'''get energy of pion jet 4'''
	epionj4 = self.evt.reco_jet4_211_e
	return epionj4
#	ejet2 = eval("self.evt."+ self.get_ptc(ptc_type)+"_e")
#	ejet3 = eval("self.evt."+ self.get_ptc(ptc_type)+"_e")
#	ejet4 = eval("self.evt."+ self.get_ptc(ptc_type)+"_e")
 #   def get energychargedpart(self,ptc_type):
#	'''get energy of charged part'''
#	eelec =eval("self.evt."+self.get

    def get_pdgid(self, ptc):
        '''Return the pdgid of the particle'''
        return eval("self.evt." + self.get_ptc(ptc) + "_pdgid")

    def get_w_mass(self, ptc_type):
        '''Return the simulated W boson mass'''
        return eval("self.evt." + ptc_type + "_m")

    def get_dim(self, ptc_type):
        '''Return the dimension of the particle'''
        return int(eval("self.evt." + self.get_ptc(ptc_type) + "_size"))

    def get_jet_ptc_charged_e(self,jet):
        '''Return the sum of charged particles in jet'''
        pdgidcharged = ["211", "11", "13"]
        sum_energy=0
        for pdgcharged in pdgidcharged:
		e_charged = eval("self.evt." + self.reco_level + "_" + jet + "_" + pdgcharged + "_e")
		sum_energy+=e_charged
        return sum_energy

    def get_jet_compo(self, jet):
        ''' Return the PDGid of the jet components'''

        pdgid = ["211", "22", "130", "11", "13"]
        components = {}

        for pid in pdgid:
            compo = eval("self.evt." + self.reco_level + "_" + jet + "_" + pid + "_num")
            components[pid] = compo

        return components

if __name__ == '__main__':
    pass
