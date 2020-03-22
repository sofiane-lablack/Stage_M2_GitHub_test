#!/usr/bin/env python
from ROOT import TFile, TH1F, TH2F, TLorentzVector, TCanvas, TF1, TLine, TObject, gPad

import tools.histogram as histogram
from tools.tree_info import get_mis_p4, get_lepton_p4
import math

def gethists():
    """function to book all histograms and return as dictionary"""
    histdict = {}

    lept_type = ['elect', 'muon']

    for lept in lept_type:
        histdict["h_misE_{}".format(lept)] = TH1F('h_misE_{}'.format(lept), 'Gen/Reco missing energy comparison', 200, -70, 40)
        histdict["h_misPx_{}".format(lept)] = TH1F('h_misPx_{}'.format(lept), 'Gen/Reco missing Px comparison', 200, -40, 40)
        histdict["h_misPy_{}".format(lept)] = TH1F('h_misPy_{}'.format(lept), 'Gen/Reco missing Py comparison', 200, -40, 40)
        histdict["h_misPz_{}".format(lept)] = TH1F('h_misPz_{}'.format(lept), 'Gen/Reco missing Pz comparison', 200, -50, 50)
        histdict["h_misP_{}".format(lept)] = TH1F('h_misP_{}'.format(lept), 'Gen/Reco missing position comparison', 200, -30, 30)
        histdict["h_misM_{}".format(lept)] = TH1F("h_misM_{}".format(lept), 'Gen/Reco missing mass comparison', 200, -150, 50)
        histdict["h_leptE_{}".format(lept)] = TH1F("h_leptE_{}".format(lept), 'Gen/Reco lepton energy comparison', 200, -5, 5)
        histdict["h_leptTheta_{}".format(lept)] = TH1F("h_leptTheta_{}".format(lept), 'Gen theta lepton', 200, -5, 5)

    histdict["h_recoJetsAngle"] = TH1F("h_recoJetsAngle", 'Angle between the two reconstructed jets', 200, 0, 3.5)
    histdict["h_recoJetsTheta"] = TH1F("h_recoJetsTheta", 'Theta angles of the reconstructed jets', 200, -3.5, 3.5)
    histdict["h_recoJetEnergy"] = TH1F("h_recoJetEnergy", 'Energy of the reconstructed jets', 200, 0, 200)

    with_wo = ['FSR', 'woFSR']

    # for cut in with_wo:
    #     histdict["h_ISR_E{}".format(cut)] = TH1F("h_ISR_E{}".format(cut), 'ISR energy', 200, -0, 150)
    #     histdict["h_ISR_Theta{}".format(cut)] = TH1F("h_ISR_Theta{}".format(cut), 'ISR theta', 200, -1.6, 1.6)
    #     histdict["h_ISR_pz{}".format(cut)] = TH1F("h_ISR_pz{}".format(cut), 'ISR pz', 200, -10, 10)

        # histdict["h_ISR_Theta_vs_E{}".format(cut)] = TH2F("h_ISR_Theta_vs_E{}".format(cut), 'ISR theta versus energy', 750, 0, 150, 200, -1.7, 1.7)
        # histdict["h_FSR_Theta_vs_E{}".format(cut)] = TH2F("h_FSR_Theta_vs_E{}".format(cut), 'FSR theta versus energy', 750, 0, 150, 200, -1.7, 1.7)

    histdict["h_FSR_E"] = TH1F("h_FSR_E", 'FSR energy', 200, -1, 5)
    histdict["h_FSR_Theta"] = TH1F("h_FSR_Theta", 'FSR theta', 200, -1.6, 1.6)
    histdict["h_FSR_pz"] = TH1F("h_FSR_pz", 'FSR pz', 200, -10, 10)

    # histdict["h_FSR_E_electrons"] = TH1F("h_FSR_E_electrons", 'energy FSR emitted by electrons', 200, -1, 5)
    # histdict["h_FSR_Theta_electrons"] = TH1F("h_FSR_Theta_electrons", 'theta FSR emited by the electrons', 200, -1.6, 1.6)
    # histdict["h_FSR_pz_electrons"] = TH1F("h_FSR_pz_electrons", 'pz FSR emited by the electrons ', 200, -10, 10)

    # histdict["h_FSR_E_muons"] = TH1F("h_FSR_E_muons", 'energy FSR emitted by muons', 200, -1, 5)
    # histdict["h_FSR_Theta_muons"] = TH1F("h_FSR_Theta_muons", 'theta FSR emited by the muons', 200, -1.6, 1.6)
    # histdict["h_FSR_pz_muons"] = TH1F("h_FSR_pz_muons", 'pz FSR emited by the muons ', 200, -10, 10)

    histdict["h_FSR_lepton_angle_vs_E"] = TH2F("h_FSR_lepton_angle_vs_E", 'Solid angle between the FSR photon and the lepton', 150, -1, 10, 150, 0, 3.17)
    histdict["h_E_p_vs_E_FSR"] = TH2F("h_E_p_vs_E_FSRPhoton", "E/p ratio versus the FSR energy photon", 220, -1, 10, 220, 0.9998, 1.0002)


    histdict["h_nonFSR_lepton_angle_vs_E"] = TH2F("h_photons_lepton_angle_vs_E", 'Solid angle between the non-FSR photons and the lepton', 150, -1, 10, 150, 0, 3.17)
    histdict["h_E_p_vs_E_nonFSR"] = TH2F("h_E_p_vs_E_NonFSRPhoton", "E/p ratio versus the non-FSR energy photon", 220, -1, 10, 220, 0.9998, 1.0002)

    histdict["h_test"] = TH2F("h_test", "h_test", 150, -1, 10, 150, 0, 3.17)
    return histdict


def elementSelection(elem):
    return (x for x in elem if x != -99)



def mis_energy(tree, histdict):
    '''Read the tree and fill the histogram event per events'''

    count_ISR_evt = 0

    for iev, evt in enumerate(tree):

        # if evt.reco_lepton_size == 0:
        #     continue

        # ISR_evt_flag = False

        if iev%1000 == 0:
            print("Processing events {} on {} ".format(iev, tree.GetEntries()))

        # jet1_tlv = TLorentzVector(evt.reco_jet1_px, evt.reco_jet1_py, evt.reco_jet1_pz, evt.reco_jet1_e)
        # jet2_tlv = TLorentzVector(evt.reco_jet2_px, evt.reco_jet2_py, evt.reco_jet2_pz, evt.reco_jet2_e)


        # angle_jets = jet1_tlv.Angle(jet2_tlv.Vect())
        # histdict["h_recoJetsAngle"].Fill(angle_jets)
        # histdict["h_recoJetsTheta"].Fill(evt.reco_jet1_theta)
        # histdict["h_recoJetsTheta"].Fill(evt.reco_jet2_theta)
        # histdict["h_recoJetEnergy"].Fill(evt.reco_jet1_e)
        # histdict["h_recoJetEnergy"].Fill(evt.reco_jet2_e)


        lepton_tlv = TLorentzVector(evt.gen_lepton_px, evt.gen_lepton_py, evt.gen_lepton_pz, evt.gen_lepton_e)

        FSR_ph = zip(elementSelection(evt.fsr_e), elementSelection(evt.fsr_px),
                     elementSelection(evt.fsr_py), elementSelection(evt.fsr_pz))
        for e, px, py, pz in FSR_ph:
            FSR_ph = TLorentzVector(px, py, pz, e)
            p_FSR = FSR_ph.P()
            E_p_FSR = e/p_FSR

            histdict["h_E_p_vs_E_FSR"].Fill(e, E_p_FSR)

            angle = FSR_ph.Angle(lepton_tlv.Vect())
            if e >= 0.2:
                histdict["h_FSR_lepton_angle_vs_E"].Fill(e, angle)


        nonFSR_ph = zip(elementSelection(evt.nonFSRPh_e), elementSelection(evt.nonFSRPh_px),
                        elementSelection(evt.nonFSRPh_py), elementSelection(evt.nonFSRPh_pz))
        for e, px, py, pz in nonFSR_ph:
            nonFSR_ph = TLorentzVector(px, py, pz, e)
            p_nonFSR = nonFSR_ph.P()
            E_p_nonFSR = e/p_nonFSR

            histdict["h_E_p_vs_E_nonFSR"].Fill(e, E_p_nonFSR)

            angle = nonFSR_ph.Angle(lepton_tlv.Vect())
            if e >= 0.2 and angle > 0.02:
                histdict["h_nonFSR_lepton_angle_vs_E"].Fill(e, angle)


    #     # ISR study
    #     for en in elementSelection(evt.isr_e):
    #         histdict["h_ISR_E"].Fill(en)
    #     for theta in elementSelection(evt.isr_theta):
    #         histdict["h_ISR_Theta"].Fill(theta)
    #     for pz in elementSelection(evt.isr_pz):
    #         histdict["h_ISR_pz"].Fill(pz)

    #     for en, theta in zip(elementSelection(evt.isr_e), elementSelection(evt.isr_theta)):
    #         histdict["h_ISR_Theta_vs_E"].Fill(en, theta)

    #         if en >= 0.2 and abs(theta) <= 1.48:
    #             ISR_evt_flag = True
    #             histdict["h_ISR_E_cut"].Fill(en)
    #             histdict["h_ISR_Theta_cut"].Fill(theta)

    #     if ISR_evt_flag:
    #         count_ISR_evt += 1

    # print("Nombre ISR evt = ", count_ISR_evt)

def addCuts(histdict, outdir):

    c_2D = TCanvas('c_2D', 'ISR photons theta versus Energy', 700, 500)

    c_2D.cd(1)
    histdict["h_ISR_Theta_vs_E"].Draw("colz")


    f1 = TF1("cutThetaPos", "1.48", -1., 200)
    f1.SetLineStyle(7)
    f1.SetLineColor(2)
    f1.Draw("same")

    f2 = TF1("cutThetaNeg", "-1.48", -1., 200)
    f2.SetLineStyle(7)
    f2.SetLineColor(2)
    f2.Draw("same")

    # gPad.DrawFrame(0, -3.5, 150, 3.5)
    cutE = TLine(0.2, -3.5, 0.2, 3.5)
    cutE.SetLineColor(2)
    cutE.SetLineStyle(7)
    cutE.Draw("same")

    outfilename = "{}.root".format(outdir)
    outfile = TFile(outfilename, "UPDATE")
    c_2D.Write("", TObject.kOverwrite)
    outfile.Write()
    outfile.Close()

    # raw_input("hit a key to exit")

        # # FSR study
        # for en in elementSelection(evt.fsr_e):
        #     histdict["h_FSR_E"].Fill(en)
        # for theta in elementSelection(evt.fsr_theta):
        #     histdict["h_FSR_Theta"].Fill(theta)
        # for pz in elementSelection(evt.fsr_pz):
        #     histdict["h_FSR_pz"].Fill(pz)

        # for en, theta in zip(elementSelection(evt.fsr_e), elementSelection(evt.fsr_theta)):
        #     histdict["h_FSR_Theta_vs_E"].Fill(en, theta)



        # if abs(evt.gen_lepton_pdgid) == 11:
        #     for en in elementSelection(evt.isr_e):
        #         histdict["h_FSR_E_electrons"].Fill(en)
        #     for theta in elementSelection(evt.isr_theta):
        #         histdict["h_FSR_Theta_electrons"].Fill(theta)
        #     for pz in elementSelection(evt.isr_pz):
        #         histdict["h_FSR_pz_electrons"].Fill(pz)

        # if abs(evt.gen_lepton_pdgid) == 13:
        #     for en in elementSelection(evt.isr_e):
        #         histdict["h_FSR_E_muons"].Fill(en)
        #     for theta in elementSelection(evt.isr_theta):
        #         histdict["h_FSR_Theta_muons"].Fill(theta)
        #     for pz in elementSelection(evt.isr_pz):
        #         histdict["h_FSR_pz_muons"].Fill(pz)



        # gen_mis = get_mis_p4(evt, "gen")
        # rec_mis = get_mis_p4(evt, "reco")
        # gen_lept = get_lepton_p4(evt, "gen")
        # rec_lept = get_lepton_p4(evt, "reco")

        # if abs(evt.gen_lepton_pdgid) == 11:
        #     histdict["h_misE_elect"].Fill(gen_mis.E() - rec_mis.E())
        #     histdict["h_misPx_elect"].Fill(gen_mis.X() - rec_mis.X())
        #     histdict["h_misPy_elect"].Fill(gen_mis.Y() - rec_mis.Y())
        #     histdict["h_misPz_elect"].Fill(gen_mis.Z() - rec_mis.Z())
        #     histdict["h_misP_elect"].Fill(gen_mis.P() - rec_mis.P())
        #     histdict["h_misM_elect"].Fill(abs(gen_mis.M()) - abs(rec_mis.M()))
        #     histdict["h_leptE_elect"].Fill(gen_lept.E() - rec_lept.E())
        #     histdict["h_leptTheta_elect"].Fill(math.pi/2 - gen_lept.Theta())


        # if abs(evt.gen_lepton_pdgid) == 13:
        #     histdict["h_misE_muon"].Fill(gen_mis.E() - rec_mis.E())
        #     histdict["h_misPx_muon"].Fill(gen_mis.X() - rec_mis.X())
        #     histdict["h_misPy_muon"].Fill(gen_mis.Y() - rec_mis.Y())
        #     histdict["h_misPz_muon"].Fill(gen_mis.Z() - rec_mis.Z())
        #     histdict["h_misP_muon"].Fill(gen_mis.P() - rec_mis.P())
        #     histdict["h_misM_muon"].Fill(abs(gen_mis.M()) - abs(rec_mis.M()))
        #     histdict["h_leptE_muon"].Fill(gen_lept.E() - rec_lept.E())
        #     histdict["h_leptTheta_muon"].Fill(math.pi/2 - gen_lept.Theta())



def main():
    '''Main function . The study is selected at the beginning with the parameters.
    Nothing should be changed in functions '''

    # parameters to choose the study
    nevts = "50K"
    ecm = 365
    m_w = 80.385


    # Analysis
    filename = "../heppy_output/semi-leptonic/ee_WW_qqll_{}_{}_M{}_FSR_nonFSR.root".format(ecm, nevts, str(m_w)[:2])
    rootfile = TFile(filename)
    tree = rootfile.Get("events")


    # output file
    outdir = "./output/plots/semi-leptonic/ISR_FSR_study/{}GeV_FSR_nonFSR".format(ecm)
    # histogram.create_output_dir(outdir)

    # Function call
    histdict = gethists()
    mis_energy(tree, histdict)

    histogram.save_root_file(histdict, outdir)

    # addCuts(histdict, outdir)

if __name__ == '__main__':
    main()
