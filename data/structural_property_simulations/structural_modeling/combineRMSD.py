#!/usr/bin/env python3

import sys
import os
import glob

def parseIt(direc):
	vals = []

	if os.path.exists("%s/RMSDs_ca.csv" % direc):
		handle = open("%s/RMSDs_ca.csv" % direc, "r")
		vals = [float(x) for x in handle.readline().strip().split(",")]
		handle.close()	

	return vals


sys.stdout.write("alignment,rep,node,RMSDs\n")

for d1 in glob.glob("models/*/rep*"):
	aln = d1.split("/")[1]
	rep = d1.split("/")[2]

	if aln == "correct_anc_seqs_aligned":
		continue

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



