# -*- coding: utf-8 -*-
''' Measurement of the W mass from the ee->WW decay from the direct reconstruction of the invariant
 masses.
 First step : compute the jets energy from the directions
 Second step : find the jet pairs (chi2 minimization)
 Third step : reconstructed invariant mass distribution and angle distribution
 Save everything in root file'''

import sys

from ROOT import TFile, TH1F, TCanvas, gPad, TLegend, TH2F, gDirectory, TF1, TLorentzVector, TTree, gROOT, AddressOf
from array import array

import tools.histogram as histogram
from energy.energy import energy_from_direction, get_beta_matrix
import energy.rescaling_factors as rescaling_factors


from tools.tree_info import TreeInfo
from particles.jets import Jet
from particles.particle import Particle
from particles.dijets import Dijet
from pairing.dijetsPairs import DijetsPairs
from pairing.BestPair import BestPair

#file1 = open("cuty34.txt","w+")
fileoutput1 = sys.argv[2]
treename = sys.argv[3]
outdirname = sys.argv[4]
#treecuts = TTree('T', 'Just A Tree' )
#treecuts.Branch('y34', treecuts )

def gethists():
    """function to book all histograms and return as dictionary"""
    histdict = {}

    dijet = ['1', '2']

    histdict["h_mass_sum"] = TH1F('h_mass_sum', 'Sum of computed mW', 120, 40, 120)
    histdict["h_mass"] = TH1F('h_mass', 'Both computed mW', 120, 40, 120)
    histdict["h_mass_true"] = TH1F('h_mass_true', 'Comparison between reconstructed mass and Mtrue', 200, -15, 15)
    histdict["h_diffmW1_mW2"] = TH1F('h_|mw1-mw2|','Difference masse des 2 W',125,-5,120)

    for djet in dijet:
        histdict["h_angle_pair{}".format(djet)] = TH1F('h_angle_pair{}'.format(djet), 'Opening angle {}'.format(djet), 180, 0, 180)
        histdict["h_mW{}".format(djet)] = TH1F('h_mW{}'.format(djet), 'mW {} dijet selected'.format(djet), 140, 20, 120)
        histdict["h_mW{}_true".format(djet)] = TH1F("h_mW{}_true".format(djet), 'Comparison between reconstructed mass and Mtrue', 200, -15, 15)

    histdict["h_mW1_mW2"] = TH2F('h_mW1_mW2', 'Larger mass versus Smaller', 120, 40, 120, 120, 40, 120)


    return histdict
  

def check_content(tree):
    '''If one jet is containing only photons -> Discarded'''

    good_compo = True

    compo_j1 = tree.get_jet_compo("jet1")
    compo_j2 = tree.get_jet_compo("jet2")
    compo_j3 = tree.get_jet_compo("jet3")
    compo_j4 = tree.get_jet_compo("jet4")

#    print compo_j1

    result_j1 = [value for key, value in compo_j1.items() if key not in "22"]
    result_j2 = [value for key, value in compo_j2.items() if key not in "22"]
    result_j3 = [value for key, value in compo_j3.items() if key not in "22"]
    result_j4 = [value for key, value in compo_j4.items() if key not in "22"]

#    print 'result_j1 = ', result_j1

    if all([v == 0 for v in result_j1]) or all([v == 0 for v in result_j2]\
     or all([v == 0 for v in result_j3]) or all([v == 0 for v in result_j4])):
        good_compo = False

    return good_compo

def w_mass_hadronic(tree, ecm, m_w, histdict, reconstruction, reco_level, reco_type=''):
    '''Run over the hadronic events and save the histograms'''

    f1 = TFile('signal_and_bkg_cut_240GeV.root',"update")
    treecut = TTree(treename,"tree title")
    y34 = array('f',[0])
    reco_jet1_e = array('f',[0])
    reco_jet2_e = array('f',[0])
    reco_jet3_e = array('f',[0])
    reco_jet4_e = array('f',[0])
    reco_jet1_px = array('f',[0])
    reco_jet2_px = array('f',[0])
    reco_jet3_px = array('f',[0])
    reco_jet4_px = array('f',[0])
    reco_jet1_py = array('f',[0])
    reco_jet2_py = array('f',[0])
    reco_jet3_py = array('f',[0])
    reco_jet4_py = array('f',[0])
    reco_jet1_pz = array('f',[0])
    reco_jet2_pz = array('f',[0])
    reco_jet3_pz = array('f',[0])
    reco_jet4_pz = array('f',[0])
    reco_jet_size = array('f',[0])
    file_type = array('f',[0])
    quark_size = array('f',[0])
    quark1_e = array('f',[0])
    quark2_e = array('f',[0])
    quark3_e = array('f',[0])
    quark4_e = array('f',[0])
    quark1_px = array('f',[0])
    quark2_px = array('f',[0])
    quark3_px = array('f',[0])
    quark4_px = array('f',[0])
    quark1_py = array('f',[0])
    quark2_py = array('f',[0])
    quark3_py = array('f',[0])
    quark4_py = array('f',[0])
    quark1_pz = array('f',[0])
    quark2_pz = array('f',[0])
    quark3_pz = array('f',[0])
    quark4_pz = array('f',[0])
    gen_jet_size = array('f',[0])
    gen_jet1_e = array('f',[0])
    gen_jet2_e = array('f',[0])
    gen_jet3_e = array('f',[0])
    gen_jet4_e = array('f',[0])

    gen_jet1_px = array('f',[0])
    gen_jet2_px = array('f',[0])
    gen_jet3_px = array('f',[0])
    gen_jet4_px = array('f',[0])
    gen_jet1_py = array('f',[0])
    gen_jet2_py = array('f',[0])
    gen_jet3_py = array('f',[0])
    gen_jet4_py = array('f',[0])
    gen_jet1_pz = array('f',[0])
    gen_jet2_pz = array('f',[0])
    gen_jet3_pz = array('f',[0])
    gen_jet4_pz = array('f',[0])


    treecut.Branch("y34",y34,'y34/F')
    treecut.Branch("reco_jet1_e",reco_jet1_e,'reco_jet1_e/F')
    treecut.Branch("reco_jet2_e",reco_jet2_e,'reco_jet2_e/F')
    treecut.Branch("reco_jet3_e",reco_jet3_e,'reco_jet3_e/F')
    treecut.Branch("reco_jet4_e",reco_jet4_e,'reco_jet4_e/F')
    treecut.Branch("reco_jet1_px",reco_jet1_px,'reco_jet1_px/F')
    treecut.Branch("reco_jet2_px",reco_jet2_px,'reco_jet2_px/F')
    treecut.Branch("reco_jet3_px",reco_jet3_px,'reco_jet3_px/F')
    treecut.Branch("reco_jet4_px",reco_jet4_px,'reco_jet4_px/F')
    treecut.Branch("reco_jet1_py",reco_jet1_py,'reco_jet1_py/F')
    treecut.Branch("reco_jet2_py",reco_jet2_py,'reco_jet2_py/F')
    treecut.Branch("reco_jet3_py",reco_jet3_py,'reco_jet3_py/F')
    treecut.Branch("reco_jet4_py",reco_jet4_py,'reco_jet4_py/F')
    treecut.Branch("reco_jet1_pz",reco_jet1_pz,'reco_jet1_pz/F')
    treecut.Branch("reco_jet2_pz",reco_jet2_pz,'reco_jet2_pz/F')
    treecut.Branch("reco_jet3_pz",reco_jet3_pz,'reco_jet3_pz/F')
    treecut.Branch("reco_jet4_pz",reco_jet4_pz,'reco_jet4_pz/F')
    treecut.Branch("reco_jet_size",reco_jet_size,'reco_jet_size/F')
    treecut.Branch("file_type",file_type,'file_type/F')
    treecut.Branch("quark_size",quark_size,'quark_size/F')
    treecut.Branch("quark1_e",quark1_e,'quark1_e/F')
    treecut.Branch("quark2_e",quark2_e,'quark2_e/F')
    treecut.Branch("quark3_e",quark3_e,'quark3_e/F')
    treecut.Branch("quark4_e",quark4_e,'quark4_e/F')
    treecut.Branch("quark1_px",quark1_px,'quark1_px/F')
    treecut.Branch("quark2_px",quark2_px,'quark2_px/F')
    treecut.Branch("quark3_px",quark3_px,'quark3_px/F')
    treecut.Branch("quark4_px",quark4_px,'quark4_px/F')
    treecut.Branch("quark1_py",quark1_py,'quark1_py/F')
    treecut.Branch("quark2_py",quark2_py,'quark2_py/F')
    treecut.Branch("quark3_py",quark3_py,'quark3_py/F')
    treecut.Branch("quark4_py",quark4_py,'quark4_py/F')
    treecut.Branch("quark1_pz",quark1_pz,'quark1_pz/F')
    treecut.Branch("quark2_pz",quark2_pz,'quark2_pz/F')
    treecut.Branch("quark3_pz",quark3_pz,'quark3_pz/F')
    treecut.Branch("quark4_pz",quark4_pz,'quark4_pz/F')
    treecut.Branch("gen_jet_size",gen_jet_size,'gen_jet_size/F')
    treecut.Branch("gen_jet1_e",gen_jet1_e,'gen_jet1_e/F')
    treecut.Branch("gen_jet2_e",gen_jet2_e,'gen_jet2_e/F')
    treecut.Branch("gen_jet3_e",gen_jet3_e,'gen_jet3_e/F')
    treecut.Branch("gen_jet4_e",gen_jet4_e,'gen_jet4_e/F')

    treecut.Branch("gen_jet1_px",gen_jet1_px,'gen_jet1_px/F')
    treecut.Branch("gen_jet2_px",gen_jet2_px,'gen_jet2_px/F')
    treecut.Branch("gen_jet3_px",gen_jet3_px,'gen_jet3_px/F')
    treecut.Branch("gen_jet4_px",gen_jet4_px,'gen_jet4_px/F')
    treecut.Branch("gen_jet1_py",gen_jet1_py,'gen_jet1_py/F')
    treecut.Branch("gen_jet2_py",gen_jet2_py,'gen_jet2_py/F')
    treecut.Branch("gen_jet3_py",gen_jet3_py,'gen_jet3_py/F')
    treecut.Branch("gen_jet4_py",gen_jet4_py,'gen_jet4_py/F')
    treecut.Branch("gen_jet1_pz",gen_jet1_pz,'gen_jet1_pz/F')
    treecut.Branch("gen_jet2_pz",gen_jet2_pz,'gen_jet2_pz/F')
    treecut.Branch("gen_jet3_pz",gen_jet3_pz,'gen_jet3_pz/F')
    treecut.Branch("gen_jet4_pz",gen_jet4_pz,'gen_jet4_pz/F')
    from_tree = TreeInfo()

    sign={}
    #eeqq
    bkg1={}
    #ZZqqll
    bkg2={}
    #ZZqqqq
    bkg3={}
    #WWqqll
    bkg4={}
    purete=[]
    efficacite=[]
    x=[]
#cut y34
#    for i in range(0,101):
#        j=i*0.001
#        x.append(j)
#    print x
#    for index, value in enumerate(x):
#	    print value
            
	#cut ejetcut
#    for i in range(0,2):
#        j=i*0.001
#        x.append(j)
#    print x
#    print len(x)
        #boucle sur les valeurs de cut

    for iev, evt in enumerate(tree):

        if iev%5000 == 0:
	    print("Processing events {} on {} ".format(iev, tree.GetEntries()))

	# Object from_tree to access the rootfile information
	from_tree.set_evt(evt, reco_level, reco_type)

	# Discard event where one jet is containing only photons and/or no clustered particles
	if from_tree.get_dim("jet") != 4:
	    continue

	if not check_content(from_tree):
	    continue

        #cut masses "similaires" des 2 W
        #if abs(m_large-m_small)<13:
        #    continue
	
	# cut y34
	if from_tree.get_y34()<=0.001:
	    continue

	#cut energy part chargees < 0.96 * energy jet
	energyjet1 = from_tree.get_reco_jet1_e()
	energyjet2 = from_tree.get_reco_jet2_e()
	energyjet3 = from_tree.get_reco_jet3_e()
	energyjet4 = from_tree.get_reco_jet4_e()
#		partchargees=['11','13','211']
	energypartchargeesjet1= from_tree.get_reco_jet1_11_e()+from_tree.get_reco_jet1_13_e()+from_tree.get_reco_jet1_211_e()
	energypartchargeesjet2= from_tree.get_reco_jet2_11_e()+from_tree.get_reco_jet2_13_e()+from_tree.get_reco_jet2_211_e()
	energypartchargeesjet3= from_tree.get_reco_jet3_11_e()+from_tree.get_reco_jet3_13_e()+from_tree.get_reco_jet3_211_e()
	energypartchargeesjet4= from_tree.get_reco_jet4_11_e()+from_tree.get_reco_jet4_13_e()+from_tree.get_reco_jet4_211_e()
	if energypartchargeesjet1 > 0.996 * energyjet1 or energypartchargeesjet2 > 0.996 * energyjet2 or energypartchargeesjet3 > 0.996 * energyjet3 or energypartchargeesjet4 > 0.996 * energyjet4:
		continue

	# Jets
	pvec = []
	for part in range(4):
	    njet = str("jet" + str(part + 1))
	    pvec.append(from_tree.get_p4(njet))

	jets = [Jet() for i in range(from_tree.get_dim("jet"))]
	# Direct reconstruction
	if reconstruction == "direct":
	    for jid, jet in enumerate(jets):
	        jet.set_id(str("jet" + str(jid + 1)))
	        jet.set_mref(m_w)
	        jet.set_p4(pvec[jid])

	# Energy Rescaling
	else:
	    beta = get_beta_matrix(pvec)
	    energy = energy_from_direction(ecm, beta, from_tree.get_dim("jet"))

	    # discarded events with energy < 0 solutions (no physics)
	    if any(energy < 0):
	        continue

	    # Need to rescale the p4 matrix
	    p4_resc = rescaling_factors.rescale(pvec, rescaling_factors.factor(energy, pvec))

	    for jid, jet in enumerate(jets):
	        jet.set_id(str("jet" + str(jid + 1)))
	        jet.set_mref(m_w)
	        jet.set_p4(p4_resc[jid])

	dijet = get_dijets_pairs(jets)

	# If the pairing conditions are not full
	if not dijet:
	    continue

	#cut energie dijets similaires
        #diffedjets = return_edijets(dijet)
        #if diffedjets>=30:
            continue

        openingangledj1, openingangledj2 = return_opening_angle(dijet)
        if openingangledj1 <= 60 or openingangledj2 <= 60 or openingangledj1 >= 145 or openingangledj2 >= 145:
            continue

        m_small, m_large = return_mass(dijet)

        #cut sur la masse de mW1 small mW2 large
        if m_large<=70: 
	#or m_small<40:               
            continue

	#fonction qui rempli les histos
	fill_histograms(dijet, histdict)
        #y34=from_tree.get_y34()
        #treecuts.Fill()
        y34[0] = from_tree.get_y34()
        reco_jet1_e[0] = from_tree.get_reco_jet1_e()
        reco_jet2_e[0] = from_tree.get_reco_jet2_e()
        reco_jet3_e[0] = from_tree.get_reco_jet3_e()
        reco_jet4_e[0] = from_tree.get_reco_jet4_e()
        reco_jet1_px[0] = from_tree.get_reco_jet1_px()
        reco_jet2_px[0] = from_tree.get_reco_jet2_px()
        reco_jet3_px[0] = from_tree.get_reco_jet3_px()
        reco_jet4_px[0] = from_tree.get_reco_jet4_px()
        reco_jet1_py[0] = from_tree.get_reco_jet1_py()
        reco_jet2_py[0] = from_tree.get_reco_jet2_py()
        reco_jet3_py[0] = from_tree.get_reco_jet3_py()
        reco_jet4_py[0] = from_tree.get_reco_jet4_py()
        reco_jet1_pz[0] = from_tree.get_reco_jet1_pz()
        reco_jet2_pz[0] = from_tree.get_reco_jet2_pz()
        reco_jet3_pz[0] = from_tree.get_reco_jet3_pz()
        reco_jet4_pz[0] = from_tree.get_reco_jet4_pz()
        reco_jet_size[0] = from_tree.get_reco_jet_size()
        quark_size[0] = from_tree.get_quark_size()
        file_type[0] = float(fileoutput1)
        quark1_e[0] = from_tree.get_quark1_e()
        quark2_e[0] = from_tree.get_quark2_e()
        quark3_e[0] = from_tree.get_quark3_e()
        quark4_e[0] = from_tree.get_quark4_e()
	quark1_px[0] = from_tree.get_quark1_px()
	quark2_px[0] = from_tree.get_quark2_px()
	quark3_px[0] = from_tree.get_quark3_px()
	quark4_px[0] = from_tree.get_quark4_px()
	quark1_py[0] = from_tree.get_quark1_py()
	quark2_py[0] = from_tree.get_quark2_py()
	quark3_py[0] = from_tree.get_quark3_py()
	quark4_py[0] = from_tree.get_quark4_py()
	quark1_pz[0] = from_tree.get_quark1_pz()
	quark2_pz[0] = from_tree.get_quark2_pz()
	quark3_pz[0] = from_tree.get_quark3_pz()
	quark4_pz[0] = from_tree.get_quark4_pz()
        gen_jet_size[0] = from_tree.get_gen_jet_size()
	gen_jet1_e[0] = from_tree.get_gen_jet1_e()
	gen_jet2_e[0] = from_tree.get_gen_jet2_e()
	gen_jet3_e[0] = from_tree.get_gen_jet3_e()
	gen_jet4_e[0] = from_tree.get_gen_jet4_e()

        gen_jet1_px[0] = from_tree.get_gen_jet1_px()
        gen_jet2_px[0] = from_tree.get_gen_jet2_px()
        gen_jet3_px[0] = from_tree.get_gen_jet3_px()
        gen_jet4_px[0] = from_tree.get_gen_jet4_px()
        gen_jet1_py[0] = from_tree.get_gen_jet1_py()
        gen_jet2_py[0] = from_tree.get_gen_jet2_py()
        gen_jet3_py[0] = from_tree.get_gen_jet3_py()
        gen_jet4_py[0] = from_tree.get_gen_jet4_py()
        gen_jet1_pz[0] = from_tree.get_gen_jet1_pz()
        gen_jet2_pz[0] = from_tree.get_gen_jet2_pz()
        gen_jet3_pz[0] = from_tree.get_gen_jet3_pz()
        gen_jet4_pz[0] = from_tree.get_gen_jet4_pz()
        #print str(quark4_pz[0])
        treecut.Fill()
    f1.cd()
    f1.Write()
    f1.Close()

def get_dijets_pairs(jets):
    '''Find the jets pairing'''

    # Dijets : compute the masses and the jet-jet angles
    dijet12 = Dijet(jets[0], jets[1])
    dijet34 = Dijet(jets[2], jets[3])
    dijet13 = Dijet(jets[0], jets[2])
    dijet24 = Dijet(jets[1], jets[3])
    dijet14 = Dijet(jets[0], jets[3])
    dijet23 = Dijet(jets[1], jets[2])

    # Dijets pairs : compute the chi and the sum angles
    dj_pair1 = DijetsPairs(dijet12, dijet34)
    dj_pair2 = DijetsPairs(dijet13, dijet24)
    dj_pair3 = DijetsPairs(dijet14, dijet23)

    best_pair = BestPair(dj_pair1, dj_pair2, dj_pair3)
    dijet_pair = best_pair.get_best_pair()

    # if the pairing never satisfy the conditions -> discarded event
    if dijet_pair == 0:
        return 0

    dijet_pair.compute()
    return dijet_pair

def return_edijets(dijets):

    dj_1 = dijets.get_dijet1()
    dj_2 = dijets.get_dijet2()

    dj1jet1 , dj1jet2 = dj_1.get_jets()
    dj2jet1 , dj2jet2 = dj_2.get_jets()

    energydj1jet1 = dj1jet1.get_E()
    energydj1jet2 = dj1jet2.get_E()

    energydj2jet1 = dj2jet1.get_E()
    energydj2jet2 = dj2jet2.get_E()

    energydj1 = energydj1jet1+energydj1jet2
    energydj2 = energydj2jet1+energydj2jet2

    diffedj = abs(energydj1-energydj2)
    return diffedj

def return_opening_angle(dijets):

    dj_1 = dijets.get_dijet1()
    dj_2 = dijets.get_dijet2()

    dj_1_angle = dj_1.get_angle()
    dj_2_angle = dj_2.get_angle()

    return dj_1_angle, dj_2_angle

def return_mass(dijets):
    dj_1 = dijets.get_dijet1()
    dj_2 = dijets.get_dijet2()

    m_small = min(dj_1.get_mass(), dj_2.get_mass())
    m_large = max(dj_1.get_mass(), dj_2.get_mass())

    return m_small, m_large


def fill_histograms(dijets, histdict):
    '''Function to fill all histograms'''

    m_small, m_large = return_mass(dijets)

    dj_1 = dijets.get_dijet1()
    dj_2 = dijets.get_dijet2()

#    histdict["h_diffmW1_mW2"].Fill(abs(m_large-m_small))
    histdict["h_mW1"].Fill(m_small)
    histdict["h_mW2"].Fill(m_large)
    histdict["h_mass_sum"].Fill((m_small + m_large)/2)
    histdict["h_mass"].Fill(m_small)
    histdict["h_mass"].Fill(m_large)


    #angular distribution between selected jets
    a_small = min(dj_1.get_angle(), dj_2.get_angle())
    a_large = max(dj_1.get_angle(), dj_2.get_angle())
    histdict["h_angle_pair1"].Fill(a_small)
    histdict["h_angle_pair2"].Fill(a_large)





def main():
    '''Main function which can run the hadronic and the semi-leptonic decay. The study is selected
    at the beginning with the parameters. Nothing should be changed in the function'''

    #input and output file from runWmass.sh
    fileinput1 = sys.argv[1]

    # parameters to choose the study
    ecm = 162.6
    m_w = 79.385
    width = '2'
    reconstruction = "direct"
    reco_level = 'reco'

    # NO NEED
    reco_type = ''
    FSI = 'BE'

    # Analysis
    histdict = gethists()
    filename = fileinput1
    #filename = "/afs/cern.ch/user/s/slablack/fcc/heppy/ee_qq_240_Bkg_50K_ee_kt_SM.root"
    print("Reading from file {}".format(filename))

    rootfile = TFile(filename)
    tree = rootfile.Get("events")


    # output file
    #outdir = fileoutput1
    outdir = outdirname
    print("Reading from file {} output file {}".format(filename,outdir))
    # outdir = "./output/hadronic/FSI_study/shift/woTreatment/W_mass_{}_M{}_width{}".format(ecm, str(m_w)[:2], width)

    # Function call
    w_mass_hadronic(tree, ecm, m_w, histdict, reconstruction, reco_level, reco_type)
    histogram.save_root_file(histdict, outdir)


if __name__ == '__main__':
    main()

