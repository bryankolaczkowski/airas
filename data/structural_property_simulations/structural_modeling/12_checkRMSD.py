#!/usr/bin/env python3

import sys
import os
import glob


for d1 in glob.glob("models/*/rep*"):
	aln = d1.split("/")[1]
	if aln == "correct_anc_seqs_aligned":
		continue
	for d in glob.glob("%s/D*/S*" % d1):
		if not os.path.exists("%s/rmsd.done" % d):
			sys.stdout.write("MISSING: %s\n" % d)

