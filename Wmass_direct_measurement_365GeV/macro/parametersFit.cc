/** \macro MassFit.cc */


using namespace std;
using namespace RooFit;


void parametersFit(const char* plotOpt = "NEU") {

  double Ecm = 240;

  // Define input Root file
  std::string inDir = "../output/50K_aout/uncertaintyMatrix";

  std::ostringstream energy;
  energy << Ecm;
  std::string ecm = energy.str();

  std::string filename;
  filename = inDir;
  filename += "/corre_matrix_";
  filename += ecm;
  filename += "_50K_M80.root";
  cout << "filename " << filename << endl;

  TFile *f= new TFile(filename.c_str(), "update");
  char *myHist = new char[105];
  int ihist = 0;

  TH1D *h_myHist[4];
  h_myHist[ihist] = (TH1D*) f->Get("h_uncert_rescaling");
  ihist = ihist + 1;
  h_myHist[ihist] = (TH1D*) f->Get("h_uncert_boost");
  ihist = ihist + 1;
  h_myHist[ihist] = (TH1D*) f->Get("h_uncert_theta");
  ihist = ihist + 1;
  h_myHist[ihist] = (TH1D*) f->Get("h_uncert_phi");
  ihist = ihist + 1;

  cout << "start loop over histos" << endl;

  // Loop over all histograms
  for (int ih = 1; ih < 2; ih++) {

    std::ostringstream histo_nb;
    histo_nb << ih +1;
    std::string histo = histo_nb.str();

    // Float_t min = h_myHist[ih]->GetXaxis()->GetXmin();
    // Float_t max = h_myHist[ih]->GetXaxis()->GetXmax();
    Float_t min = -0.4;
    Float_t max = 0.2;

    Float_t nBins = h_myHist[ih]->GetSize();
    RooRealVar parameter("parameter", "Uncertainty on parameter", min, max, "GeV/c^{2}");

    // Parameters for the first Crystal Ball Lineshape
    RooRealVar  alpha1("#alpha_{1}", "Cut", -3.79, -5., 0.);
    RooRealVar  alpha2("#alpha_{2}", "Cut", 0.38, 0., 5.);

    RooRealVar  sigma1("#sigma_{CB, 1}", "Width", 0.0001, 0., 1.0, "GeV/c^{2}");
    RooRealVar  sigma2("#sigma_{CB, 2}", "Width", 0.084, 0., 1.0, "GeV/c^{2}");

    RooRealVar  m0("m_{0}", "Mean parameter", -0.037, -0.5, 0.5, "GeV/c^{2}");
    RooRealVar  n1("n_{1}", "Power", 3.46, 0., 6.);
    RooRealVar  n2("n_{2}", "Power", 0.91, 0., 6.);

    // Crystal ball distributions
    RooCBShape resCB1("resCB1", "A first Crystal Ball Lineshape", parameter, m0, sigma1, alpha1, n1);
    RooCBShape resCB2("resCB2", "A second Crystal Ball Lineshape", parameter, m0, sigma2, alpha2, n2);

    RooRealVar frac("f", "Fraction", 0.0,0.0,1.0);
    RooAddPdf  model("model", "Resolution Model", resCB1, resCB2, frac);

    // Create a datahist that imports contents of all TH1
    std::string c_name = "c_fit_ ";
    c_name += histo;
    c_name += "_";
    c_name += ecm;

    TCanvas* c_mass_fit = new TCanvas(c_name.c_str(), "Fit", 700, 500);
    c_mass_fit->cd();

    RooDataHist data("data", "data", parameter, Import(*h_myHist[ih]));
    TStopwatch t;
    t.Start();
    RooFitResult* result = model.fitTo(data, FitOptions("mhr"), Optimize(0), Timer(1));
    t.Print();

    RooPlot* plot = parameter.frame(Range(min, max), Bins(nBins));
    data.plotOn(plot, DrawOption("h"));
    model.plotOn(plot);
    model.paramOn(plot, Layout(0.6, 0.90, 0.85), Format(plotOpt,AutoPrecision(2)), Parameters(RooArgSet(m0, sigma1, sigma2, alpha1, alpha2, n1, n2)), ShowConstants(kTRUE));

    result->Print();

    RooArgSet* model_params2 = model.getParameters(data);
    model_params2->Print("v");

    plot->Draw();
    cout << " ih = " << ih << endl;

     // write into an output file and close the file
    std::string output_filename = inDir;
    output_filename += "fitted_parameters.root";

    TFile* outfile = new TFile(output_filename.c_str(), "UPDATE");
    c_mass_fit->Write("", TObject::kOverwrite);
    outfile->Write();
    outfile->Close();

  }

  cout << "ihist = " << ihist << endl;
}
