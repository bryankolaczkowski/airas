#!/usr/bin/python

import sys
import glob
import os

basedir = sys.argv[1]
if basedir[-1] == "/":
	basedir = basedir[:-1]

workdir = os.getcwd()

for thedir in glob.glob("%s/rep*" % basedir):
	os.chdir(thedir)

	cmd = "../../../airas.py ../consensus_nosupport.tre aligned_clustalw.fasta aligned_mafft.fasta aligned_msaprobs.fasta aligned_muscle.fasta aligned_probalign.fasta aligned_probcons.fasta aligned_tcoffee.fasta -e structaligned.fasta -e correctaligned.fasta -c correctancestral.fasta"

	os.system(cmd)

	os.chdir(workdir)

