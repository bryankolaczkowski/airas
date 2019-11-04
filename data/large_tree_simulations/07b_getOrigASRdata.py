#!/usr/bin/python

import sys
import os
import glob

def calculateErrors(node,seq,correct_ancs):
	# read aligned sequences #
	corr_aligned = correct_ancs[node]
	infr_aligned = seq

	# compare sequences #
	inserts = 0
	deletes = 0
	errors  = 0
	length  = len(corr_aligned)
	for i in range(length):
		corr_c = corr_aligned[i]
		infr_c = infr_aligned[i]
		if corr_c == "-" and infr_c != "-":
			inserts += 1
		elif corr_c != "-" and infr_c == "-":
			deletes += 1
		elif corr_c != infr_c:
			errors += 1
#	print corr_aligned
#	print infr_aligned
#	print (length,errors,inserts,deletes)
	return (length,errors,inserts,deletes)

if len(sys.argv) < 2:
	sys.stderr.write("usage: %s PROTEIN [PROTEIN...]\n" % sys.argv[0])
	sys.stderr.write("  for example, PROTEIN = DSRM3\n")
	sys.exit(1)

for prot in sys.argv[1:]:
	if prot[-1] == "/":
		prot = prot[:-1]

	outf = open("%s.origErrors.csv" % prot, "w")
	outf.write("alignment,replicate,node,AlnLen,ResErrors,InsertErrors,DeleteErrors\n")
	for rep in glob.glob("%s/rep*" % prot):
		replicate = rep.split("/")[-1]
		# read unaligned correct ancestral sequences #
		aligned_correct_ancestrals = {}
		handle = open("%s/airas_RESULTS_correct_anc_seqs_aligned.fasta" % rep)
		line = handle.readline()
		while line:
			if line[0] == ">":
				id = line.strip()[1:]
				se = ""
				line = handle.readline()
				while line and line[0] != ">":
					se += line.strip()
					line = handle.readline()
				aligned_correct_ancestrals[id] = se
		handle.close()

		# go through inferred ancestral sequences #
		# we don't need the gaps                  #
		for asrfname in glob.glob("%s/airas_RESULTS_*.asr.csv" % rep):
			alignment = asrfname.split("airas_RESULTS_")[-1].split(".asr.csv")[0]
			handle = open(asrfname, "r")
			linearr = handle.readline().strip().split(",")
			residues = linearr[2:]
			node = ""
			seq  = ""
			for line in handle:
				linearr = line.strip().split(",")
				mynode = linearr[0]
				# clear existing node if we are onto the next one #
				if mynode != node:
					if node == "":
						node = mynode
					else:
						(length,errors,inserts,deletes) = calculateErrors(node,seq,aligned_correct_ancestrals)
						outf.write("%s,%s,%s,%d,%d,%d,%d\n" % (alignment,replicate,node,length,errors,inserts,deletes))
						node = mynode
						seq  = ""
				mypps  = [float(x) for x in linearr[2:]]
				if mypps[0] > 0.5:
					maxi = 0
					maxpp = mypps[0]
				else:
					maxi = -1
					maxpp = 0.0
					for i in range(1,len(mypps)):
						if mypps[i] > maxpp:
							maxi = i
							maxpp = mypps[i]
				# we do want gap characters #
				seq += residues[maxi]
			# last one is ROOT; we'll skip that one #
			handle.close()
