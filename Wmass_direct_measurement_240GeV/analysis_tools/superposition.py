""" With this file you can overlap several histograms previously build """

from ROOT import TFile, gDirectory, TCanvas, gPad, TLegend, TObject, TAttLine, TLatex


def overlap(outdir, file1, file2 = 0):

  file_1 = TFile(file1, "r")
  # file_2 = TFile(file2, "r")

  h_name = ["h_mass_sum_reco_jet_cone", "h_mass_pair_reco_jet_cone1", "h_mass_pair_reco_jet_cone2", "h_mass_true_reco_jet_cone"]

  for h in h_name:
    h_good = h + "_good"
    h_bad = h + "_wrong"

    cname = "c_"+ h + "good_bad_jet_association"
    canvas_name = TCanvas(cname, "c_", 800, 600)
    canvas_name.cd()

    file_1.cd()
    h_1 = gDirectory.Get(h_good)
    # h_reco1 = gDirectory.Get(h_reco)

    # file_2.cd()
    h_2 = gDirectory.Get(h_bad)
    # h_reco2 = gDirectory.Get(h_reco)

    h_1.SetLineColor(4)
    # h_reco1.SetLineColor(2)

    h_2.SetLineColor(2)
    # h_reco2.SetLineColor(6)

    # if (h == "h_beta_"):
    #     h_reco2.Draw("HIST E")
    #     h_gen2.Draw("HIST E SAMES")
    # else :
        # h_gen2.Draw("HIST E")
        # h_reco2.Draw("HIST E SAMES")

    h_1.Draw("HIST E")
    h_2.Draw("HIST E SAMES")


    # # # h_reclu.GetYaxis().SetRangeUser(0, 0.21)
    # # h_reclu.GetXaxis().SetRangeUser(-20, 20)
    # # h_reclu.GetXaxis().SetTitle("M_{comp} - M_{true} [GeV]")
    # # # fit_1.Draw("SAMES")
    # # # fit_2.Draw("SAMES")
    # # # if file3: 
    # # h_3.Draw("HIST E sames")
    # # # fit_3.Draw("SAMES")

    gPad.Update()
    stat_2 = h_2.GetListOfFunctions().FindObject("stats")
    # stat_2.SetOptStat(0000)
    stat_2.SetX1NDC(0.75)
    stat_2.SetX2NDC(0.9)
    stat_2.SetY1NDC(0.6)
    stat_2.SetY2NDC(0.75)
    stat_2.SetTextColor(2)
    stat_2.SetBorderSize(2)
    # stat_2.SetTitle("162.3 GeV Fit")
    gPad.Modified()
    gPad.Update()
    stat_1 = h_1.GetListOfFunctions().FindObject("stats")
    stat_1.SetX1NDC(0.75)
    stat_1.SetX2NDC(0.9)
    stat_1.SetY1NDC(0.45)
    stat_1.SetY2NDC(0.6)
    stat_1.SetTextColor(4)
    stat_1.SetBorderSize(4)
    # stat_1.SetTitle("240 GeV Fit")
    gPad.Modified()
    gPad.Update()
    # # stat_3 = h_3.GetListOfFunctions().FindObject("stats")
    # # stat_3.SetX1NDC(0.75)
    # # stat_3.SetX2NDC(0.9)
    # # stat_3.SetY1NDC(0.30)
    # # stat_3.SetY2NDC(0.45)
    # # #stat_3.SetTitle("240 GeV Fit")
    # # gPad.Modified()
    # # gPad.Update()

    mylegend = TLegend(0.15, 0.7, 0.4, 0.85)
    mylegend.SetFillColor(0)
    mylegend.SetBorderSize(2)
    mylegend.SetTextSize(0.02)
    mylegend.AddEntry(h_1, "good jets pairing", "l")
    mylegend.AddEntry(h_2, "wrong jets pairing", "l")
    # mylegend.AddEntry(h_gen2, "gen jets without cuts (curr.)", "l")
    # mylegend.AddEntry(h_reco2, "reco jets without cuts (curr.)", "l")
    mylegend.Draw()

    # # l = TLatex()
    # # l.SetTextSize(0.04)
    # # l.SetTextColor(16)
    # # l.DrawLatex(-18, 1500, "Preliminary results")
    # # l.DrawLatex(-18, 1900, "Without Detector")
    # # canvas_name.Update()

    raw_input("hit a key to exit")

    # write into the output file and close the file
    outfilename = "{}.root".format(outdir)
    outfile = TFile(outfilename, "UPDATE")
    canvas_name.Write("", TObject.kOverwrite)
    outfile.Write()
    outfile.Close()


def main():
    """Main function"""

    Ecm = 240
    mW = 80.385

    dire = "../plots/test/"

    outdir = dire + "superposition_good_bad_pairing_cone"

    file1 = dire + "test_cone_all_evt.root"
    print "Opening file: ", file1
    # file2 = dire + "corre_matrix_{}_{}_without_cone.root".format(Ecm, mW)
    # print "Opening file: ", file2

    overlap(outdir, file1)

if __name__ == '__main__':
    main()
