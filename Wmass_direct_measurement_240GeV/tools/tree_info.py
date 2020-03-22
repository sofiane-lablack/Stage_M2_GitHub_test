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

    def get_gen_jet1_e(self):
        '''get energy of 1st get'''
        egenjet1 = self.evt.gen_jet1_e
        return egenjet1

    def get_gen_jet2_e(self):
        '''get energy of 2st get'''
        egenjet2 = self.evt.gen_jet2_e
        return egenjet2

    def get_gen_jet3_e(self):
        '''get energy of 3st get'''
        egenjet3 = self.evt.gen_jet3_e
        return egenjet3

    def get_gen_jet4_e(self):
        '''get energy of 4st get'''
        egenjet4 = self.evt.gen_jet4_e
        return egenjet4

    def get_gen_jet1_px(self):
        '''get px of 1st get'''
        pxgenjet1 = self.evt.gen_jet1_px
        return pxgenjet1

    def get_gen_jet2_px(self):
        '''get px of 2st get'''
        pxgenjet2 = self.evt.gen_jet2_px
        return pxgenjet2

    def get_gen_jet3_px(self):
        '''get px of 3st get'''
        pxgenjet3 = self.evt.gen_jet3_px
        return pxgenjet3

    def get_gen_jet4_px(self):
        '''get px of 4st get'''
        pxgenjet4 = self.evt.gen_jet4_px
        return pxgenjet4

    def get_gen_jet1_py(self):
        '''get py of 1st get'''
        pygenjet1 = self.evt.gen_jet1_py
        return pygenjet1

    def get_gen_jet2_py(self):
        '''get py of 2st get'''
        pygenjet2 = self.evt.gen_jet2_py
        return pygenjet2

    def get_gen_jet3_py(self):
        '''get py of 3st get'''
        pygenjet3 = self.evt.gen_jet3_py
        return pygenjet3

    def get_gen_jet4_py(self):
        '''get py of 4st get'''
        pygenjet4 = self.evt.gen_jet4_py
        return pygenjet4

    def get_gen_jet1_pz(self):
        '''get pz of 1st get'''
        pzgenjet1 = self.evt.gen_jet1_pz
        return pzgenjet1

    def get_gen_jet2_pz(self):
        '''get pz of 2st get'''
        pzgenjet2 = self.evt.gen_jet2_pz
        return pzgenjet2

    def get_gen_jet3_pz(self):
        '''get pz of 3st get'''
        pzgenjet3 = self.evt.gen_jet3_pz
        return pzgenjet3

    def get_gen_jet4_pz(self):
        '''get pz of 4st get'''
        pzgenjet4 = self.evt.gen_jet4_pz
        return pzgenjet4

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

    def get_reco_jet1_px(self):
	'''get px of 1st jet '''
	pxjet1 = self.evt.reco_jet1_px
	return pxjet1

    def get_reco_jet2_px(self):
	'''get px of 2nd jet '''
	pxjet2 = self.evt.reco_jet2_px
	return pxjet2

    def get_reco_jet3_px(self):
	'''get px of 3rd jet '''
	pxjet3 = self.evt.reco_jet3_px
	return pxjet3

    def get_reco_jet4_px(self):
	'''get px of 4th jet '''
	pxjet4 = self.evt.reco_jet4_px
	return pxjet4

    def get_reco_jet1_py(self):
	'''get py of 1st jet '''
	pyjet1 = self.evt.reco_jet1_py
	return pyjet1

    def get_reco_jet2_py(self):
	'''get py of 2nd jet '''
	pyjet2 = self.evt.reco_jet2_py
	return pyjet2

    def get_reco_jet3_py(self):
	'''get py of 3rd jet '''
	pyjet3 = self.evt.reco_jet3_py
	return pyjet3

    def get_reco_jet4_py(self):
	'''get py of 4th jet '''
	pyjet4 = self.evt.reco_jet4_py
	return pyjet4

    def get_reco_jet1_pz(self):
	'''get pz of 1st jet '''
	pzjet1 = self.evt.reco_jet1_pz
	return pzjet1

    def get_reco_jet2_pz(self):
	'''get pz of 2nd jet '''
	pzjet2 = self.evt.reco_jet2_pz
	return pzjet2

    def get_reco_jet3_pz(self):
	'''get pz of 3rd jet '''
	pzjet3 = self.evt.reco_jet3_pz
	return pzjet3

    def get_reco_jet4_pz(self):
	'''get pz of 4th jet '''
	pzjet4 = self.evt.reco_jet4_pz
	return pzjet4

    def get_reco_jet_size(self):
	'''get jet size'''
	jetsize = self.evt.reco_jet_size
	return jetsize

    def get_quark_size(self):
        '''get quark size'''
        quarksize = self.evt.quark_size
        return quarksize

    def get_gen_jet_size(self):
	'''get gen jet size'''
	genjetsize = self.evt.gen_jet_size
	return genjetsize

    def get_quark1_e(self):
        '''get quark1_e'''
        quark1_e = self.evt.quark1_e
        return quark1_e

    def get_quark2_e(self):
        '''get quark2_e'''
        quark2_e = self.evt.quark2_e
        return quark2_e

    def get_quark3_e(self):
        '''get quark3_e'''
        quark3_e = self.evt.quark3_e
        return quark3_e

    def get_quark4_e(self):
        '''get quark4_e'''
        quark4_e = self.evt.quark4_e
        return quark4_e

    def get_quark1_px(self):
        '''get quark1_px'''
        quark1_px = self.evt.quark1_px
        return quark1_px

    def get_quark2_px(self):
        '''get quark2_px'''
        quark2_px = self.evt.quark2_px
        return quark2_px

    def get_quark3_px(self):
        '''get quark3_px'''
        quark3_px = self.evt.quark3_px
        return quark3_px

    def get_quark4_px(self):
        '''get quark4_px'''
        quark4_px = self.evt.quark4_px
        return quark4_px

    def get_quark1_py(self):
        '''get quark1_py'''
        quark1_py = self.evt.quark1_py
        return quark1_py

    def get_quark2_py(self):
        '''get quark2_py'''
        quark2_py = self.evt.quark2_py
        return quark2_py

    def get_quark3_py(self):
        '''get quark3_py'''
        quark3_py = self.evt.quark3_py
        return quark3_py

    def get_quark4_py(self):
        '''get quark4_py'''
        quark4_py = self.evt.quark4_py
        return quark4_py

    def get_quark1_pz(self):
        '''get quark1_pz'''
        quark1_pz = self.evt.quark1_pz
        return quark1_pz

    def get_quark2_pz(self):
        '''get quark2_pz'''
        quark2_pz = self.evt.quark2_pz
        return quark2_pz

    def get_quark3_pz(self):
        '''get quark3_pz'''
        quark3_pz = self.evt.quark3_pz
        return quark3_pz

    def get_quark4_pz(self):
        '''get quark4_pz'''
        quark4_pz = self.evt.quark4_pz
        return quark4_pz

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
