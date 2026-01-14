from .base_processor import BaseProcessor
import os
import sys
import ROOT
from pathlib import Path

class SkimProcessor(BaseProcessor):
    def __init__(self, *args, **kwargs):
    batch = kwargs.pop('batch', False)
    flat = kwargs.pop('flat', False)
    super().__init__(*args, **kwargs)
    self.batch = batch
    self.flat = flat
    self.script = "skimonefile.py"
    if self.flat:
    self.recursive = False

    def batch_script(self, cmd):
    return f"""#!/bin/bash
cd {os.getcwd()}
{cmd}
"""

    def condor_script(self, script_filename, input_directory, output_directory, job_name):
    return f"""executable = {output_directory}/Log/{script_filename}
universe  = vanilla
JobBatchName = {job_name}
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
transfer_input_files    = {output_directory}/Log/{script_filename}
getenv     = True
Accounting_Group        = group_cms
output = {output_directory}/Log/skim_{job_name}.out
error = {output_directory}/Log/skim_{job_name}.error
log = {output_directory}/Log/skim_{job_name}.log
queue
"""

    def process_batch_jobs(self, rootfiles):
    log_dir = self.outdir / 'Log'
    log_dir.mkdir(exist_ok=True)

    for afile in rootfiles:
    # For KISTI xrootd
    xrootd_url = "root://cms-t2-se01.sdfarm.kr:1096/" + str(afile)
    outfname = self.outdir / (afile.stem + "_analyzed.root")

    cmd = f"./{self.script} --year={self.year} --syst={self.syst} --json={self.json} --globaltag={self.globaltag} {xrootd_url} {outfname} {self.intreename} {self.outtreename}"

    script_filename = f'sub_{afile.stem}.sh'
    with open(script_filename, 'w') as f:
    f.write(self.batch_script(cmd))

    os.chmod(script_filename, 0o755)
    (log_dir / script_filename).write_text(Path(script_filename).read_text())
    os.remove(script_filename)

    job_filename = f'job_{afile.stem}.sub'
    with open(job_filename, 'w') as f:
    f.write(self.condor_script(script_filename, str(self.indir), str(self.outdir), afile.stem))

    (log_dir / job_filename).write_text(Path(job_filename).read_text())
    os.remove(job_filename)

    print(f"Submitting job for {afile.name}")
    subprocess.call(['condor_submit', str(log_dir / job_filename)])

    def process(self, allinone=False):
    if allinone:
    # Simplified for now, similar to AnalysisProcessor
    rootfiles = self.get_root_files(self.indir)
    t = ROOT.TChain(self.intreename)
    for afile in rootfiles:
    t.Add(str(afile))
    self.load_libraries()
    aproc = ROOT.SkimEvents(t, str(self.outdir), self.year, self.syst, self.json, self.globaltag, self.split)
    aproc.setupAnalysis()
    aproc.run(self.saveallbranches, self.outtreename)
    elif self.batch:
    rootfiles = self.get_root_files(self.indir)
    self.process_batch_jobs(rootfiles)
    else:
    self.run(self.script)
