#!/usr/bin/env python3

import sys
import os
import glob

for d1 in glob.glob("models/*/rep*"):
	for d in glob.glob("%s/D*/S*" % d1):
		npdb = len(glob.glob("%s/seq.BESTMODEL_*.pdb" % d))
		if npdb != 10 or not os.path.exists("%s/seq.done" % d):
			sys.stdout.write("unfinished: %s\n" % d)
			if os.path.exists("%s/seq.done" % d):
				os.remove("%s/seq.done" % d)

