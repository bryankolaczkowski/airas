#!/usr/bin/env python3

import sys
import os
import glob

min_results = 10

for d1 in glob.glob("models/*/rep*"):
	for d in glob.glob("%s/D*/S*" % d1):
		nresults = len(glob.glob("%s/seq.BESTMODEL_*.pdb.dgremout" % d))
		if nresults < min_results:
			sys.stdout.write("unfinished: %s\n" % d)
		else:
			outf = open("%s/dgrem.done" % d, "w")
			outf.write("got %d\n" % nresults)
			outf.close()

