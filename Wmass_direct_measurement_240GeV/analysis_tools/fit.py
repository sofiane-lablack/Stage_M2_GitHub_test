#!/usr/bin/env python
from ROOT import TCanvas, TFile, TF1, gDirectory, TLatex, TLegend, TObject, gStyle, gPad
from array import array
import sys
from math import sqrt

sys.path.insert(0, '../tools/')
import tools.histogram as histogram



def fit(histo, outdir, file=0, Ecm=0):
    """Fit the transverse profile to gat the parametrization and save in root file"""

    canvas_fit = TCanvas("c_fit_{}_{}".format(histo, Ecm),"c_fit",800,600)

    if not file:
        infile = outdir + ".root"
    else:
        infile = file

    file_ = TFile(infile,"r")
    file_.cd()

    g_fit = gDirectory.Get(histo)
    g_fit.Draw()

    par = array( 'd', 13*[0.] )

    f1 = TF1("f1","gaus", -4, -3.5)
    g_fit.Fit(f1, "R0")
    par1 = f1.GetParameters()

    tail1 = TF1("tail1","crystalball", -6, -3.5)
    tail1.SetParameters(par1[0], par1[1], par1[2], 1.0, 1.6)
    tail1.SetLineColor(3)
    g_fit.Fit(tail1, "R0+")
    par2 = tail1.GetParameters()

    tail2 = TF1("tail2","crystalball", -4, -2)
    tail2.SetParameters(par1[0], par1[1], par1[2], -0.68, 1.85)
    tail2.SetLineColor(4)
    g_fit.Fit(tail2, "R0+")
    par3 = tail2.GetParameters()

    par[0], par[1], par[2] = par1[0], par1[1], par1[2]
    par[3], par[4], par[5], par[6], par[7] = par2[0], par1[1], par2[2], par2[3], par2[4]
    par[8], par[9], par[10], par[11], par[12] = par3[0], par1[1], par3[2], par3[3], par3[4]
    total = TF1("total", 'gaus(0)+crystalball(3)+crystalball(8)', -6, -2.3)
    total.SetParameters(par)
    total.SetLineColor(1)
    g_fit.Fit(total, "R+")


    # gStyle.SetOptFit(1)
    tot_param = total.GetParameters()
    sum_sigma = sqrt(tot_param[2]*tot_param[2] + tot_param[5]*tot_param[5] + tot_param[10]*tot_param[10])
    print sum_sigma

    sum_sigma2 = sqrt(par1[2]*par1[2] + par2[2]*par2[2] + par3[2]*par3[2])
    print "Verif = ", sum_sigma2

    uncertainty = TLatex()
    uncertainty.DrawLatex(0, 0, "#sigma = {}".format(sum_sigma))

    # write into the output file and close the file0
    outFileName = "{}.root".format(outdir)
    outFile = TFile(outFileName, "UPDATE")

    raw_input("hit a key to exit")

    canvas_fit.Write("", TObject.kOverwrite)
    outFile.Write()
    outFile.Close()

    # canvas_fit.Print("{}/gaus_fit_{}_{}.pdf".format(outdir, histo, Ecm))


def main():
    """Main function"""

    # Ecm = 350
    # mW = 80.385
    # nEvents = 10000
    # channel = 'semi_leptonic'
    # detector = 'wo_detector'

    # if detector == 'detector':
    #     det_type = 'CLIC'
    # else:
    #     det_type = ''

    # dire = "/afs/cern.ch/work/m/mabeguin/private/Wmass_direct_measurement/plots/{}/{}/{}/{}GeV/".format(detector, det_type, channel, Ecm)
    # outdir = "../plots/{}/{}/{}/gaus_fit".format(detector, det_type, channel)

    # histogram.create_output_dir(outdir)

    # file = dire+"W_mass_{}_{}_{}_ee_kt.root".format(Ecm, nEvents, mW)
    # print "Opening file: ", file

    # fit("h_mass_pair1", outdir, file, Ecm)


if __name__ == '__main__':
    main()
