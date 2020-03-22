''' Measurement of the W mass from the ee->WW decay from the direct reconstruction of the invariant
    mass from the decay product.
 '''

from ROOT import TFile, TH1F, TH2F

import tools.histogram as histogram

from tools.tree_info import TreeInfo
from particles.jets import Jet
from particles.particle import Particle
from particles.dijets import Dijet
from particles.leptonic_decay import LeptonicDecay

def gethists():
    """function to book all histograms and return as dictionary"""
    histdict = {}

    histdict["h_mass_sum"] = TH1F('h_mass_sum', 'Sum of computed mW', 120, 40, 120)
    histdict["h_mass_lepto"] = TH1F('h_mass_lepto', 'mW of the leptonic part', 120, 40, 120.)
    histdict["h_mass_hadro"] = TH1F('h_mass_hadro', 'mW of the hadronic part', 120, 40, 120)

    histdict["h_angle_hadro"] = TH1F('h_angle_dijet', 'Opening angle between the W hadronic\'s jets', 180, 0, 180)

    histdict["h_mass_true"] = TH1F('h_mass_true', 'Comparison between reconstructed mass and Mtrue', 200, -15, 15)
    histdict["h_mass_hadro_true"] = TH1F("h_mass_hadro_true", 'Comparison between reconstructed hadronic mass and Mtrue', 200, -15, 15)
    histdict["h_mass_lepto_true"] = TH1F("h_mass_lepto_true", 'Comparison between reconstructed leptonic mass and Mtrue', 200, -15, 15)

    histdict["h_mass_lepto_hadro"] = TH2F('h_mass_lepto_hadro', 'Leptonic mass versus hadronic mass', 120, 40, 120, 120, 40, 120)

    return histdict


def check_jet_compo(tree):

    good_compo = True

    compo_j1 = tree.get_jet_compo("jet1")
    compo_j2 = tree.get_jet_compo("jet2")

    result_j1 = [value for key, value in compo_j1.items() if key not in "22"]
    result_j2 = [value for key, value in compo_j2.items() if key not in "22"]

    if all([v == 0 for v in result_j1]) or all([v == 0 for v in result_j2]):
        good_compo = False

    return good_compo



def w_mass_semi_leptonic(ecm, tree, histdict, reco_level):
    '''Run over the events and fill the histograms'''

    from_tree = TreeInfo()

    nDiscarded = 0
    for iev, evt in enumerate(tree):

        if iev%5000 == 0:
            print("Processing event {} on {} ".format(iev, tree.GetEntries()))


        # Object from_tree to access the rootfile information
        from_tree.set_evt(evt, reco_level)

        if from_tree.get_dim("lepton") != 1 or from_tree.get_dim("jet") != 2:
            nDiscarded += 1
            continue

        if not check_jet_compo(from_tree):
            nDiscarded += 1
            continue

        #### Leptonic decay part
        lepton = Particle(from_tree.get_p4("lepton"))
        misenergy = Particle(from_tree.get_p4("misenergy"))

        # Compute W mass from the lepton and the missing energy
        lep_decay = LeptonicDecay(lepton, misenergy)
        lep_decay.set_true_mass(from_tree.get_w_mass("leptonic_W"))
        lep_decay.compute()

        #### hadronic decay part
        jets = [Jet() for i in range(from_tree.get_dim("jet"))]
        for jid, jet in enumerate(jets):
            njet = str("jet" + str(jid + 1))
            jet.set_p4(from_tree.get_p4(njet))

        # Compute W mass from the jet and their angle
        dijet = Dijet(jets[0], jets[1])
        dijet.set_true_mass(from_tree.get_w_mass("hadronic_W"))
        dijet.compute()

        fill_histograms(ecm, histdict, dijet, lep_decay)
    print nDiscarded

def fill_histograms(ecm, histdict, dijet, lepto):
    ''' Fill histograms '''

    lepto_mass = lepto.get_mass()
    dijet_mass = dijet.get_mass()

    if ecm == 162.6:
        if lepto_mass > dijet_mass:
            histdict["h_mass_lepto"].Fill(lepto_mass)
        else:
            histdict["h_mass_hadro"].Fill(dijet_mass)
    else:
        histdict["h_mass_hadro"].Fill(dijet_mass)
        histdict["h_mass_lepto"].Fill(lepto_mass)

    histdict["h_mass_lepto_hadro"].Fill(dijet_mass, lepto_mass)
    histdict["h_mass_sum"].Fill((dijet_mass + lepto_mass)/2)

    m_hadro_diff = dijet.get_masses_difference()
    m_lepto_diff = lepto.get_masses_difference()

    histdict["h_mass_hadro_true"].Fill(m_hadro_diff)
    histdict["h_mass_lepto_true"].Fill(m_lepto_diff)
    histdict["h_mass_true"].Fill(m_lepto_diff + m_hadro_diff)

    histdict["h_angle_hadro"].Fill(dijet.get_angle())


def main():
    '''Main function which can run the hadronic and the semi-leptonic decay. The study is selected
    at the beginning with the parameters. Nothing should be changed in the function'''

    # parameters to choose the study
    nevts = "50K"
    ecm = 365
    m_w = 80.385
    width = '3'
    reco_level = "reco"

    # Analysis
    histdict = gethists()

    filename = "../heppy_output/pythia_2018/semi-leptonic/onlyMuons/width_variation/ee_WW_qqll_{}_{}_M{}_width{}.root".format(ecm, nevts, str(m_w)[:2], width)
    print("Reading from file {}".format(filename))

    rootfile = TFile(filename)
    tree = rootfile.Get("events")

    # output file
    outdir = "./output/pythia_2018/semi-leptonic/width_variation/W_mass_{}_{}_M{}_width{}_direct".format(ecm, nevts, str(m_w)[:2], width)

    w_mass_semi_leptonic(ecm, tree, histdict, reco_level)
    histogram.save_root_file(histdict, outdir)


if __name__ == '__main__':
    main()
