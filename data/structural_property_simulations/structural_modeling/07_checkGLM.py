#!/usr/bin/env python3

import sys
import os
import glob

min_results = 4

for d1 in glob.glob("models/*/rep*"):
	for d in glob.glob("%s/D*/S*" % d1):
		os.system("rm -f %s/*.tmp" % d)
		nresults = len(glob.glob("%s/seq.BESTMODEL_*.pdb.results" % d))
		if nresults < min_results:
			sys.stdout.write("unfinished: %s\n" % d)
		else:
			outf = open("%s/glm.done" % d, "w")
			outf.write("got %d\n" % nresults)
			outf.close()

