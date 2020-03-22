from ROOT import TH1F, TCanvas, TLegend, TLatex


def gen_reco_particles():

    count_event = -1
    data = []

    with open('./particles_init.txt', 'r') as f:

        for line in f:
            if not line.strip():
                count_event +=1
            else:
                if count_event < 100:
                    row = line.split()
                    data.append(row)

    h_gen_E = TH1F( 'hgen_E', 'Energy distribution of the gen particles', 20, 0, 2)
    h_reco_E = TH1F( 'hreco_E', 'Energy distribution of the reco particles', 20, 0, 2)
    h_sim_E = TH1F( 'hsim_E', 'Energy distribution of the sim particles', 20, 0, 2)
    h_gen_pt = TH1F( 'hgen_pt', 'Pt distribution of the gen particles', 20, 0, 2)
    h_reco_pt = TH1F( 'hreco_pt', 'Pt distribution of the reco particles', 20, 0, 2)
    h_sim_pt = TH1F( 'hsim_pt', 'Pt distribution of the sim particles', 20, 0, 2)

    for i, line in enumerate(data) :
            h_gen_E.Fill(float(data[i][0]))
            h_gen_pt.Fill(float(data[i][2]))
            if (float(data[i][1]) != 10000):
                h_reco_E.Fill(float(data[i][1]))
            if (float(data[i][3]) != 10000):
                h_reco_pt.Fill(float(data[i][3]))
            if (float(data[i][4]) != 10000):
                h_sim_E.Fill(float(data[i][4]))
            if (float(data[i][5]) != 10000):
                h_sim_pt.Fill(float(data[i][5]))

    c_gen_reco_E = TCanvas('c_gen_reco_E', 'Energy distribution of gen and reco particles', 900, 700)
    c_gen_reco_E.cd()
    h_gen_E.SetStats(False)
    h_gen_E.Draw()
    h_reco_E.SetStats(False)
    h_reco_E.SetLineColor(2)
    h_reco_E.Draw("SAME")
    # h_sim_E.SetStats(False)
    # h_sim_E.SetLineColor(8)
    # h_sim_E.Draw("SAME")

    mylegend = TLegend(0.65, 0.75, 0.9, 0.9)
    mylegend.SetTextSize(0.03)
    mylegend.AddEntry(h_gen_E, "gen particles", "l")
    mylegend.AddEntry(h_reco_E, "reco particles", "l")
    mylegend.Draw()

    l = TLatex()
    l.SetTextSize(0.03)
    l.DrawLatex(0.4, 35, "100 events")
    l.DrawLatex(0.4, 25, "Silicon Based Detector")
    c_gen_reco_E.Update()

    raw_input("hit a key to exit")


    # c_gen_reco_pt = TCanvas('c_gen_reco_pt', 'Pt distribution of gen and reco particles', 900, 700)
    # c_gen_reco_pt.cd()
    # h_gen_pt.SetStats(False)
    # h_gen_pt.Draw()
    # h_reco_pt.SetStats(False)
    # h_reco_pt.SetLineColor(2)
    # h_reco_pt.Draw("SAME")
    # # h_sim_pt.SetStats(False)
    # # h_sim_pt.SetLineColor(8)
    # # h_sim_pt.Draw("SAME")

    # mylegend = TLegend(0.65, 0.75, 0.9, 0.9)
    # mylegend.SetTextSize(0.03)
    # mylegend.AddEntry(h_gen_pt, "gen particles", "l")
    # mylegend.AddEntry(h_reco_pt, "reco particles", "l")
    # # mylegend.AddEntry(h_sim_pt, "sim particles", "l")
    # mylegend.Draw()

    # l = TLatex()
    # l.SetTextSize(0.03)
    # l.DrawLatex(0.4, 65, "100 events")
    # l.DrawLatex(0.4, 55, "Silicon Based Detector")
    # # l.DrawLatex(10, 5.5, "Reco particles : {}".format(len(reco_particles)))
    # c_gen_reco_pt.Update()

    # raw_input("hit a key to exit")

    c_gen_reco_E.Print("../plots/gen_reco_particles/E_gen_reco_particles_100evts.pdf")
    # c_gen_reco_pt.Print("../plots/gen_reco_particles/pt_gen_reco_particles_100evts_newCuts.pdf")

if __name__ == '__main__':
    gen_reco_particles()