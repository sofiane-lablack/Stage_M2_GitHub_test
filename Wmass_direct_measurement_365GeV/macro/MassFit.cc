/** \macro MassFit.cc */


using namespace std;
using namespace RooFit;


void MassFit(const char* plotOpt = "NEU") {

  double Ecm = 162.6;
  string study = "4C";


  // Define input Root file
  std::string inDir = "./output/testHadronicChannel/recoLevel/woCR/reco";

  std::ostringstream energy;
  energy << Ecm;
  std::string ecm = energy.str();

  std::string filename;
  if (study == "direct" || study == "simple_rescaling") {
    filename = inDir;
    filename += "/W_mass_";
    filename += ecm;
    filename += "_50K_M80_woCR_";
    filename += study;
    filename += ".root";
  }
  else {
    filename = "../kinematic_fit/";
    filename += inDir;
    filename += "/kinFit_WMass_";
    filename += ecm;
    filename += "_4param_logBoost_";
    filename += study;
    filename += "_M80_woCR.root";
  }

  cout << "filename " << filename << endl;

  TFile *f= new TFile(filename.c_str(), "update");
  char *myHist = new char[105];
  int ihist = 0;

  TH1D *h_myHist[2];
  h_myHist[ihist] = (TH1D*) f->Get("h_mW1");
  ihist = ihist + 1;
  h_myHist[ihist] = (TH1D*) f->Get("h_mW2");
  ihist = ihist + 1;

  cout << "start loop over histos" << endl;

  // Loop over all histograms
  for (int ih = 1; ih < 2; ih++) {

    std::ostringstream histo_nb;
    histo_nb << ih +1;
    std::string histo = histo_nb.str();

    Float_t massMin(40), massMax(120);
    RooRealVar mass("mass", "M(e^{+}e^{-})", massMin, massMax, "GeV/c^{2}");
    Int_t nBins(120);

    // Gaussian
    RooRealVar  sig("#sigma_{G}", "Core Width", 17., 5., 35.,"GeV/c^{2}");

    // Parameters for Crystal Ball Lineshape 
    RooRealVar  m0("#Delta m_{0}", "Bias", 0.61, -3., 3., "GeV/c^{2}");
    RooRealVar  sigma("#sigma_{CB}", "Width", 0.84, 0., 5.0, "GeV/c^{2}");
    RooRealVar  cut("#alpha", "Cut", -0.2, -5., 0.);
    RooRealVar  power("n", "Power", 10, 5., 10.0);
    // cut.setConstant();
    // power.setConstant();

    // Parameters or Breit-Wigner Distribution
    RooRealVar  mRes("M_{W}", "W mass", 80.379, 75.0, 85.0, "GeV/c^{2}");
    RooRealVar  Gamma("#Gamma", "#Gamma", 2.085, 2.0, 3.0, "GeV/c^{2}");
    mRes.setConstant();
    Gamma.setConstant();


    //  Introduce a resolution model
    RooGaussian    resG("resG",   "A  Gaussian Lineshape",     mass, m0, sig);
    RooCBShape     resCB("resCB", "A  Crystal Ball Lineshape", mass, m0, sigma, cut, power);
    RooRealVar     fracG("f_{G}",  "Gaussian Fraction",        0.0,0.0,1.0);
    RooAddPdf      res("res",     "Resolution Model",          resG, resCB, fracG);

    //  Breit-Wigner Lineshape 
    RooBreitWigner bw("bw","A Breit-Wigner Distribution", mass, mRes, Gamma);

    //  Convolution p.d.f. using numeric convolution operator based on Fourier Transforms
    RooFFTConvPdf bw_res("bw_res","Convolution", mass, bw, res);

    //  Background  p.d.f.
    RooRealVar  bgtau("a_{BG}", "Backgroung Shape", -0.1, -1.0, 0.0, "1/GeV/c^{2}");
    RooExponential bg("bg", "Backgroung Distribution", mass, bgtau);

    // Fit Model
    float nentries, nsigmin, nsigmean, nsigmax, nbkgmean, nbkgmax;

    nentries = h_myHist[ih]->GetEntries();
    cout << "nentries = " << nentries<< endl;

    nsigmin = 0.5 * nentries;
    nsigmean = 1.0 * nentries;
    nsigmax = 1.05 * nentries;
    nbkgmean = 0.01 * nentries;
    nbkgmax = 0.1 * nentries;

    RooRealVar  nsig("N_{S}", "#signal events", nsigmean, nsigmin, nsigmax); // temporary
    RooRealVar  nbkg("N_{B}", "#background events", nbkgmean, 0, nbkgmax); // temporary
    RooAddPdf   model("model", "Di-photon mass model", RooArgList(bw_res, bg), RooArgList(nsig, nbkg));// temporary

    // Create a datahist that imports contents of all TH1
    std::string c_name = "c_fit_m ";
    c_name += histo;
    c_name += "_";
    c_name += ecm;
    c_name += "_";
    c_name += study;

    TCanvas* c_mass_fit = new TCanvas(c_name.c_str(), "Fit", 700, 500);
    c_mass_fit->cd();

    RooDataHist data("data","data",mass,Import(*h_myHist[ih]));
    TStopwatch t;
    t.Start();
    RooFitResult* result = model.fitTo(data, FitOptions("mhr"), Optimize(0), Timer(1));
    t.Print();

    RooPlot* plot = mass.frame(Range(massMin, massMax), Bins(nBins));
    data.plotOn(plot, DrawOption("h"));
    model.plotOn(plot);
    model.paramOn(plot, Layout(0.6, 0.90, 0.85), Format(plotOpt,AutoPrecision(2)), Parameters(RooArgSet(m0, sigma, nsig, nbkg, cut, power, Gamma, mRes)), ShowConstants(kTRUE));
    model.plotOn(plot, Components("bg"), LineStyle(kDashed), LineColor(kRed));

    result->Print();

    RooArgSet* model_params2 = model.getParameters(data);
    model_params2->Print("v");

    auto m = m0.getVal();
    auto s = sigma.getVal();
    cout << "m = " << m << " s = " << s <<endl;

    plot->Draw();
    plot->Write();
    cout << " ih = " << ih << endl;


     // write into an output file and close the file
    std::string output_filename = inDir;
    output_filename += "/fit/fit_mass_";
    output_filename += study;
    output_filename += ".root";

    TFile* outfile = new TFile(output_filename.c_str(), "UPDATE");
    c_mass_fit->Write("", TObject::kOverwrite);
    outfile->Write();
    outfile->Close();

  }

  cout << "ihist = " << ihist << endl;
}
