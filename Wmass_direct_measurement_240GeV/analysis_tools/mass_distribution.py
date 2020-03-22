import numpy as np
from math import sqrt

from ROOT import TCanvas, TGraph, TLatex, TLegend, TFile, TObject


def read_file_stat(filename) :
    '''Read the file and return the list(energy, type, stat)'''

    with open(filename, "r") as fle:
        lines = fle.readlines()
        stat = []
        mass_value = []

        for il, x in enumerate(lines):
            stat.append(float(x.split(' ')[3]))
            mass_value.append(float(x.split(' ')[5]))

    return zip(stat, mass_value)


def mass(energies, stat_info):
    #Plot the FOM evolution as function of the energy

    # e_stat_direct = read_file_stat("{}/data/fom_stat_{}_direct{}.txt".format(file_dir, channel, fom_type))
    # e_stat_simple = read_file_stat("{}/data/fom_stat_{}_simple_rescaling{}.txt".format(file_dir, channel, fom_type))

    # stat_simple = calculation_stat(e_stat_simple, nentries, corr_simple, mass)
    # stat_direct = calculation_stat(e_stat_direct, nentries, corr_direct, mass)
    sigma_min = stat_info[4][0]
    sigma_max = stat_info[5][0]

    mass_min = stat_info[4][1]
    mass_max = stat_info[5][1]

    num = mass_min/sigma_min**2 + mass_max/sigma_max**2
    denum = 1/sigma_min**2 + 1/sigma_max**2

    print num / denum

    # stat_kinfit2 = calculation_stat_onlyOneMass(e_stat_kinfit2, nentries)

    # c_stat_vs_e = TCanvas("c_stat_vs_e", "c_stat_vs_e")
    # c_stat_vs_e.cd()

    # npts = len(energies)
    # gr_simple = TGraph(npts, energies, stat_simple)
    # gr_direct = TGraph(npts, energies, stat_direct)
    # gr_kinfit1 = TGraph(npts, energies, stat_kinfit1)
    # gr_kinfit2 = TGraph(npts, energies, stat_kinfit2)

    # gr_direct.GetXaxis().SetTitle("#sqrt{s} [GeV]")
    # gr_direct.GetXaxis().SetTitleSize(0.04)
    # gr_direct.GetXaxis().SetRangeUser(153, 390)
    # gr_direct.GetYaxis().SetRangeUser(10., 100.)
    # # gr_direct.GetYaxis().SetRangeUser(0., 1.4)
    # gr_direct.GetYaxis().SetTitle("#Delta M_{W, stat}  [MeV]")
    # gr_direct.GetYaxis().SetTitleSize(0.04)
    # gr_direct.GetYaxis().SetTitleOffset(1)
    # gr_direct.GetYaxis().SetLabelSize(0.04)
    # gr_direct.SetTitle("Variation of the statistical uncertainty of W mass as function of E_{CM}")

    # gr_direct.SetMarkerColor(1)
    # gr_simple.SetMarkerColor(8)
    # gr_kinfit1.SetMarkerColor(2)
    # gr_kinfit2.SetMarkerColor(4)

    # gr_simple.SetMarkerStyle(23)
    # gr_simple.SetMarkerSize(2)
    # gr_direct.SetMarkerStyle(23)
    # gr_direct.SetMarkerSize(2)
    # gr_kinfit1.SetMarkerStyle(23)
    # gr_kinfit1.SetMarkerSize(2)
    # gr_kinfit2.SetMarkerStyle(23)
    # gr_kinfit2.SetMarkerSize(2)

    # gr_direct.Draw("AP")
    # gr_simple.Draw("SAME P")
    # gr_kinfit1.Draw("SAME P")
    # gr_kinfit2.Draw("SAME P")


    # mylegend = TLegend(0.3, 0.65, 0.68, 0.88)
    # mylegend.SetFillColor(0)
    # mylegend.SetBorderSize(2)
    # mylegend.SetTextSize(0.04)
    # mylegend.AddEntry(gr_direct, "Raw mass", "p")
    # mylegend.AddEntry(gr_simple, "4C kinematic rescaling", "p")
    # mylegend.AddEntry(gr_kinfit1, "{}C Kinematic Fit".format(constraints_list[0]), "p")
    # mylegend.AddEntry(gr_kinfit2, "{}C Kinematic Fit".format(constraints_list[1]), "p")
    # mylegend.Draw()

    # raw_input("hit a key to exit")

    # # write into the output file and close the file
    # c_stat_vs_e.Print("{}/stat/stat_vs_E_{}{}{}_{}_gen_testFormule_woEff.pdf".format(file_dir, channel, param, fom_type, mass))
    # outfile = TFile("{}/stat/stat_vs_E_{}{}{}_{}_gen_testFormule_woEff.root".format(file_dir, channel, param, fom_type, mass), "UPDATE")
    # c_stat_vs_e.Write("", TObject.kOverwrite)
    # outfile.Write()
    # outfile.Close()


def main():

    # energies = np.array([162.6, 240, 365])
    energies = [365]
    channel = 'hadronic'
    fom_type = '_sophisticated'

    # if channel == 'hadronic':
    #     constraints_list = [4, 5]
    # else:
    #     constraints_list = [1, 2]

    file_dir = "./output/testHadronicChannel/recoLevel/woCR/reco/FOM/data"
    stat_info = read_file_stat("{}/fom_stat_{}_4C_logBoost{}.txt".format(file_dir, channel, fom_type))

    mass(energies, stat_info)

if __name__ == '__main__':
    main()
