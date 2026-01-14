from .base_processor import BaseProcessor
import sys
import ROOT
from pathlib import Path

class AnalysisProcessor(BaseProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.script = "processonefile.py"

    def process_all_in_one(self, outputroot):
        """Processes all files and merges them into a single output ROOT file."""
        rootfiles = self.get_root_files(self.indir)

        if not rootfiles:
            print("No files to process.")
            return

        t = ROOT.TChain(self.intreename)
        for afile in rootfiles:
            t.Add(str(afile))

        self.load_libraries()
        aproc = ROOT.LQtopAnalyzer(t, outputroot, self.year, self.syst, self.json, self.globaltag, self.split)
        aproc.setupAnalysis()
        aproc.run(self.saveallbranches, self.outtreename)

        # sum up counter histograms
        self.sum_counter_hists(rootfiles, outputroot)

    def sum_counter_hists(self, rootfiles, outputroot):
        counterhistogramsum = None
        for arootfile in rootfiles:
            intf = ROOT.TFile.Open(str(arootfile))
            if not intf or intf.IsZombie():
                continue
            counterhistogram = intf.Get("hcounter_nocut")
            if counterhistogram:
                if counterhistogramsum is None:
                    counterhistogramsum = counterhistogram.Clone()
                    counterhistogramsum.SetDirectory(0)
                else:
                    counterhistogramsum.Add(counterhistogram)
            intf.Close()

        if counterhistogramsum:
            print("Updating with counter histogram")
            outf = ROOT.TFile.Open(outputroot, "UPDATE")
            counterhistogramsum.Write()
            outf.Write("", ROOT.TObject.kOverwrite)
            outf.Close()
        else:
            print("counter histogram not found")

    def process(self, allinone=False):
        if allinone:
            self.process_all_in_one(str(self.outdir)) # in all-in-one, outdir is a filename
        else:
            self.run(self.script)
