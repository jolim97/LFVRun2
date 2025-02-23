import os
import sys
import ROOT
from ROOT import *
import array

pname = sys.argv[1]
print("pname : " + pname)
outfname = pname + ".root"
outfolder = "./hists/"
if not os.path.isdir(outfolder):
        os.mkdir(outfolder)
print("Output rootfiles will be stored at " + outfolder)

dir_base = "/data1/common/NanoAOD/v8_UL/"
dir_input = sys.argv[2]

flist = os.listdir(dir_base + dir_input)
rfile_list = []
for root, dirs, files in os.walk(dir_base + dir_input):
    for d in dirs:
        tmp_files = root + "/" + d + "/*.root"
        print(tmp_files)
        rfile_list.append(tmp_files)

std_rfile_list = ROOT.std.vector('string')()
for r in rfile_list:
    std_rfile_list.push_back(r)

df = ROOT.RDataFrame("Events",std_rfile_list)
print(df)

if pname == "WJetsToLNu_HT-0To100":
    df = df.Filter("LHE_HT < 100")

nocutevts = df.Count().GetValue()
df = df.Filter("HLT_IsoMu24")\
       .Define("muoncuts","Muon_pt > 30 && abs(Muon_eta) < 2.4 && Muon_tightId && Muon_pfRelIso04_all < 0.15")\
       .Define("nmuonpass","Sum(muoncuts)")\
       .Define("vetomuoncuts","!muoncuts && Muon_pt > 15 && abs(Muon_eta) < 2.4 && Muon_looseId && Muon_pfRelIso04_all < 0.25")\
       .Define("nvetomuons","Sum(vetomuoncuts)")\
       .Define("vetoelecuts","Electron_pt>15.0 && abs(Electron_eta)<2.4 && Electron_cutBased == 1")\
       .Define("nvetoeles","Sum(vetoelecuts)")\
       .Filter("nmuonpass == 1 && (nvetomuons + nvetoeles) == 0")

hmuon1pt = df.Define("muon1pt","Muon_pt[muoncuts][0]")\
             .Histo1D(ROOT.RDF.TH1DModel("hmuon1pt", "hmuon1pt", 40, 0, 400),"muon1pt")

hmuon1eta = df.Define("muon1eta","Muon_eta[muoncuts][0]")\
             .Histo1D(ROOT.RDF.TH1DModel("hmuon1eta", "hmuon1eta", 40, -4.0, 4.0),"muon1eta")


hfile = TFile( outfolder + outfname, "RECREATE" )
hcount_nocut = TH1D("hcount_nocut","counter",2,0,2)
hcount_nocut.SetBinContent(1,nocutevts)
hcount_nocut.Write()
hmuon1pt.Write()
hmuon1eta.Write()
hfile.Close()
