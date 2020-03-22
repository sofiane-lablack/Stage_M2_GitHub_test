//////////////////////////////////////////////////////////////////////////
//
// 'SPECIAL PDFS' RooFit tutorial macro #701
// 
// Unbinned maximum likelihood fit of an efficiency eff(x) function to 
// a dataset D(x,cut), where cut is a category encoding a selection, of which
// the efficiency as function of x should be described by eff(x)
//
// 07/2008 - Wouter Verkerke 
//
/////////////////////////////////////////////////////////////////////////

#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooConstVar.h"
#include "RooFormulaVar.h"
#include "RooProdPdf.h"
#include "RooEfficiency.h"
#include "RooPolynomial.h"
#include "RooCategory.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "RooPlot.h"
using namespace RooFit ;


void unbinned_fit() {

  int E = 240;
  int nEvts = 50;
  int mW = 80;

  std::string inDir = "../output/50K_aout/uncertaintyMatrix";

  std::string filename = inDir;
  filename += "/corre_matrix_";
  filename += std::to_string(E);
  filename += "_50K_M80.root";
  cout << "filename " << filename << endl;

  // Import data to fit, observable
  RooRealVar logBoost("log_boost","log_boost",-0.4, 0.4);
  RooRealVar theta("theta","theta",-0.005, 0.005);
  RooRealVar phi("phi","phi",-0.005, 0.005);

  RooDataSet* data = RooDataSet::read(filename.c_str(), RooArgSet(logBoost));

  // ----Beta Fit----
  // First Crystal ball definition
  RooRealVar mean1("mean1", "The mean of the Gaussian", 0, -0.001, 0.001);
  RooRealVar sigma1("sigma1", "The width of the Gaussian", 0., -0.0001, 0.0001);
  RooRealVar alpha1("alpha1", "The alpha of the Gaussian", 0.07, -1., 1.);
  RooRealVar n1("n1", "The power law of the Gaussian", 1., -2., 2.);

  RooCBShape crystalBall1("CB1","The Crystal Ball pdf", logBoost, mean1, sigma1, alpha1, n1);


  // Second Crystal ball definition
  RooRealVar mean2("mean2", "The mean of the Gaussian", 0, -0.0001, 0.0001);
  RooRealVar sigma2("sigma2", "The width of the Gaussian", 0., -0.001, 0.001);
  RooRealVar alpha2("alpha2", "The alpha of the Gaussian", -0.5, -2., 1.);
  RooRealVar n2("n2", "The power law of the Gaussian", 0.9, -1.5, 1.);

  RooCBShape crystalBall2("CB2","The Crystal Ball pdf", logBoost, mean2, sigma2, alpha2, n2);

  // Total PDF
  // RooRealVar NCB1("NCB1","The first crystalball signal events", 10., 0., 100000.);
  // RooRealVar NCB2("NCB2","The second crystalball signal events", 10., 0., 130000.);
  RooRealVar f("f", "f", 0., 1.) ;
  RooAddPdf totPDF("totPDF", "The total PDF", crystalBall1, crystalBall2, f);

  // Fit
  RooFitResult *logBoost_fit;
  // logBoost_fit = totPDF.fitTo(*data, Save());
  logBoost_fit = totPDF.fitTo(*data, Save());
  logBoost_fit->Print();

  // Check the fit results
  RooArgList list = logBoost_fit->floatParsFinal();
  for (Int_t i = 0; i < list.getSize(); i++) {

    RooRealVar* temp = (RooRealVar*)list.at(i);

    if ((temp->getVal() + 3.*temp->getError()) > temp->getMax()) {
       cout << "Parameter " << temp->GetName() << " exceeds range at 3 sigma!" << endl;
    }

    else if ((temp->getVal() - 3.*temp->getError()) < temp->getMin()) {
       cout << "Parameter " << temp->GetName() << " exceeds range at 3 sigma!" << endl;
    }
  }

  // Plot the fitted data
  RooPlot* distrib = logBoost.frame(Title("Fitted logBoost"));
  data->plotOn(distrib);
  totPDF.plotOn(distrib);
  // data->statOn(distrib);
  // totPDF.paramOn(distrib, data);

   // distrib->Print("V");
   // auto dataHist  = (RooHist*) distrib->getHist("Fitted logBoost"); 
   // auto curve1 = (RooCurve*) distrib->getObject(1);  // 1 is index in the list of RooPlot items (see printout from distrib->Print("V")  
   // auto curve2 = (RooCurve*) distrib->getObject(2);
   // auto hresid1 =  dataHist->makePullHist(*curve1,true);
   // auto hresid2 =  dataHist->makePullHist(*curve2,true);

  // TCanvas* c_logBoost = new TCanvas("", "", 700, 500);
  // c_logBoost->cd();
  // // c_logBoost->SetLogy();
  // distrib->Draw();
  // c_logBoost->SaveAs("../output/plots/uncertainties_study/beta_uncertainty.pdf");

}