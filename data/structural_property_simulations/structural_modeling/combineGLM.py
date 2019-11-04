#!/usr/bin/env python3

import sys
import os
import glob

def parseIt(direc):
	vals = []
	
	for f in glob.glob("%s/seq.BESTMODEL_*.pdb.results" % direc):
		handle = open(f, "r")
		for line in handle:
			if line.find("predicted pKD") == 0:
				vals.append(float(line.split()[-1]))	
		handle.close()	

	return vals


sys.stdout.write("alignment,rep,node,pKDs\n")

for d1 in glob.glob("models/*/rep*"):
	aln = d1.split("/")[1]
	rep = d1.split("/")[2]
	for thedr in glob.glob("%s/D*/S*" % d1):
		handle = open("%s/id.txt" % thedr, "r")
		node = handle.readline().strip()
		handle.close()

		values = parseIt(thedr)

		if len(values) > 2:		
			sys.stdout.write("%s,%s,%s" % (aln,rep,node))
			for v in values:
				sys.stdout.write(",%.4f" % v)
			sys.stdout.write("\n")



