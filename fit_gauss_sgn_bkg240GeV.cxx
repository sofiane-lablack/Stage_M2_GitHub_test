#include "TFile.h"
#include "TF1.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TH1D.h"
#include "fstream"
#include "iostream"
#include "TStyle.h"

#include "TLegend.h"

using namespace std;

int myMacro(){

        TCanvas* canvas = new TCanvas("canvas");
        TFile *file = new TFile("/home/lablack/Bureau/forSofiane/kinFit_sign_bkg/output_kinematic_5C_fit_sign_and_bkg_cut_240GeV.root");
        TH1D *histsgnbkg = (TH1D*) file->Get("h_mW1_cutProb");
//histsgnbkg->GetXaxis()->SetLimits(70,90);
histsgnbkg->GetXaxis()->SetRange(40,80);
        TF1* f2 = new TF1("f2","gaus",78,82);
        f2->SetParNames("Const","Mean","Sigma");
        histsgnbkg->Fit(f2,"R");


    //RooRealVar Gamma("#Gamma", "#Gamma", 2.094, 1.0, 3.0,"GeV/c^{2}");

//TF1* bw = new TF1("bw","A Breit-Wigner Distribution", 80.385, 80.385, 2.0);
/*
TF1 *bw = new TF1("bw","(1/(2*TMath::Pi()))*([0]/((x-[1])*(x-[1]))+[0]/4)",76,84);
bw->SetParameters(2.094,80.38);
 histsgnbkg->Fit("bw","+");
*/
	canvas->cd();
gStyle->SetOptStat(0);
histsgnbkg->GetXaxis()->SetTitle(" GeV ");
        histsgnbkg->Draw("hist");
//	bw->Draw("same");
	f2->Draw("same");

        Double_t Const = f2->GetParameter(0);
        Double_t Mean = f2->GetParameter(1);
        Double_t Sigma = f2->GetParameter(2);
        Double_t chi = f2->GetChisquare();
        //fdata << "Hist fit parameters: " << "Constant " << Const<< "    Mean " << Mean << "     Sigma " << Sigma  << "  chi2 " << chi  << endl;
cout << " const " << Const << " Mean " << Mean << " Sigma " << Sigma << " chi2 " << chi << endl;


        TCanvas* canvas4 = new TCanvas("canvas4");
        TFile *file4 = new TFile("/home/lablack/Bureau/forSofiane/kinFit_output/kinFit_WMass_240_4param_logBoost_5C_M80_width2_ISRTreatment.root");
        TH1D *histsgnref = (TH1D*) file4->Get("h_mW1_cutProb");
//histsgnbkg->GetXaxis()->SetLimits(70,90);
histsgnref->GetXaxis()->SetRange(40,80);
        TF1* f4 = new TF1("f4","gaus",78,82);
        f4->SetParNames("Const4","Mean4","Sigma4");
        histsgnref->Fit(f4,"R");

	canvas4->cd();
gStyle->SetOptStat(0);
histsgnref->GetXaxis()->SetTitle(" GeV ");
	histsgnref->Draw("hist");
	f4->Draw("same");
	
        Double_t Const4 = f4->GetParameter(0);
        Double_t Mean4 = f4->GetParameter(1);
        Double_t Sigma4 = f4->GetParameter(2);
        Double_t chi4 = f4->GetChisquare();
cout << " const4 " << Const4 << " Mean4 " << Mean4 << " Sigma4 " << Sigma4 << " chi2 4 " << chi4 << endl;


return 0;
}
