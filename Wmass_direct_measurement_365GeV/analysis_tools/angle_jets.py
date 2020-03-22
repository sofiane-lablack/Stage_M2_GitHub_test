''' jet angles for good and bad pairing '''

from ROOT import TCanvas, TGraph, TLegend, TLatex, TFile, gDirectory, TH1F
from array import array

from tools.tree_info import *
import tools.histogram as histogram

from particles.jets import Jet
from particles.dijets import Dijet


def gethists():
    """function to book all histograms and return as dictionary"""
    histdict = {}

    histdict["h_angle_goodPairing"] = TH1F('h_angle_goodPairing', 'Angle between good paired jets', 180, 0, 180)
    histdict["h_angle_badPairing"] = TH1F('h_angle_badPairing', 'Angle between wrong paired jets', 180, 0, 180)

    return histdict


def angle_study(tree, histdict):

    for iev, evt in enumerate(tree):

        if iev%1000 == 0:
            print("Processing events {} on {} ".format(iev, tree.GetEntries()))

        pvec = get_jets_p4(evt, "gen_jet")
        dim = int(get_jet_dim(evt, "gen_jet"))

        jets = [Jet() for i in range(dim)]
        for jid, jet in enumerate(jets):
            jet.set_id(str(jid+1))
            jet.set_p4(pvec[jid])

        # Good jet pairing
        dijet12_good = Dijet(jets[0], jets[1])
        dijet34_good = Dijet(jets[2], jets[3])

        histdict["h_angle_goodPairing"].Fill(dijet12_good.get_angle())
        histdict["h_angle_goodPairing"].Fill(dijet34_good.get_angle())

        # Bad Pairing
        dijet13_wrong = Dijet(jets[0], jets[2])
        dijet24_wrong = Dijet(jets[1], jets[3])

        dijet14_wrong = Dijet(jets[0], jets[3])
        dijet23_wrong = Dijet(jets[1], jets[2])

        histdict["h_angle_badPairing"].Fill(dijet13_wrong.get_angle())
        histdict["h_angle_badPairing"].Fill(dijet24_wrong.get_angle())
        histdict["h_angle_badPairing"].Fill(dijet14_wrong.get_angle())
        histdict["h_angle_badPairing"].Fill(dijet23_wrong.get_angle())

def main():

    # input
    indir = '../heppy_output/reconnectionStudy/'
    infile = indir + 'ee_WW_qqqq_300_50K_M80_genLevel_ee_kt_woReconnection_woISR_woFSR_woRemnant_perfectPairing.root'

    rootfile = TFile(infile)
    tree = rootfile.Get("events")

    # output
    outdir = "./output/testHadronicChannel/genLevelStudy/reconnection/angleStudy"

    histdict = gethists()
    angle_study(tree, histdict)

    histogram.save_root_file(histdict, outdir)


if __name__ == "__main__":
    main()