from math import log
from ROOT import TFile, TH1F, TH2F

import tools.histogram as histogram
from tools.tree_info import TreeInfo
from tools.association import object_association

from particles.jets import Jet
from particles.particle import Particle

from analysis_tools.fit import fit


def gethists():
    """function to book all histograms and return as dictionary"""
    histdict = {}

    histdict["h_uncert_energy"] = TH1F('h_uncert_energy', 'Energy difference between reco and gen lepton; E_gen - E_reco [GeV]', 100, -1, 1)


    histdict["h_uncert_rescaling"] = TH1F('h_uncert_rescaling', 'Energy difference between parton energy and jet energy; E_{jet} / E_{parton} - 1 [GeV]', 100, -0.2, 0.2)
    histdict["h_uncert_theta"] = TH1F('h_uncert_theta', 'Theta difference between reco and gen jet;theta_gen - theta_reco [rad]', 200, -0.1, 0.1)
    histdict["h_uncert_phi"] = TH1F('h_uncert_phi', 'Phi difference between reco and gen jet;phi_gen - phi_reco [rad]', 100, -0.1, 0.1)
    histdict["h_uncert_log_boost"] = TH1F('h_uncert_log_boost', 'log(boost) difference between gen and reco jet', 100, -6, 0)

    histdict["h_corr_theta_alpha"] = TH2F('h_corr_alpha_theta', 'Correlation between theta and the rescaling coefficient;theta[rad];alpha', 120, -3, 3, 200, -1, 3)
    histdict["h_corr_phi_alpha"] = TH2F('h_corr_alpha_phi', 'Correlation between phi and the rescaling coefficient;phi[rad];alpha', 60, -3, 3, 200, -1, 3)
    histdict["h_corr_theta_phi"] = TH2F('h_corr_phi_theta', 'Correlation between theta and phi jet;theta[rad];phi[rad]', 60, -3, 3, 120, -6, 6)
    histdict["h_corr_log_boost_alpha"] = TH2F('h_corr_alpha_log_boost', 'Correlation between the logarithm of the boost and the rescaling coefficient;log(boost);alpha', 200, -2, 2, 200, -2, 3)
    histdict["h_corr_log_boost_theta"] = TH2F('h_corr_theta_log_boost', 'Correlation between the logarithm of the boost and theta;log(boost);theta', 200, -2, 2, 200, -2, 2)
    histdict["h_corr_log_boost_phi"] = TH2F('h_corr_phi_log_boost', 'Correlation between the logarithm of the boost and phi;log(boost);phi', 200, -2, 2, 200, -10, 10)

    return histdict


def coefficients(tree, histdict):
    '''Computation of the rescaling coefficient, beta, theta and phi uncertainties'''

    from_tree = TreeInfo()

    # Run on events
    for iev, evt in enumerate(tree):

        if iev%5000 == 0:
            print("Processing events {} over {}".format(iev, tree.GetEntries()))

        # Object from_tree to access the rootfile information
        from_tree.set_evt(evt)

        if from_tree.get_dim("reco_jet") != 2:
            continue
        if from_tree.get_dim("quark") != 2:
            continue
        if from_tree.get_pdgid("reco_lepton") < -90:
            continue

        # if evt.gen_jet2_theta < -1. or evt.gen_jet2_theta > 1.:
        #     continue

        ######### Leptonic part
        g_lepton = Particle(from_tree.get_p4("gen_lepton"))
        r_lepton = Particle(from_tree.get_p4("reco_lepton"))
        if not r_lepton:
            continue

        histdict["h_uncert_energy"].Fill(r_lepton.get_E() - g_lepton.get_E())

        ######## Hadronic part
        partons = [Particle() for i in range(from_tree.get_dim("quark"))]
        for iparton, parton in enumerate(partons):
            nparton = str("quark" + str(iparton + 1))
            parton.set_p4(from_tree.get_p4(nparton))

        gen_jets = [Jet()for i in range(from_tree.get_dim("gen_jet"))]
        for ijet, jet in enumerate(gen_jets):
            njet = str("gen_jet" + str(ijet + 1))
            jet.set_p4(from_tree.get_p4(njet))

        rec_jets = [Jet()for i in range(from_tree.get_dim("reco_jet"))]
        for ijet, jet in enumerate(rec_jets):
            njet = str("reco_jet" + str(ijet + 1))
            jet.set_p4(from_tree.get_p4(njet))

        if not rec_jets:
            continue

        association(partons, rec_jets, gen_jets, histdict)


def association(partons, rjets, gjets, histdict):
    '''Associations
    The rec_jets list copy is necessary because the rec_jets list will be empty at the end
    of the first association.'''

    new_rjets = rjets[:]
    new_partons = partons[:]
    pj_asso = object_association(rjets, partons)

    alpha_list = []

    for iel, elem in enumerate(pj_asso):
        alpha = (elem[0].get_E() / elem[1].get_E()) - 1
        histdict["h_uncert_rescaling"].Fill(alpha)
        alpha_list.append(alpha)

    jj_asso = object_association(new_rjets, new_partons)

    for iel, elem in enumerate(jj_asso):
        theta = elem[0].get_theta() - elem[1].get_theta()
        phi = elem[0].get_phi() - elem[1].get_phi()
        log_boost = log(elem[0].get_boost()) - log(elem[1].get_boost())

        histdict["h_uncert_theta"].Fill(theta)
        histdict["h_uncert_phi"].Fill(phi)
        histdict["h_uncert_log_boost"].Fill(log_boost)

        histdict["h_corr_theta_phi"].Fill(theta, phi)
        histdict["h_corr_log_boost_theta"].Fill(log_boost, theta)
        histdict["h_corr_log_boost_phi"].Fill(log_boost, phi)

        histdict["h_corr_theta_alpha"].Fill(theta, alpha_list[iel])
        histdict["h_corr_phi_alpha"].Fill(phi, alpha_list[iel])
        histdict["h_corr_log_boost_alpha"].Fill(log_boost, alpha_list[iel])


def print_corr_coef_into_file(histdict, outdir):
    fh = open("{}.txt".format(outdir), "w")
    fh.write("Correlation theta/phi = {} \n".format(histdict["h_corr_theta_phi"].GetCorrelationFactor()))
    fh.write("Correlation boost/theta = {} \n".format(histdict["h_corr_log_boost_theta"].GetCorrelationFactor()))
    fh.write("Correlation boost/phi =  {} \n".format(histdict["h_corr_log_boost_phi"].GetCorrelationFactor()))
    fh.write("Correlation theta/alpha =  {} \n".format(histdict["h_corr_theta_alpha"].GetCorrelationFactor()))
    fh.write("Correlation phi/alpha =  {} \n".format(histdict["h_corr_phi_alpha"].GetCorrelationFactor()))
    fh.write("Correlation boost alpha =  {} \n".format(histdict["h_corr_log_boost_alpha"].GetCorrelationFactor()))
    fh.close()


def main():
    ''' Main function, define parameters and process the correlation matrix definition'''

    # parameters to choose the study
    ecm = 365  #GeV
    m_w = 80  #GeV
    nevt = 50 #K
    width = 2

    ###### Input
    filename = "../heppy_output/pythia_2018/semi-leptonic/onlyMuons/ref_templates/ee_WW_qqll_{}_{}K_M{}_width{}.root".format(ecm, nevt, m_w, width)
    rootfile = TFile(filename)
    tree = rootfile.Get("events")

    ###### Output
    outdir = "./output/pythia_2018/semi-leptonic/ref_templates/correlation_matrix/corre_matrix_{}_{}K_M{}_width{}".format(ecm, nevt, m_w, width)

    # # Distributions
    # histdict = gethists()
    # coefficients(tree, histdict)
    # histogram.save_root_file(histdict, outdir)
    # print_corr_coef_into_file(histdict, outdir)

    # Fit
    h_list = ["h_uncert_log_boost"]
    for h_ in h_list:
        fit(h_, outdir)


if __name__ == '__main__':
    main()
