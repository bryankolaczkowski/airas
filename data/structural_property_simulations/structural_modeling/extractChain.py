#!/usr/bin/env python

import sys

pdbfname = sys.argv[1]
chains   = sys.argv[2:]

handle = open(pdbfname, "r")
for line in handle:
	if len(line) > 21:
		chain = line[21]
		if chain in chains:
			sys.stdout.write(line)
handle.close()

