#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import argparse
from lib.analysis_processor import AnalysisProcessor

def main():
    parser = argparse.ArgumentParser(description="NanoAOD processing script for STLFV analysis.")
    parser.add_argument("indir", help="Input directory containing NanoAOD files")
    parser.add_argument("outdir", help="Output directory or file name (if all-in-one)")
    parser.add_argument("-Y", "--year", default="", help="Select 2016, 2017, or 2018 runs")
    parser.add_argument("-S", "--syst", default="", help="Systematic sources")
    parser.add_argument("-J", "--json", default="", help="Select events using this JSON file (data only)")
    parser.add_argument("--split", type=int, default=1, help="How many jobs to split into")
    parser.add_argument("--skipold", action="store_true", default=False, help="Skip existing root files")
    parser.add_argument("--recursive", action="store_true", default=True, help="Process files recursively")
    parser.add_argument("-A", "--allinone", action="store_true", default=False, help="Output a single root file")
    parser.add_argument("--saveallbranches", action="store_true", default=False, help="Save all branches")
    parser.add_argument("--globaltag", default="", help="Global tag for JetMET corrections")

    args = parser.parse_args()

    intree = "outputTree"
    outtree = "outputTree2"

    processor = AnalysisProcessor(
        outdir=args.outdir,
        indir=args.indir,
        outtree=outtree,
        intree=intree,
        year=args.year,
        syst=args.syst,
        json=args.json,
        split=args.split,
        skipold=args.skipold,
        recursive=args.recursive,
        saveallbranches=args.saveallbranches,
        globaltag=args.globaltag
    )

    processor.process(allinone=args.allinone)

if __name__ == "__main__":
    main()
