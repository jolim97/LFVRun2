import os
import re
import subprocess
from pathlib import Path
from multiprocessing import Process
import cppyy
import ROOT

class BaseProcessor:
    def __init__(self, outdir, indir, outtree, intree, year, syst, json, split, skipold, recursive, saveallbranches, globaltag):
        self.outdir = Path(outdir)
        self.indir = Path(indir)
        self.outtreename = outtree
        self.intreename = intree
        self.year = year
        self.syst = syst
        self.json = json
        self.split = split
        self.skipold = skipold
        self.recursive = recursive
        self.saveallbranches = saveallbranches
        self.globaltag = globaltag
        
        if not self.indir.exists():
            print(f'Path {self.indir} does not exist')
            exit(1)

    def load_libraries(self, libname="libnanoadrdframe.so"):
        cppyy.load_reflection_info(libname)

    def get_root_files(self, directory):
        """Finds root files in the directory based on recursive flag."""
        files = []
        if self.recursive:
            for path in directory.rglob("*.root"):
                files.append(path)
        else:
            for path in directory.glob("*.root"):
                files.append(path)
        return files

    def filter_existing(self, rootfiles, outputdirectory):
        """Filters out files that have already been processed."""
        if not self.skipold:
            return rootfiles
        
        filtered = []
        for afile in rootfiles:
            outfname = Path(outputdirectory) / (afile.stem + "_analyzed.root")
            if not outfname.exists():
                filtered.append(afile)
            else:
                print(f"{afile.name} already in output dir, skipping")
        return filtered

    def run_process_one(self, script, infile, outfile):
        """Runs the external script for a single file."""
        cmd = [
            f"./{script}",
            f"--year={self.year}",
            f"--syst={self.syst}",
            f"--json={self.json}",
            f"--globaltag={self.globaltag}",
            str(infile),
            str(outfile),
            self.intreename,
            self.outtreename
        ]
        if self.saveallbranches:
            cmd.insert(4, "--saveallbranches")
        
        subprocess.call(cmd)

    def process_batch(self, script, outdir, rootfiles):
        """Processes a batch of files using the specified script."""
        for afile in rootfiles:
            outfname = Path(outdir) / (afile.stem + "_analyzed.root")
            self.run_process_one(script, afile, outfname)

    def run(self, script):
        """Main entry point for processing."""
        if not self.outdir.exists():
            self.outdir.mkdir(parents=True, exist_ok=True)
            
        rootfiles = self.get_root_files(self.indir)
        rootfiles = self.filter_existing(rootfiles, self.outdir)
        
        if not rootfiles:
            print("No files to process.")
            return

        if self.split > 1:
            njobs = min(self.split, len(rootfiles))
            nfileperjob = len(rootfiles) / njobs
            
            processes = []
            for i in range(njobs):
                start = int(i * nfileperjob)
                end = int((i + 1) * nfileperjob) if i < njobs - 1 else len(rootfiles)
                filesforjob = rootfiles[start:end]
                
                p = Process(target=self.process_batch, args=(script, self.outdir, filesforjob))
                p.start()
                processes.append(p)
                
            for p in processes:
                p.join()
        else:
            self.process_batch(script, self.outdir, rootfiles)
