from logging import DEBUG, ERROR, basicConfig, getLogger
from ROOT import TFile, TH1F, TCanvas, TH2F
import math

basicConfig(filename = "./accuracy/debug/debug_Wmass.log", level=DEBUG)

import tools.histogram as histogram
from tools.tree_info import *
from tools.association import  object_association

from particles.partons import Parton
from particles.jets import Jet

from analysis_tools.fit import fit


_logger = getLogger(__name__)


def gethists():
    """function to book all histograms and return as dictionary"""
    histdict = {}

    histdict["h_jet_energy"] = TH1F('h_jet_energy', 'Energy difference between parton energy and jet energy; E_{reco} - E_{parton} [GeV]', 200, -20, 20)
    return histdict


def energy_jet(tree, histdict, jet_type, outdir):
    '''Energy jet distribution'''

    # Run on events
    for iev, e in enumerate(tree):

        if iev%1000 == 0:
            print("Processing events {} over {}".format(iev, tree.GetEntries()))

        partons = [Parton() for i in range(int(get_parton_dim(e)))]
        for iparton, parton in enumerate(partons):
            parton.set_p4(get_parton_p4(e)[iparton])

        gen_jet = "gen_jet" + jet_type

        p4_gen_jets = get_jets_p4(e, gen_jet)
        gen_jets = [Jet()for i in range(int(get_jet_dim(e, gen_jet)))]
        for ijet, jet in enumerate(gen_jets):
            jet.set_p4(p4_gen_jets[ijet])

            if math.log(jet.get_boost()) == float('inf'):
                _logger.info("This event contains at least one gen jet with infinity boost (beta = 1) -> Discarded")
                _logger.info("Bad jet with single photon")
                continue

        # elem[0] = reco_jet, elem[1] = parton
        pj_asso = object_association(gen_jets, partons)

        for iel, elem in enumerate(pj_asso):
            histdict['h_jet_energy'].Fill(elem[0].get_E() - elem[1].get_E())

    c_ = TCanvas('c_', '', 700, 500)
    c_.cd()
    histdict["h_jet_energy"].Draw()
    c_.Print("{}.pdf".format(outdir))



def main():
    ''' Main function, define paramters and process the correlation matrix definition'''

    # parameters to choose the study
    Ecm = 240  #GeV
    mW = 80.385  #GeV
    nEvt = 50 #K
    channel = 'hadronic'

    jet_type = ""

    if channel == 'hadronic':
        decay = 'qqqq'
    else:
        decay = 'qqll'

    R = '3'

    # input
    filename = "../heppy_output/algoStudyHadro/g1.3/ee_WW_{}_{}_{}K_M{}_genLevel_valencia_R{}_b1_g1.3.root".format(decay, Ecm, nEvt, str(mW)[:2], R)
    _logger.info("Reading from file %s", filename)
    rootfile = TFile(filename)
    tree = rootfile.Get("events")
    _logger.debug("Get the tree %s", tree)

    # Output
    outdir = "../parallele_study/output/algo_valencia/ee_WW_{}_{}_{}K_M{}_genLevel_valencia_R{}_b1_g1.3".format(decay, Ecm, nEvt, str(mW)[:2], R)

    histdict = gethists()
    energy_jet(tree, histdict, jet_type, outdir)



if __name__ == '__main__':
    main()
