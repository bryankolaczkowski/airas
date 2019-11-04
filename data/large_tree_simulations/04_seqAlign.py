#!/usr/bin/python

import sys
import glob
import os
import shutil

seq_scripts = ["clustalw.bash",
               "mafft.bash",
               "msaprobs.bash",
               "muscle.bash", 
               "probalign.bash", 
               "probcons.bash",  
               "tcoffee.bash"]

basedir = os.getcwd()

for dr in glob.glob("*/rep*"):
	for scr in seq_scripts:
		shutil.copy("../alignment_scripts/%s" % scr, "%s/" % dr)

	os.chdir(dr)
	for scr in seq_scripts:
		os.system("sbatch %s" % scr)

	os.chdir(basedir)

