from ROOT import TFile
import os


def create_output_dir(outdir):
    """Create output directory if it does not exist yet"""
    if not os.path.exists(outdir):
        os.makedirs(outdir)


def save_root_file(histdict, outdir):

    outfile_name = "{}.root".format(outdir)
    outfile = TFile(outfile_name, "recreate")

    for key, item in histdict.items():

        # do not save empty histograms
        if item.GetEntries() == 0:
            continue

        item.GetXaxis().SetTitle('[GeV]')
        item.Write()

    outfile.Write()
    outfile.Close()


if __name__ == '__main__':
    pass
