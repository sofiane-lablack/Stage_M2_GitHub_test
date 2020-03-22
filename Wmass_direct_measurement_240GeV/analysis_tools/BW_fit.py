''' Macro to fit with a convolution of Breit-Wigner and crystal ball'''

from ROOT import TFile, TCanvas, gDirectory, TObject
from ROOT import RooFit, RooAddPdf, RooRealVar, RooBreitWigner, RooGaussian, RooCBShape
from ROOT import RooDataHist, RooArgList, RooFFTConvPdf, RooArgSet, RooExponential


def bw_fit(ecm, infile, outdir, reconstruction):
    """Breit-Wigner fit of the Mw distribution"""

    file_ = TFile(infile,"r")
    file_.cd()

    mass_ = 'h_mW2'
    h_mass = gDirectory.Get(mass_)
    scale = h_mass.GetXaxis().GetBinWidth(1)/(h_mass.Integral("width"))
    h_mass.Scale(scale)

    mass_min = 40
    mass_max = 120

    mass = RooRealVar("Dijet mass", "Dijet mass", mass_min, mass_max, "GeV")

    # parameters for gaussian function
    gaus_sig = RooRealVar("#sigma_{G}", "Core Width", 1., 0.5, 10., "GeV")
    # gaus_sig.setConstant()

    # parameters for Crystall Ball distribution
    m_ = RooRealVar("#Delta m", "Bias", 0., -3., 3., "GeV")
    sigma = RooRealVar("#sigma", "Width", 1.7, 0., 10., "GeV")
    alpha = RooRealVar("#alpha", "Cut", -0.15, -5., 0.)
    n = RooRealVar("n", "Power", 2.4, 0.5, 10.)
    alpha.setConstant()
    n.setConstant()

    # Parameters for Breit-Wigner distribution
    m_res = RooRealVar("M_{W}", "W boson mass", 80.385, 80.0, 81.0, "GeV")
    width = RooRealVar("#Gamma", "W width", 2.085, 1.5, 2.5, "GeV")
    m_res.setConstant()
    width.setConstant()

    # Cristall-Ball lineshape
    resG = RooGaussian("resG", "Gaussian distribution", mass, m_, gaus_sig)
    resCB = RooCBShape("resCB", "Crystal Ball distribution", mass, m_, sigma, alpha, n)
    fracG = RooRealVar("f_{G}", "Gaussian Fraction", 0., 0., 1.)
    res = RooAddPdf("res", "Resolution Model", resG, resCB, fracG)

    # Breit-wigner lineshape
    bw = RooBreitWigner("bw", "Breit-Wigner distribution", mass, m_res, width)

    # Convolution
    bw_CB_conv = RooFFTConvPdf("bw_CB_conv", "Convolution", mass, bw, res)


    # Background p.d.f
    bgtau = RooRealVar("a_{BG}", "Backgroung Shape", -0.15, -1.0, 0.0, "1/GeV/c^{2}")
    bg = RooExponential("bg", "Background distribution", mass, bgtau)

    # Fit model
    nentries = h_mass.GetEntries()
    nsigmin = 0.5 * nentries
    nsigmean = 1.0 * nentries
    nsigmax = 1.05 * nentries
    nbkgmean = 0.01 * nentries
    nbkgmax = 0.1 * nentries

    nsig = RooRealVar("N_S", "#signal events", nsigmean, nsigmin, nsigmax)
    nbkg = RooRealVar("N_B", "#background events", nbkgmean, 0, nbkgmax)
    model = RooAddPdf("model", "W mass fit", RooArgList(bw_CB_conv, bg), RooArgList(nsig, nbkg))

    ###### FIT
    c_name = "c_ " + mass_ + "_" + str(ecm) + "_" + reconstruction + "_fit"
    c_mass_fit = TCanvas(c_name, 'Fit of the reconstructed mass distribution with a convolution of Breit-Wigner and Crystal-Ball', 700, 500)
    c_mass_fit.cd()

    data = RooDataHist("data", "data", RooArgList(mass), h_mass)
    frame = mass.frame()
    data.plotOn(frame)
    model.fitTo(data, RooFit.Optimize(0))

    model.plotOn(frame)
    model.paramOn(frame, RooFit.Layout(0.6, 0.90, 0.85))
    frame.Draw()

    # norm = h_mass.Integral()/bw_CB_conv.createIntegral(RooArgSet(mass)).getValV()
    # m = m_.getValV()*norm
    # s = sigma.getValV()*norm

    m = m_.getVal()
    s = sigma.getVal()

    print("\n\n----------------------------------------------")
    print("     Fit results :")
    print(" Bias to apply on mW : {} GeV".format(m))
    print(" Mw = {}  +/- {} GeV".format((m + 80.385), s))
    print("--------------------------------------------------")

    raw_input("")
    c_mass_fit.Print("{}fit/fit_{}_{}_{}.pdf".format(outdir, mass_, ecm, reconstruction))

    # write into an output file and close the file
    outfilename = "{}fit/fit_{}_{}.root".format(outdir, mass_, ecm)
    outfile = TFile(outfilename, "UPDATE")
    c_mass_fit.Write("", TObject.kOverwrite)
    outfile.Write()
    outfile.Close()




def main():
    '''Main function which can run the hadronic and the semi-leptonic decay. The study is selected
    at the beginning with the parameters. Nothing should be changed in the function'''

    # parameters to choose the study
    nevts = "50K"
    ecm = 240
    m_w = 80.385
    reconstruction = 'simple_rescaling'

    # Analysis
    outdir = "./output/testHadronicChannel/recoLevel/woCR/reco/"
    infile = outdir + "W_mass_{}_{}_M{}_woCR_{}.root".format(ecm, nevts, str(m_w)[:2], reconstruction)
    # infile = "../kinematic_fit/" + outdir + "kinFit_WMass_{}_4param_logBoost_5C_M{}_woCR.root".format(ecm, str(m_w)[:2])


    bw_fit(ecm, infile, outdir, reconstruction)

if __name__ == '__main__':
    main()
