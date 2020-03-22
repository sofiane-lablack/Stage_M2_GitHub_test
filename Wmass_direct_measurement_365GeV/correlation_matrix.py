from ROOT import TFile, TH1F, TCanvas, TH2F
from math import log

import tools.histogram as histogram
from tools.tree_info import TreeInfo
from tools.association import object_association, object_association_semi

from particles.jets import Jet
from particles.particle import Particle

from analysis_tools.fit import fit


def gethists():
    """function to book all histograms and return as dictionary"""
    histdict = {}

    jet_type_list = ["", "_cone"]
    jets = ["gen", "reco"]

    # histdict["h_missing_energy"] = TH1F('h_missing_energy', 'Missing energy distribution';[GeV], 200, -100, 100)
    for jet_type in jet_type_list:
        histdict["h_uncert_rescaling{}".format(jet_type)] = TH1F('h_uncert_rescaling{}'.format(jet_type), 'Energy difference between parton energy and jet energy; E_{jet} / E_{parton} - 1 [GeV]', 100, -0.3, 0.3)
        histdict["h_uncert_theta{}".format(jet_type)] = TH1F('h_uncert_theta{}'.format(jet_type), 'Theta difference between reco{} and gen{} jets;theta_gen - theta [rad]'.format(jet_type, jet_type), 100, -0.04, 0.04)
        histdict["h_uncert_phi{}".format(jet_type)] = TH1F('h_uncert_phi{}'.format(jet_type), 'Phi difference between reco{} and gen{} jets;phi_gen - phi [rad]'.format(jet_type, jet_type), 100, -0.04, 0.04)
        histdict["h_uncert_log_boost{}".format(jet_type)] = TH1F('h_uncert_log_boost{}'.format(jet_type), 'Log(boost) difference between reco{} and gen{} jets;phi_gen - phi [rad]'.format(jet_type, jet_type), 100, -0.3, 0.5)

        histdict["h_corr_theta_phi{}".format(jet_type)] = TH2F('h_corr_phi_theta{}'.format(jet_type), 'Correlation between theta and phi;theta[rad];phi[rad]', 50, -3.18, 3.18, 50, -3.18, 3.18)
        histdict["h_corr_theta_alpha{}".format(jet_type)] = TH2F('h_corr_alpha_theta{}'.format(jet_type), 'Correlation between theta and the rescaling coefficient;theta[rad];alpha', 100, -3.18, 3.18, 100, -10, 10)
        histdict["h_corr_phi_alpha{}".format(jet_type)] = TH2F('h_corr_alpha_phi{}'.format(jet_type), 'Correlation between phi and the rescaling coefficient;phi[rad];alpha', 100, -3.18, 3.18, 100, -10, 10)
        histdict["h_corr_log_boost_alpha{}".format(jet_type)] = TH2F('h_corr_alpha_log_boost{}'.format(jet_type), 'Correlation between the logarithm of the boost and the rescaling coefficient;log(boost);alpha', 200, -2, 2, 200, -2, 3)
        histdict["h_corr_log_boost_theta{}".format(jet_type)] = TH2F('h_corr_theta_log_boost{}'.format(jet_type), 'Correlation between the logarithm of the boost and theta;log(boost);theta', 200, -2, 2, 200, -2, 2)
        histdict["h_corr_log_boost_phi{}".format(jet_type)] = TH2F('h_corr_phi_log_boost{}'.format(jet_type), 'Correlation between the logarithm of the boost and phi;log(boost);phi', 200, -2, 2, 200, -0.1, 0.1)

    return histdict


def coefficients(tree, histdict, reco_type=''):
    '''Computation of the rescaling coefficient, theta and phi uncertainty'''

    from_tree = TreeInfo()

    # Run on events
    for iev, evt in enumerate(tree):

        if iev%5000 == 0:
            print("Processing events {} over {}".format(iev, tree.GetEntries()))

        # Object from_tree to access the rootfile information
        from_tree.set_evt(evt)

	#value for normalisation
        histweight = from_tree.get_file_type()
        if (histweight == 1 or histweight == 2 or histweight == 3):
            print histweight
	
        #value distinguish ZZllll from ZZqqll from ZZqqqq in ZZall
        ZZqqll = 0
	ZZqqqq = 0
        if (histweight == 3 & from_tree.get_dim("quark") == 2):
	    ZZqqll = 1
        if (histweight == 3 & from_tree.get_dim("quark") == 4):
            ZZqqqq = 1
	#ecarte les evenements purement leptoniques du background ZZAll
        #if (histweight == 3 & from_tree.get_dim("quark") == 0):
        #    continue
        

        #if (histweight==0 or histweight ==3):
        #if from_tree.get_dim("reco_jet{}".format(reco_type)) != 4:
        #    continue
        #if(histweight==1 or histweight ==2):
        #    if from_tree.get_dim("reco_jet{}".format(reco_type)) != 2:
        #        continue

        #if from_tree.get_dim("quark") != 4:
        #    continue

        partons = [Particle() for i in range(from_tree.get_dim("quark"))]
	#print "range partons "+str(from_tree.get_dim("quark"))
        for iparton, parton in enumerate(partons):
            nparton = str("quark" + str(iparton + 1))
            #print "nparton "+str(nparton)
            parton.set_p4(from_tree.get_p4(nparton))

        gen_jets = [Jet()for i in range(from_tree.get_dim("gen_jet{}".format(reco_type)))]
        #print "gen_jets"+str(from_tree.get_dim("gen_jet{}".format(reco_type)))
        for ijet, jet in enumerate(gen_jets):
            #print "range ijet "+str(gen_jets)
            njet = str("gen_jet" + str(ijet + 1) + reco_type)
            #print njet
            if from_tree.get_p4(njet).E() < 0:
                continue
            jet.set_p4(from_tree.get_p4(njet))

        rec_jets = [Jet()for i in range(from_tree.get_dim("reco_jet{}".format(reco_type)))]
        for ijet, jet in enumerate(rec_jets):
            njet = str("reco_jet" + str(ijet + 1) + reco_type)

            if from_tree.get_p4(njet).E() < 0:
                continue
            jet.set_p4(from_tree.get_p4(njet))

        if not rec_jets:
	    print "No rec_jets"
            continue

	#print iev
        association(partons, rec_jets, gen_jets, histdict,histweight,ZZqqll,ZZqqqq)
	#histdict["h_uncert_rescaling"].Draw()
	#raw_input()


def association(partons, rjets, gjets, histdict,histweight,ZZqqll,ZZqqqq):
    '''Associations
    The rec_jets list copy is necessary because the rec_jets list will be empty at the end
    of the first association.'''

    sigma0 = 7.467  # ee WW qqqq
    sigma1 = 52.48  # ee qq
    sigma2 = 3.585  # ee WW qqll
    sigma3 = 1.360  # ee ZZ all

    weight1 = sigma1/sigma0 # norm ee qq
    weight2 = sigma2/sigma0 # norm WW qqll
    weight3 = sigma3/sigma0 # norm ZZ all
    if (histweight == 0):
        norm = 1
    if (histweight == 1):
        norm = weight1
    if (histweight == 2):
        norm = weight2
    if (histweight == 3):
        norm = weight3
    #print norm
    new_rjets = rjets[:]

    alpha_list = []

    if (histweight == 0 or ZZqqqq == 1):
        pj_asso = object_association(rjets, partons)


        # elem[0] = reco_jet, elem[1] = parton
        for iel, elem in enumerate(pj_asso):
            alpha = (elem[0].get_E() / elem[1].get_E()) - 1
            histdict["h_uncert_rescaling"].Fill(alpha,norm)
            #print alpha
            alpha_list.append(alpha)


    if (histweight == 1 or histweight == 2 or ZZqqll == 1):
        pj_asso = object_association_semi(rjets, partons)


        # elem[0] = reco_jet, elem[1] = parton
        for iel, elem in enumerate(pj_asso):
            alpha = (elem[0].get_E() / elem[1].get_E()) - 1
            histdict["h_uncert_rescaling"].Fill(alpha,norm)
            #print alpha
            alpha_list.append(alpha)

    if (histweight == 0 or ZZqqqq == 1):
        jj_asso = object_association(new_rjets, gjets)

        # elem[0] = reco_jet, elem[1] = gen_jet
        for iel, elem in enumerate(jj_asso):
            theta = elem[0].get_theta() - elem[1].get_theta()
            phi = elem[0].get_phi() - elem[1].get_phi()
            log_boost = log(elem[0].get_boost()) - log(elem[1].get_boost())

            histdict["h_uncert_theta"].Fill(theta,norm)
            histdict["h_uncert_phi"].Fill(phi,norm)
            histdict["h_uncert_log_boost"].Fill(log_boost,norm)

            histdict["h_corr_theta_phi"].Fill(theta, phi,norm)
            histdict["h_corr_log_boost_theta"].Fill(log_boost, theta,norm)
            histdict["h_corr_log_boost_phi"].Fill(log_boost, phi,norm)

            histdict["h_corr_theta_alpha"].Fill(theta, alpha_list[iel],norm)
            histdict["h_corr_phi_alpha"].Fill(phi, alpha_list[iel],norm)
            histdict["h_corr_log_boost_alpha"].Fill(log_boost, alpha_list[iel],norm)


    if (histweight == 1 or histweight == 2 or ZZqqll == 1):
        jj_asso = object_association_semi(new_rjets, gjets)

        # elem[0] = reco_jet, elem[1] = gen_jet
        for iel, elem in enumerate(jj_asso):
            theta = elem[0].get_theta() - elem[1].get_theta()
            phi = elem[0].get_phi() - elem[1].get_phi()
            log_boost = log(elem[0].get_boost()) - log(elem[1].get_boost())

            histdict["h_uncert_theta"].Fill(theta,norm)
            histdict["h_uncert_phi"].Fill(phi,norm)
            histdict["h_uncert_log_boost"].Fill(log_boost,norm)

            histdict["h_corr_theta_phi"].Fill(theta, phi,norm)
            histdict["h_corr_log_boost_theta"].Fill(log_boost, theta,norm)
            histdict["h_corr_log_boost_phi"].Fill(log_boost, phi,norm)

            histdict["h_corr_theta_alpha"].Fill(theta, alpha_list[iel],norm)
            histdict["h_corr_phi_alpha"].Fill(phi, alpha_list[iel],norm)
            histdict["h_corr_log_boost_alpha"].Fill(log_boost, alpha_list[iel],norm)


def print_corr_coef_into_file(histdict, outdir):
    fh = open("{}.txt".format(outdir), 'w')
    fh.write("Correlation theta/phi = {} \n".format(histdict["h_corr_theta_phi"].GetCorrelationFactor()))
    fh.write("Correlation boost/theta = {} \n".format(histdict["h_corr_log_boost_theta"].GetCorrelationFactor()))
    fh.write("Correlation boost/phi =  {} \n".format(histdict["h_corr_log_boost_phi"].GetCorrelationFactor()))
    fh.write("Correlation theta/alpha =  {} \n".format(histdict["h_corr_theta_alpha"].GetCorrelationFactor()))
    fh.write("Correlation phi/alpha =  {} \n".format(histdict["h_corr_phi_alpha"].GetCorrelationFactor()))
    fh.write("Correlation boost/alpha =  {} \n".format(histdict["h_corr_log_boost_alpha"].GetCorrelationFactor()))
    fh.close()


def main():
    ''' Main function, define paramters and process the correlation matrix definition'''

    # parameters to choose the study
    ecm = 240  #GeV
    m_w = 80.385  #GeV
    width = 2
    reco_type = '_pcut'
    fittedparameter = "log_boost"

    # input
    #filename = "../heppy_output/hadronic/ref_templates/ee_WW_qqqq_{}_M{}_width{}.root".format(ecm, str(m_w)[:2], width)
    filename = "/afs/cern.ch/user/s/slablack/fcc/signal_and_background_cuts_240GeV.root"
    rootfile = TFile(filename)
    tree = rootfile.Get("events")

    # Output
    #outdir = "./output/pythia_2018/hadronic/correlation_matrix/corre_matrix_{}_M{}_width{}{}".format(ecm, str(m_w)[:2], width, reco_type)
    outdir = "/afs/cern.ch/user/s/slablack/fcc/heppy_cuts/Fit_correlation_merged_sign_bkg_240GeV/fitted_merged_sign_bkg_240GeV"
    #histdict = gethists()
    #coefficients(tree, histdict)
    #histogram.save_root_file(histdict, outdir)

    #print_corr_coef_into_file (histdict, outdir)

    h_list = ["h_uncert_{}".format(fittedparameter)]
    for h_ in h_list:
        sum_sigma = fit(h_, outdir)


if __name__ == '__main__':
    main()
