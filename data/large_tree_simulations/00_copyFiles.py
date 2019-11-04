#!/usr/bin/python

import os
import sys
import glob
import shutil

for prot in ["DSRM1", "DSRM2", "DSRM3", "RD1"]:
	basesource = "/Volumes/WorkBackup/bryan/projects/AIRAS/Kelsey_oldData/analysis/sequences/simulated_sequences/%s" % prot

	shutil.copy("%s/consensus_nosupport.tre" % basesource, "%s/" % prot)
	shutil.copy("%s/brlens_and_labels.tre"   % basesource, "%s/" % prot)

	for dir in glob.glob("%s/rep*" % basesource):
		rep  = dir.split("/")[-1]
		if not os.path.exists("%s/%s" % (prot,rep)):
			os.mkdir("%s/%s" % (prot,rep))

		shutil.copy("%s/%s/unaligned.fasta" % (basesource,rep), "%s/%s" % (prot,rep))
		shutil.copy("%s/%s/correctaligned.fasta" % (basesource,rep), "%s/%s" % (prot,rep))
		shutil.copy("%s/%s/correctancestral.fasta" % (basesource,rep), "%s/%s" % (prot,rep))
