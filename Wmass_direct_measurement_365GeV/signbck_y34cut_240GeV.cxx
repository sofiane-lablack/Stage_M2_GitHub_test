 #include <stdlib.h>
 #include <string.h>
 #include <stdio.h>
 #include <ctype.h>
 #include <sstream>
 #include <cmath>
 

 #include "TCanvas.h"
 #include "TH1.h"
 #include "TBrowser.h"

#include "TFile.h"
#include "TF1.h"
#include "TGraph.h"
#include "TLegend.h"


 using namespace std;

 int signbck240()
 {

// 	double NbEntries = hist1->GetXaxis()->GetXmax();
 	double sigma0 = 7.467; //ee WW qqqq
 	double sigma1 = 52.48; //ee qq
 	double sigma3 = 0.6343; // ee ZZqqll
 	double sigma4 = 0.6325; // ee ZZ qqqq
 	double sigma5 = 3.585; // ee WW qqll
 	double sigma6 = 0.0548; // ee ZH qqqq
 	double sigma7 = 0.00790; // ee ZH llqq
 	double sigma8 = 0.00572; // ee ZH qqll
 	double norm1 = sigma0 / sigma1;
 	double norm3 = sigma0 / (2 *sigma3);
 	double norm4 = sigma0 / sigma4;
 	double norm5 = sigma0 / (2 *sigma5);
 	double norm6 = sigma0 / sigma6;
 	double norm7 = sigma0 / sigma7;
 	double norm8 = sigma0 / sigma8;


//////////////////////////////////////////   MW1 Norm  /////////////////////////////////////

 	TFile *fnorm1 = new TFile("/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_240GeV/output_ee_WW_qqqq_240_y34cut_50K_ee_kt_SM.root");
 	TH1D *h1norm = (TH1D *) fnorm1->Get("h_mW1");
 	h1norm->SetLineColor(2);
 	h1norm->SetLineWidth(2);

 	TFile *fnorm2 = new TFile("/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_240GeV/output_ee_qq_240_y34cut_Bkg_50K_ee_kt_SM.root");
 	TH1D *h2norm = (TH1D *) fnorm2->Get("h_mW1");
 	h2norm->SetLineColor(6);
 	h2norm->SetLineWidth(2);
 	h2norm->Scale(1/norm1);

 	TFile *fnorm4 = new TFile("/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_240GeV/output_ee_ZZ_qqllBkg_240_y34cut_50K_ee_kt_SM.root");
 	TH1D *h4norm = (TH1D *) fnorm4->Get("h_mW1");
 	h4norm->SetLineColor(7);
 	h4norm->SetLineWidth(2);
 	h4norm->Scale(1/norm3);

 	TFile *fnorm5 = new TFile("/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_240GeV/output_ee_ZZ_qqqqBkg_240_y34cut_50K_ee_kt_SM.root");
 	TH1D *h5norm = (TH1D *) fnorm5->Get("h_mW1");
 	h5norm->SetLineColor(3);
 	h5norm->SetLineWidth(2);
 	h5norm->Scale(1/norm4);

 	TFile *fnorm6 = new TFile("/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_240GeV/output_ee_WW_qqllBkg_240_y34cut_50K_ee_kt_SM.root");
 	TH1D *h6norm = (TH1D *) fnorm6->Get("h_mW1");
 	h6norm->SetLineColor(4);
 	h6norm->SetLineWidth(2);
 	h6norm->Scale(1/norm5);

 	TFile *fnorm7 = new TFile("/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_240GeV/output_ee_ZH_qqqqBkg_240_y34cut_50K_ee_kt_SM.root");
 	TH1D *h7norm = (TH1D *) fnorm7->Get("h_mW1");
 	h7norm->SetLineColor(5);
 	h7norm->SetLineWidth(2);
 	h7norm->Scale(1/norm6);

 	TFile *fnorm8 = new TFile("/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_240GeV/output_ee_ZH_llqqBkg_240_y34cut_50K_ee_kt_SM.root");
 	TH1D *h8norm = (TH1D *) fnorm8->Get("h_mW1");
 	h8norm->SetLineColor(14);
 	h8norm->SetLineWidth(2);
 	h8norm->Scale(1/norm7);

 	TFile *fnorm9 = new TFile("/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_240GeV/output_ee_ZH_qqllBkg_240_y34cut_50K_ee_kt_SM.root");
 	TH1D *h9norm = (TH1D *) fnorm9->Get("h_mW1");
 	h9norm->SetLineColor(1);
 	h9norm->SetLineWidth(2);
 	h9norm->Scale(1/norm8);


	TH1D *hZHsemimW1 = new TH1D("ZHsemimW1","ZHsemimW1",140,20,120);
	hZHsemimW1->Add(h9norm);
	hZHsemimW1->Add(h8norm);
 	hZHsemimW1->SetLineWidth(3); 
 	hZHsemimW1->SetLineStyle(3); 

//////////////////////////////////////////   MW2 Norm  /////////////////////////////////////



 	TFile *fnorm12 = new TFile("/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_240GeV/output_ee_WW_qqqq_240_y34cut_50K_ee_kt_SM.root");
 	TH1D *h12norm = (TH1D *) fnorm12->Get("h_mW2");
 	h12norm->SetLineColor(2);
 	h12norm->SetLineWidth(2);

 	TFile *fnorm22 = new TFile("/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_240GeV/output_ee_qq_240_y34cut_Bkg_50K_ee_kt_SM.root");
 	TH1D *h22norm = (TH1D *) fnorm22->Get("h_mW2");
 	h22norm->SetLineColor(6);
 	h22norm->SetLineWidth(2);
 	h22norm->Scale(1/norm1);

 	TFile *fnorm42 = new TFile("/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_240GeV/output_ee_ZZ_qqllBkg_240_y34cut_50K_ee_kt_SM.root");
 	TH1D *h42norm = (TH1D *) fnorm42->Get("h_mW2");
 	h42norm->SetLineColor(7);
 	h42norm->SetLineWidth(2);
 	h42norm->Scale(1/norm3);

 	TFile *fnorm52 = new TFile("/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_240GeV/output_ee_ZZ_qqqqBkg_240_y34cut_50K_ee_kt_SM.root");
 	TH1D *h52norm = (TH1D *) fnorm52->Get("h_mW2");
 	h52norm->SetLineColor(3);
 	h52norm->SetLineWidth(2);
 	h52norm->Scale(1/norm4);

 	TFile *fnorm62 = new TFile("/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_240GeV/output_ee_WW_qqllBkg_240_y34cut_50K_ee_kt_SM.root");
 	TH1D *h62norm = (TH1D *) fnorm62->Get("h_mW2");
 	h62norm->SetLineColor(4);
 	h62norm->SetLineWidth(2);
 	h62norm->Scale(1/norm5);

 	TFile *fnorm72 = new TFile("/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_240GeV/output_ee_ZH_qqqqBkg_240_y34cut_50K_ee_kt_SM.root");
 	TH1D *h72norm = (TH1D *) fnorm72->Get("h_mW2");
 	h72norm->SetLineColor(5);
 	h72norm->SetLineWidth(2);
 	h72norm->Scale(1/norm6);

 	TFile *fnorm82 = new TFile("/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_240GeV/output_ee_ZH_llqqBkg_240_y34cut_50K_ee_kt_SM.root");
 	TH1D *h82norm = (TH1D *) fnorm82->Get("h_mW2");
 	h82norm->SetLineColor(14);
 	h82norm->SetLineWidth(2);
 	h82norm->Scale(1/norm7);
 	
 	TFile *fnorm92 = new TFile("/afs/cern.ch/user/s/slablack/fcc/output_wmass_y34cut_240GeV/output_ee_ZH_qqllBkg_240_y34cut_50K_ee_kt_SM.root");
 	TH1D *h92norm = (TH1D *) fnorm92->Get("h_mW2");
 	h92norm->SetLineColor(1);
 	h92norm->SetLineWidth(2);
 	h92norm->Scale(1/norm8);

	TH1D *hZHsemimW2 = new TH1D("ZHsemimW2","ZHsemimW2",140,20,120);
	hZHsemimW2->Add(h92norm);
	hZHsemimW2->Add(h82norm);
 	hZHsemimW2->SetLineWidth(3); 
 	hZHsemimW2->SetLineStyle(3); 

/*	double NbEntries = hZHsemimW2->GetEntries();
	cout<< NbEntries << endl;
*/

/////////////DRAW///////////////


	TCanvas *c0 = new TCanvas("canvas0", "Signal/Bkgd à 240 Gev W1 W2 norm", 0, 0, 960, 540);
 	c0->Divide(2, 1);
 	c0->cd(1);
 	h2norm->Draw("hist");
 	h1norm->Draw("hist same");
 	h4norm->Draw("hist same");
 	h5norm->Draw("hist same");
 	h6norm->Draw("hist same");
 	h7norm->Draw("hist same");
 	h8norm->Draw("hist same");
 	h9norm->Draw("hist same");
	hZHsemimW1->Draw("hist same");

 	//TLegend *leg0 = new TLegend(0.5, 0.65, 0.25, 0.9);
 	TLegend *leg0 = new TLegend(0.9, 0.5, 0.65, 0.75);
 	leg0->AddEntry(h1norm, "Signal", "l");
 	leg0->AddEntry(h2norm, "ee_qq", "l");
 	leg0->AddEntry(h4norm, "ee_ZZ_qqll", "l");
 	leg0->AddEntry(h5norm, "ee_ZZ_qqqq", "l");
 	leg0->AddEntry(h6norm, "ee_WW_qqll", "l");
 	leg0->AddEntry(h7norm, "ee_ZH_qqqq", "l");
 	leg0->AddEntry(h8norm, "ee_ZH_llqq", "l");
 	leg0->AddEntry(h9norm, "ee_ZH_qqll", "l");
	leg0->AddEntry(hZHsemimW1, "ee_ZH_(llq+qqll)", "l");
	leg0->SetTextSize(0.025);
 	leg0->Draw("SAME");

 	c0->cd(2);

 	h22norm->Draw("hist");
 	h12norm->Draw("hist same");
 	h42norm->Draw("hist same");
 	h52norm->Draw("hist same");
 	h62norm->Draw("hist same");
 	h72norm->Draw("hist same");
 	h82norm->Draw("hist same");
 	h92norm->Draw("hist same");
	hZHsemimW2->Draw("hist same");


 	TLegend *leg02 = new TLegend(0.9, 0.5, 0.65, 0.75);
 	leg02->AddEntry(h12norm, "Signal", "l");
 	leg02->AddEntry(h22norm, "ee_qq", "l");
 	leg02->AddEntry(h42norm, "ee_ZZ_qqll", "l");
 	leg02->AddEntry(h52norm, "ee_ZZ_qqqq", "l");
 	leg02->AddEntry(h62norm, "ee_WW_qqll", "l");
 	leg02->AddEntry(h72norm, "ee_ZH_qqqq", "l");
 	leg02->AddEntry(h82norm, "ee_ZH_llqq", "l");
 	leg02->AddEntry(h92norm, "ee_ZH_qqll", "l");
	leg02->AddEntry(hZHsemimW2, "ee_ZH_(llqq+qqll)", "l");
	leg02->SetTextSize(0.025);
 	leg02->Draw("SAME");


 	c0->SaveAs("Signal_Bck_W1_W2_y34cut_240Gev_norm.png");

 	return 0;

 }
