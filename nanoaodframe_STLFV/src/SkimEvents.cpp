/*
 * SkimEvents.cpp
 *
 *  Created on: Dec 9, 2018
 *      Author: suyong
 */

#include "SkimEvents.h"
#include "utility.h"

SkimEvents::SkimEvents(TTree *t, std::string outfilename, std::string year, std::string syst, std::string jsonfname, string globaltag, int nthreads)
:NanoAODAnalyzerrdframe(t, outfilename, year, syst, jsonfname, globaltag, nthreads),_year(year),_syst(syst)
{

}

// Define your cuts here
void SkimEvents::defineCuts()
{
	// Cuts to be applied in order
	// These will be passed to Filter method of RDF
	// check for good json event is defined earlier
        if(_year.find("wjet") != std::string::npos){
                addCuts("LHE_HT < 100","0");
                if(_year.find("16") != std::string::npos){
                        addCuts("Flag_filter && (HLT_IsoMu24 || HLT_IsoTkMu24) && nmuonpass == 1","00");
                }else if(_year.find("17") != std::string::npos){
                        addCuts("Flag_filter && HLT_IsoMu27 && nmuonpass == 1","00");
                }else if(_year.find("18") != std::string::npos){
                        addCuts("Flag_filter && HLT_IsoMu24 && nmuonpass == 1","00");
                }
        }else{ 
                if(_year.find("16") != std::string::npos){
                        addCuts("Flag_filter && (HLT_IsoMu24 || HLT_IsoTkMu24) && nmuonpass == 1","0");
                }else if(_year.find("17") != std::string::npos){
                        addCuts("Flag_filter && HLT_IsoMu27 && nmuonpass == 1","0");
                }else if(_year.find("18") != std::string::npos){
                        addCuts("Flag_filter && HLT_IsoMu24 && nmuonpass == 1","0");
                }
        }
}

void SkimEvents::defineMoreVars()
{
        if(_year.find("16") != std::string::npos){
            addVar({"Flag_filter","Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter",""});
        }else{
            // For 17, 18 UL
            addVar({"Flag_filter","Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter",""});
            // For 17, 18 v6
            //addVar({"Flag_filter","Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_ecalBadCalibFilterV2",""});
        }
        // define variables that you want to store
        addVartoStore("run");
        addVartoStore("luminosityBlock");
        addVartoStore("event");
        addVartoStore("puWeight.*");
        addVartoStore("pugenWeight.*");
        addVartoStore("unitGenWeight.*");
        addVartoStore("nGenPart");
        addVartoStore("GenPart_.*");
        addVartoStore("nGenJet");
        addVartoStore("GenJet_.*");
        addVartoStore("nGenVisTau");
        addVartoStore("GenVisTau_.*");
        addVartoStore("gen.*");
        addVartoStore("Pileup.*");
        addVartoStore("nJet");
        addVartoStore("Jet_area");
        addVartoStore("Jet_btagDeep.*");
        addVartoStore("Jet_eta");
        addVartoStore("Jet_genJetIdx");
        addVartoStore("Jet_hadronFlavour");
        addVartoStore("Jet_jetId");
        addVartoStore("Jet_mass");
        addVartoStore("Jet_p.*");
        addVartoStore("Jet_rawFactor");
        addVartoStore("nTau");
        addVartoStore("Tau_charge");
        addVartoStore("Tau_d.*");
        addVartoStore("Tau_eta");
        addVartoStore("Tau_gen.*");
        addVartoStore("Tau_idDecayModeNewDMs");
        addVartoStore("Tau_idDeepTau.*");
        addVartoStore("Tau_jetIdx");
        addVartoStore("Tau_mass");
        addVartoStore("Tau_phi");
        addVartoStore("Tau_pt");
        addVartoStore("Tau_puCorr");
        addVartoStore("Tau_rawDeep.*");
        addVartoStore("Tau_rawIso.*");
        addVartoStore("MET_p.*");
        addVartoStore("MET_sumEt");
        addVartoStore("RawMET.*");
        addVartoStore("LHE_HT");
        //addVartoStore("PuppiMET.*");
        //addVartoStore("RawPuppiMET.*");
        addVartoStore("nElectron");
        addVartoStore("Electron_charge");
        addVartoStore("Electron_cutBased");
        addVartoStore("Electron_deltaEtaSC");
        addVartoStore("Electron_dxy.*");
        addVartoStore("Electron_dz.*");
        addVartoStore("Electron_eta");
        addVartoStore("Electron_gen.*");
        addVartoStore("Electron_mass");
        addVartoStore("Electron_pf.*");
        addVartoStore("Electron_phi");
        addVartoStore("Electron_pt");
        addVartoStore("nMuon");
        addVartoStore("Muon_charge");
        addVartoStore("Muon_dxy.*");
        addVartoStore("Muon_dz.*");
        addVartoStore("Muon_eta");
        addVartoStore("Muon_gen.*");
        addVartoStore("Muon_loose.*");
        addVartoStore("Muon_mass");
        addVartoStore("Muon_pfRelIso04_all");
        addVartoStore("Muon_phi");
        addVartoStore("Muon_pt.*");
        addVartoStore("Muon_tightId");
        addVartoStore("Muon_mini.*");
        addVartoStore("PV.*");
        addVartoStore("fixedGridRhoFastjet.*");
}

void SkimEvents::bookHists()
{
	// _hist1dinfovector contains the information of histogram definitions (as TH1DModel)
	// the variable to be used for filling
	// and the minimum cutstep for which the histogram should be filled
	//
	// The braces are used to initalize the struct
	// TH1D
        add1DHist( {"hcounter", "Event counter", 2, -0.5, 1.5}, "one", "unitGenWeight", "");
}
