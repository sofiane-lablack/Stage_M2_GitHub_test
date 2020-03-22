'''from ROOT import TCanvas, TFile, TF1, gDirectory, TLatex, TLegend, TObject, gStyle, gPad, TH2F
from array import array
import sys
from math import sqrt
import numpy


sys.path.insert(0, '../tools/')
import tools.histogram as histogram



def fit(histo, outdir, file=0, Ecm=0):
    """Fit the transverse profile to gat the parametrization and save in root file"""

    canvas_fit = TCanvas("c_fit_{}_{}".format(histo, Ecm),"c_fit",800,600)

    if not file:
        infile = outdir + ".root"
    else:
        infile = file

    file_ = TFile(infile,"r")
    file_.cd()
    #file_.Print()
    #print histo

    g_fit = gDirectory.Get(histo)
    g_fit.Draw()

    par = array( 'd', 13*[0.] )
    #TH2F (constchar *name, const char *title, Int_t nbinsx, Double_t xlow, Double_t xup, Int_t nbinsy, Double_t ylow, Double_t yup)
    #histchi2  = TH2F('histchi2','title',100,0,100,100,0,100)

    tail1xmin = -0.04
    tail1xmax = -0.055
    gaussxmin = -0.055
    gaussxmax = 0.045
    tail2xmin = 0.045
    tail2xmax = 0.04

    #par1tail1 = 0.2
    par2tail1 = 2.56
    #par1tail2 = -0.57
    par2tail2 = 2.64
    
    x=[]
    y=[]
    w=[]
    z=[]
    p=[]
    q=[]
    listpar1tail1=[]
    listpar2tail1=[]
    listpar1tail2=[]
    listpar2tail2=[]
    listsigma=[]

    listtail1xmaxgaussxmax=[]
    listtail2xmingaussxmin=[]
    listtotalfitchisquare=[]
    listchireal=[]
    listchirealtail1=[]
    listchirealtail2=[]

    #listcovmatrixtail1=[]
    #listcovmatrixtail2=[]
    #listcovmatrixtotal=[]

    listaveragepar1tail1=[]
    listaveragepar1tail2=[]

    listmeandistance=[]
    meandistance = 0

    #liste pour boucle sur les ranges gaussxmin et gaussxmax
    for i in range(0,3):
		m=-0.0012+i*0.0005
		p.append(m)
                n=-(-0.0015+i*0.0005)
		q.append(n)
    #liste boucle sur par1tail1 a parameter tail1
    for i in range(0,20):
	j=-10+i*5.0
	#j=6.168+i*0.00016
        x.append(j)
    #print x
    #print len(x)

    #liste boucle sur par1tail2 a parameter tail2
    for k in range(0,20):
        #l=-3.064+k*0.00016
	l=-10+k*0.5
	y.append(l)
    #print y
    #print len(y)

    #liste boucle sur par2tail1
    #for k in range(0,20):
    #    m=-7.9+k*0.01
    #    w.append(m)
    #print y
    #print len(y)

    #liste boucle sur par2tail2
    #for k in range(0,1):
    #    n=1.84
    #    z.append(n)
    #print y
    #print len(y)

    binlist=[]
    listdistance=[]
    listdistintermediaire=[]
    n = 0
    nbiter = 0
    for k in range(0,100):
        n=n+1
        binlist.append(n)


    for index, tail1xmaxgaussxmax in enumerate(q):
		print tail1xmaxgaussxmax

		for index, tail2xmingaussxmin in enumerate(p):
			#print tail2xmingaussxmin

			for index, par1tail1 in enumerate(x):
				#print par1tail1

				for index, par1tail2 in enumerate(y):
					#print par1tail2

					#for index, par2tail1 in enumerate(w):
						#print par2tail1

					#for index, par2tail2 in enumerate(z):
						#print par2tail2

					f1 = TF1("f1","gaus",tail2xmingaussxmin, tail1xmaxgaussxmax)
					fitgauss = g_fit.Fit(f1, "RNQS") #recupere valeur status (option S) et fit gauss
					par1 = f1.GetParameters()
					#print str(fitgauss.CovMatrixStatus()) #Print la valeur de status de gauss
					gaussfitcovmatrix = fitgauss.CovMatrixStatus()
					#print str(gaussfitcovmatrix)
					if gaussfitcovmatrix != 3:
					    continue

					tail1 = TF1("tail1","crystalball", tail1xmin, tail1xmaxgaussxmax)
					tail1.SetParameters(par1[0], par1[1], par1[2], par1tail1, par2tail1)
					tail1.SetLineColor(3)
					fittail1 = g_fit.Fit(tail1, "RNQS") #recupere valeur status (option S) et fit tail1
					par2 = tail1.GetParameters()
					tail1fitcovmatrix = fittail1.CovMatrixStatus()
					#print str(tail1fitcovmatrix) #Print la valeur de status tail 1
					if tail1fitcovmatrix != 3:
					    continue

					tail2 = TF1("tail2","crystalball", tail2xmingaussxmin, tail2xmax)
					tail2.SetParameters(par1[0], par1[1], par1[2], par1tail2, par2tail2)
					tail2.SetLineColor(4)
					fittail2 = g_fit.Fit(tail2, "RNQS") #recupere valeur status (option S) et fit tail2
					par3 = tail2.GetParameters()
					tail2fitcovmatrix = fittail2.CovMatrixStatus()
                                        #Print la valeur de status tail 2
					#print str(tail2fitcovmatrix)
					if tail2fitcovmatrix != 3:
					    continue

					par[0], par[1], par[2] = par1[0], par1[1], par1[2]
					par[3], par[4], par[5], par[6], par[7] = par2[0], par1[1], par2[2], par2[3], par2[4]
					par[8], par[9], par[10], par[11], par[12] = par3[0], par1[1], par3[2], par3[3], par3[4]
					total = TF1("total", 'gaus(0)+crystalball(3)+crystalball(8)', tail1xmin, tail2xmax)
					total.SetParameters(par)
					total.SetLineColor(1)
					totalfit = g_fit.Fit(total, "RNQS") #recupere valeur status (option S) et fit tout
					#print str(totalfit.CovMatrixStatus()) #Print la valeur de status du fit total
					totalfitcovmatrix = totalfit.CovMatrixStatus()
					#print "avant ",str(totalfitcovmatrix)

				        totalfitchisquare = totalfit.Chi2()
					totalfitchireal = total.GetChisquare()
					#if totalfitchireal > 94:
                                        #s    continue
				        #print "totalfitchisquare "+str(totalfitchisquare)
					totalfitchirealtail1 = tail1.GetChisquare()
					totalfitchirealtail2 = tail2.GetChisquare()


					if totalfitcovmatrix != 3:
					    continue
					#print "apres ",str(totalfitcovmatrix)

					# gStyle.SetOptFit(1)
					tot_param = total.GetParameters()
					sum_sigma = sqrt(tot_param[2]*tot_param[2] + tot_param[5]*tot_param[5] + tot_param[10]*tot_param[10])
					#print sum_sigma
					#if sum_sigma > 0.051:
					#    continue

					sum_sigma2 = sqrt(par1[2]*par1[2] + par2[2]*par2[2] + par3[2]*par3[2])
					#print "Verif = ", sum_sigma2

					distance = 0
					meandistance = 0
					#for index, bin in enumerate(binlist): 
					#	bincont = g_fit.GetXaxis().GetBinCenter(bin)
					#	fittedxval = total.Eval(bin);
					#	print "bin ="+str(bin)+" fittedxval= "+str(fittedxval)
					#	distance += abs(bincont-fittedxval
					chi2 = 0
					fullbins = 0
					for ibin in range(1,g_fit.GetNbinsX()+1):
						observation = g_fit.GetBinContent(ibin)
						binCentre = g_fit.GetXaxis().GetBinCenter(ibin)
						expectation = total.Eval(binCentre)
						distance = abs(binCentre-expectation)
						#print "distance = "+str(distance)
						listdistintermediaire.append(distance)
					meandistance = numpy.mean(listdistintermediaire)
					listmeandistance.append(meandistance)
					#if all(i < 5000 for i in listdistintermediaire):
					#	print "Trouve !! "
					#	raw_input("found !")
					#else: continue
					listdistance.append(distance)
					#print " g_fit.GetNbinsX() = "+str(g_fit.GetNbinsX())
					#print "distance = "+str(distance)
					

					#if (gaussfitcovmatrix == 3 & tail1fitcovmatrix == 3 & tail2fitcovmatrix == 3 & totalfitcovmatrix == 3):
					listsigma.append(sum_sigma)
					listpar1tail1.append(par1tail1)
					listpar1tail2.append(par1tail2)
					listtail1xmaxgaussxmax.append(tail1xmaxgaussxmax)
					listtail2xmingaussxmin.append(tail2xmingaussxmin)
					listchireal.append(totalfitchireal)

					listchirealtail1.append(totalfitchirealtail1)
					listchirealtail2.append(totalfitchirealtail2)
					#listpar2tail1.append(par2tail1)
					#listpar2tail2.append(par2tail2)
					#listcovmatrixtail1.append(tail1fitcovmatrix)
					#listcovmatrixtail2.append(tail2fitcovmatrix)
					#listcovmatrixtotal.append(totalfitcovmatrix)

					#print totalfitcovmatrix
					#print "sum sigma ",str(sum_sigma)
					listtotalfitchisquare.append(totalfitchisquare)

					#Trace sigma sur le graph
					uncertainty = TLatex()
					uncertainty.DrawLatex(-0.008, 3000, "#sigma = {}".format(sum_sigma))
					xmin_gauss = TLatex()
					xmin_gauss.DrawLatex(0.003,3000,"Gauss_xmin = {}".format(gaussxmin))
					xmax_gauss = TLatex()
					xmax_gauss.DrawLatex(0.003,2800,"Gauss_xmax = {}".format(gaussxmax))
					xmin_tail1 = TLatex()
					xmin_tail1.DrawLatex(0.003,2600,"tail1_xmin = {}".format(tail1xmin))
					xmax_tail1 = TLatex()
					xmax_tail1.DrawLatex(0.003,2400,"tail1_xmax = {}".format(tail1xmax))
					xmin_tail2 = TLatex()
					xmin_tail2.DrawLatex(0.003,2200,"tail2_xmin = {}".format(tail2xmin))
					xmax_tail2 = TLatex()
					xmax_tail2.DrawLatex(0.003,2000,"tail2_xmax = {}".format(tail2xmax))

					par1_tail1 = TLatex()
					par1_tail1.DrawLatex(0.003,1800,"tail1_par1 = {}".format(par1tail1))
					par2_tail1 = TLatex()
					par2_tail1.DrawLatex(0.003,1600,"tail1_par2 = {}".format(par2tail1))
					par1_tail2 = TLatex()
					par1_tail2.DrawLatex(0.003,1400,"tail2_par1 = {}".format(par1tail2))
					par2_tail2 = TLatex()
					par2_tail2.DrawLatex(0.003,1200,"tail2_par2 = {}".format(par2tail2))


					# write into the output file and close the file0
					outFileName = "{}.root".format(outdir)
					outFile = TFile(outFileName, "UPDATE")


					canvas_fit.Write("", TObject.kOverwrite)
					outFile.Write()
					outFile.Close()

					# canvas_fit.Print("{}/gaus_fit_{}_{}.pdf".format(outdir, histo, Ecm))
					#histchi2.Fill(par1tail1,par1tail2,totalfitchisquare)
    #c1_chi2 = TCanvas( 'c1')
    #c1_chi2.cd()				
    #histchi2.Draw("LEGO")
    #raw_input('ici')
    print "valeur mean distance = "+str(meandistance)
    indexminmeandistanceinter =  listmeandistance.index(min(listmeandistance))
    print "valeur par1tail1 de min mean distance ="+str(listpar1tail1[indexminmeandistanceinter])
    print "valeur par1tail2 de min mean distance ="+str(listpar1tail2[indexminmeandistanceinter])
    print "valeur gaussxmintail2xmin de min mean distance ="+str(listtail2xmingaussxmin[indexminmeandistanceinter])
    print "valeur gaussxmaxtail1xmax de min mean distance ="+str(listtail1xmaxgaussxmax[indexminmeandistanceinter])
    
    print len(listpar1tail1)
    minlistsigma = min(listsigma)
    print "le sigma min vaut"+str(minlistsigma)
    print "le chireal vaut "+str(min(listchireal))
    print "le chi2/fcn min vaut "+str(totalfitchisquare)
    indexlistchireal = listchireal.index(min(listchireal))
    indexlistchirealtail1 = listchirealtail1.index(min(listchirealtail1))
    indexlistchirealtail2 = listchirealtail2.index(min(listchirealtail2))
    indexminlistsigma = listsigma.index(min(listsigma))
    indexminlistdistance = listdistance.index(min(listdistance))
    indexminlisttotalfitchisquare = listtotalfitchisquare.index(min(listtotalfitchisquare))
    print "la position du sigma min est"+str(indexminlistsigma)
    print "la position du chi2 min est "+str(indexminlisttotalfitchisquare)
    par1tail1opti = listpar1tail1[indexminlisttotalfitchisquare]
    #par2tail1opti = listpar2tail1[indexminlistsigma]
    par1tail2opti = listpar1tail2[indexminlisttotalfitchisquare]
    #par2tail2opti = listpar2tail2[indexminlistsigma]
    tail1xmaxgaussxmaxopti = listtail1xmaxgaussxmax[indexminlisttotalfitchisquare]
    tail2xmingaussxminopti = listtail2xmingaussxmin[indexminlisttotalfitchisquare]

    print "la valeur de tail1xmaxgaussxmax qui correspond au minimum de distance est "+str(listtail1xmaxgaussxmax[indexminlistdistance])
    print "la valeur de tail2xmingaussxmin qui correspond au minimum de distance est "+str(listtail2xmingaussxmin[indexminlistdistance])
    print "la valeur de par1tail1 qui correspond au minimum de distance est "+str(listpar1tail1[indexminlistdistance])
    print "la valeur de par1tail2 qui correspond au minimum de distance est "+str(listpar1tail2[indexminlistdistance])

    print "la valeur de tail1xmaxgaussxmax qui correspond au minimum de sigma est "+str(listtail1xmaxgaussxmax[indexminlistsigma])
    print "la valeur de tail2xmingaussxmin qui correspond au minimum de sigma est "+str(listtail2xmingaussxmin[indexminlistsigma])
    print "la valeur de par1tail1 qui correspond au minimum de sigma est "+str(listpar1tail1[indexminlistsigma])
    print "la valeur de par1tail2 qui correspond au minimum de sigma est "+str(listpar1tail2[indexminlistsigma])
    print "la valeur de tail1xmaxgaussxmax qui correspond au minimum de chi2 est "+str(tail1xmaxgaussxmaxopti)
    print "la valeur de tail2xmingaussxmin qui corresponnd au minimum de chi2 est "+str(tail2xmingaussxminopti)
    print"la valeur de par1tail1 qui correspond au minimum chi2 est "+str(par1tail1opti)
    #print"la valeur de par2tail1 qui correspond au minimum de sigma est "+str(par2tail1opti)
    print"la valeur de par1tail2 qui correspond au minimum de chi2 est "+str(par1tail2opti)
    #print"la valeur de par2tail2 qui correspond au minimum de sigma est "+str(par2tail2opti)
    #print "valeur de sigma"+str(listsigma)
    #print "valeur par1tail1"+str(listpar1tail1)
    #print "valeur par2tail1"+str(listpar2tail1)
    #print "valeur par1tail2"+str(listpar1tail2)
    listaveragepar1tail1 = numpy.mean(listpar1tail1)
    listaveragepar1tail2 = numpy.mean(listpar1tail2)
    print "la valeur moyenne de par1tail1 est "+str(listaveragepar1tail1)
    print "la valeur moyenne de par1tail2 est "+str(listaveragepar1tail2)
    print " borne inf chi real est "+str(listtail1xmaxgaussxmax[indexlistchireal])
    print " borne sup chi real est "+str(listtail2xmingaussxmin[indexlistchireal])
    print "par 1 tail 1 chi real est "+str(listpar1tail1[indexlistchireal])
    print "par 1 tail 2 chi real est "+str(listpar1tail2[indexlistchireal])

    print "par1 tail1 listchirealtail1 est "+str(listpar1tail1[indexlistchirealtail1])
    print "xmingausstail2xmin listchirealtail1 est "+str(listtail2xmingaussxmin[indexlistchirealtail1])
    #print "xmaxgausstail1xmax listchirealtail2 est "+str(listtail1xmaxgaussxmax[indexlistchirealtail1])
    print "par1 tail2 listchirealtail2 est "+str(listpar1tail2[indexlistchirealtail2])
    print "xmingausstail2xmin listchirealtail2 est "+str(listtail2xmingaussxmin[indexlistchirealtail2])
    #print"xmaxgausstail1xmax listchirealtail1 est "+str(listtail1xmaxgaussxmax[indexlistchirealtail2])
    #raw_input("hit a key to exit")


def main():
		    """Main function"""

		    # Ecm = 350
		    # mW = 80.385
		    # nEvents = 10000
		    # channel = 'semi_leptonic'
		    # detector = 'wo_detector'

		    # if detector == 'detector':
		    #     det_type = 'CLIC'
		    # else:
		    #     det_type = ''

		    # dire = "/afs/cern.ch/work/m/mabeguin/private/Wmass_direct_measurement/plots/{}/{}/{}/{}GeV/".format(detector, det_type, channel, Ecm)
		    # outdir = "../plots/{}/{}/{}/gaus_fit".format(detector, det_type, channel)

		    # histogram.create_output_dir(outdir)

		    # file = dire+"W_mass_{}_{}_{}_ee_kt.root".format(Ecm, nEvents, mW)
		    # print "Opening file: ", file

		    # fit("h_mass_pair1", outdir, file, Ecm)


if __name__ == '__main__':
    main'''
#usr/bin/env python
from ROOT import TCanvas, TFile, TF1, gDirectory, TLatex, TLegend, TObject, gStyle, gPad
from array import array
import sys
from math import sqrt

sys.path.insert(0, '../tools/')
import tools.histogram as histogram



def fit(histo, outdir, file=0, Ecm=0):
    """Fit the transverse profile to gat the parametrization and save in root file"""

    canvas_fit = TCanvas("c_fit_{}_{}".format(histo, Ecm),"c_fit",800,600)

    if not file:
        infile = outdir + ".root"
    else:
        infile = file

    file_ = TFile(infile,"r")
    file_.cd()
    #file_.Print()
    #print histo

    g_fit = gDirectory.Get(histo)
    g_fit.Draw()

    par = array( 'd', 13*[0.] )

    tail1xmin = -0.3
    gaussxmin = tail2xmin = -0.03
    gaussxmax = tail1xmax = 0.06
    #gaussxmin = -0.0012
    #gaussxmax = 0003
    tail2xmax = 0.5

    par1tail1 = 5.8
    par2tail1 = 2.75
    par1tail2 = -4.25
    par2tail2 = 4.7



    f1 = TF1("f1","gaus", gaussxmin, gaussxmax)
    g_fit.Fit(f1, "RN")
    par1 = f1.GetParameters()

    tail1 = TF1("tail1","crystalball", tail1xmin, tail1xmax)
    tail1.SetParameters(par1[0], par1[1], par1[2], par1tail1, par2tail1)
    tail1.SetLineColor(3)
    g_fit.Fit(tail1, "RN")
    par2 = tail1.GetParameters()

    tail2 = TF1("tail2","crystalball", tail2xmin, tail2xmax)
    tail2.SetParameters(par1[0], par1[1], par1[2], par1tail2, par2tail2)
    tail2.SetLineColor(4)
    g_fit.Fit(tail2, "RN")
    par3 = tail2.GetParameters()

    par[0], par[1], par[2] = par1[0], par1[1], par1[2]
    par[3], par[4], par[5], par[6], par[7] = par2[0], par1[1], par2[2], par2[3], par2[4]
    par[8], par[9], par[10], par[11], par[12] = par3[0], par1[1], par3[2], par3[3], par3[4]
    total = TF1("total", 'gaus(0)+crystalball(3)+crystalball(8)', tail1xmin, tail2xmax)
    total.SetParameters(par)
    total.SetLineColor(1)
    totalfit = g_fit.Fit(total, "R+S")
    totalfitcovmatrix = totalfit.GetCovarianceMatrix()
    #totalfitStdDev = totalfit.GetStdDev(x)
    #totalfitfcn = totalfit.mnhess()
    #if totalfitcovmatrix == 3:
    #print "totalfilcovmatrix"+str(totalfitcovmatrix)
    	#print str(totalfitfcn)

    # gStyle.SetOptFit(1)
    tot_param = total.GetParameters()
    sum_sigma = sqrt(tot_param[2]*tot_param[2] + tot_param[5]*tot_param[5] + tot_param[10]*tot_param[10])
    print sum_sigma

    sum_sigma2 = sqrt(par1[2]*par1[2] + par2[2]*par2[2] + par3[2]*par3[2])
    print "Verif = ", sum_sigma2

    #Trace sigma sur le graph
    '''uncertainty = TLatex()
    uncertainty.DrawLatex(-0.008, 3000, "#sigma = {}".format(sum_sigma))
    xmin_gauss = TLatex()
    xmin_gauss.DrawLatex(0.003,3000,"Gauss_xmin = {}".format(gaussxmin))
    xmax_gauss = TLatex()
    xmax_gauss.DrawLatex(0.003,2800,"Gauss_xmax = {}".format(gaussxmax))
    xmin_tail1 = TLatex()
    xmin_tail1.DrawLatex(0.003,2600,"tail1_xmin = {}".format(tail1xmin))
    xmax_tail1 = TLatex()
    xmax_tail1.DrawLatex(0.003,2400,"tail1_xmax = {}".format(tail1xmax))
    xmin_tail2 = TLatex()
    xmin_tail2.DrawLatex(0.003,2200,"tail2_xmin = {}".format(tail2xmin))
    xmax_tail2 = TLatex()
    xmax_tail2.DrawLatex(0.003,2000,"tail2_xmax = {}".format(tail2xmax))

    par1_tail1 = TLatex()
    par1_tail1.DrawLatex(0.003,1800,"tail1_par1 = {}".format(par1tail1))
    par2_tail1 = TLatex()
    par2_tail1.DrawLatex(0.003,1600,"tail1_par2 = {}".format(par2tail1))
    par1_tail2 = TLatex()
    par1_tail2.DrawLatex(0.003,1400,"tail2_par1 = {}".format(par1tail2))
    par2_tail2 = TLatex()
    par2_tail2.DrawLatex(0.003,1200,"tail2_par2 = {}".format(par2tail2))'''

    # write into the output file and close the file0
    outFileName = "{}.root".format(outdir)
    outFile = TFile(outFileName, "UPDATE")

    raw_input("hit a key to exit")

    canvas_fit.Write("", TObject.kOverwrite)
    outFile.Write()
    outFile.Close()

    fittedparameter = "log_boost"
    outfit = "/afs/cern.ch/user/s/slablack/fcc/correlation_matrix_365GeV/Fit_parameters_correlation_matrix_sign_and_bkg_240GeV"
    fitresults = open("{}_{}.txt".format(outfit,fittedparameter),"w")
    fitresults.write("sum_sigma {} \n".format(sum_sigma))
    fitresults.write("gaussxmin {} \n".format(gaussxmin))
    fitresults.write("gaussxmax {} \n".format(gaussxmax))
    fitresults.write("tail1xmin {} \n".format(tail1xmin))
    fitresults.write("tail1xmax {} \n".format(tail1xmax))
    fitresults.write("tail2xmin {} \n".format(tail2xmin))
    fitresults.write("tail2xmax {} \n".format(tail2xmax))
    fitresults.write("par1tail1 {} \n".format(par1tail1))
    fitresults.write("par2tail1 {} \n".format(par2tail1))
    fitresults.write("par1tail2 {} \n".format(par1tail2))
    fitresults.write("par2tail2 {} \n".format(par2tail2))
    fitresults.close()

    # canvas_fit.Print("{}/gaus_fit_{}_{}.pdf".format(outdir, histo, Ecm))


def main():
		    """Main function"""

		    # Ecm = 350
		    # mW = 80.385
		    # nEvents = 10000
		    # channel = 'semi_leptonic'
		    # detector = 'wo_detector'

		    # if detector == 'detector':
		    #     det_type = 'CLIC'
		    # else:
		    #     det_type = ''

		    # dire = "/afs/cern.ch/work/m/mabeguin/private/Wmass_direct_measurement/plots/{}/{}/{}/{}GeV/".format(detector, det_type, channel, Ecm)
		    # outdir = "../plots/{}/{}/{}/gaus_fit".format(detector, det_type, channel)

		    # histogram.create_output_dir(outdir)

		    # file = dire+"W_mass_{}_{}_{}_ee_kt.root".format(Ecm, nEvents, mW)
		    # print "Opening file: ", file

		    # fit("h_mass_pair1", outdir, file, Ecm)


if __name__ == '__main__':
    main
