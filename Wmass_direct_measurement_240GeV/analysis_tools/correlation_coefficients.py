'''The aim of this file is to get a correlation coefficients form a TH2 histograms'''

from ROOT import TFile, gDirectory


def correlation_coefficient(input, output, ecm):
    '''Function to get the correlation coefficients from a TH2'''

    file_ = TFile(input,"r")
    file_.cd()


    for obj in file_.GetListOfKeys():
        if "h_corr_" in obj.GetName():
            histo = gDirectory.Get(obj.GetName())

            output.write("{} \t {}\n".format(obj.GetName(), histo.GetCorrelationFactor()))


def main():
    '''Main function to select the study. The user can change the parameters to put the correct
    input file or gives directly the name of his file. The coefficents are written in an output txt
    file.'''

    # parameters to choose the study
    ecm = 365  #GeV
    m_w = 80.385  #GeV
    nevt = 50 #K
    channel = 'semi-leptonic'

    ###### Input
    if channel == 'hadronic':
        decay = 'qqqq'
    else:
        decay = 'qqll'

    infile = "../output/plots/uncertainties_study/{}/corre_matrix_{}_{}K_M{}.root".format(channel, ecm, nevt, str(m_w)[:2])


    ###### Output
    outdir = "../output/data/{}".format(channel)
    outfile = open('{}/correlation_coefficients_{}_{}K_M{}.txt'.format(outdir, ecm, nevt, str(m_w)[:2]), 'w')

    #  Run function
    correlation_coefficient(infile, outfile, ecm)

if __name__ == '__main__':
    main()

