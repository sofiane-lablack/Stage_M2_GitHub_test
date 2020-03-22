import ROOT
from ROOT import TTree, TBranch, TFile, gROOT, AddressOf
import numpy as np

import random


gROOT.ProcessLine(
    "struct events_t {\
       Int_t                nEvt;\
       Int_t            nPhotons;\
       Double_t       Energy[30];\
    };")

EVT = [[120, 53, 186], [220, 150, 42, 58], [78], [], [64, 57, 97]]


class IsrTree():
    '''Fill the tree for several ISR photons'''

    def __init__(self, file, tree, events):

        self.file = file
        self.tree = tree
        self.events = events

        # self.tree.Branch("events", events, 'nEvts/I:nPhotons:Energy')
        self.tree.Branch("nPhotons", AddressOf(self.events, 'nPhotons'), 'nPhotons/I')
        self.tree.Branch("isr_e", AddressOf(self.events, 'Energy'), 'isr_e[nPhotons]/D')

    def fill(self):
        '''Fill the root tree. Call the fill method from TTree'''
        self.tree.Fill()

    def save_file(self):
        '''Write and close the root file'''
        self.file.Write()
        self.file.Close()


def loop_event():
    ''' Loop over the event, get the photons energy and fill the tree'''

    events = ROOT.events_t()

    file_ = TFile('test.root', 'recreate')
    tree_ = TTree("tree", "my tree")

    tree = IsrTree(file_, tree_, events)

    for event in EVT:
        events.nEvts = 1
        events.nPhotons = len(event)

        for iph, ph in enumerate(event):
            events.Energy[iph] = random.random()

        tree.fill()

    tree.save_file()


if __name__ == '__main__':
    loop_event()
