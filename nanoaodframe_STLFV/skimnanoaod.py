#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import argparse
from lib.skim_processor import SkimProcessor

def main():
    parser = argparse.ArgumentParser(description="NanoAOD skimming script for STLFV analysis.")
    parser.add_argument("indir", help="Input directory containing NanoAOD files or a list of files (.txt)")
    parser.add_argument("outdir", help="Output directory")
    parser.add_argument("-Y", "--year", default="", help="Select 2016, 2017, or 2018 for runs")
    parser.add_argument("-S", "--syst", default="", help="Systematic sources")
    parser.add_argument("-J", "--json", default="", help="Select events using this JSON file (data only)")
    parser.add_argument("--split", type=int, default=1, help="How many jobs to split into")
    parser.add_argument("--batch", action="store_true", default=False, help="Submit jobs @KISTI")
    parser.add_argument("--skipold", action="store_true", default=False, help="Skip existing root files")
    parser.add_argument("--recursive", action="store_true", default=True, help="Process files recursively")
    parser.add_argument("-F", "--flat", action="store_true", default=False, help="Process files recursively but store flat")
    parser.add_argument("--allinone", action="store_true", default=False, help="Output a single root file")
    parser.add_argument("--saveallbranches", action="store_true", default=False, help="Save all branches")
    parser.add_argument("--globaltag", default="", help="Global tag for JetMET corrections")

    args = parser.parse_args()

    intree = "Events"
    outtree = "outputTree"

    processor = SkimProcessor(
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
        globaltag=args.globaltag,
        batch=args.batch,
        flat=args.flat
    )

    processor.process(allinone=args.allinone)

if __name__ == "__main__":
    main()
