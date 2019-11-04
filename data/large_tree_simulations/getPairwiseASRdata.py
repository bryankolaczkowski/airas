#!/usr/bin/python

import sys
import os
import glob

needlecmd = "needle -asequence %s -bsequence %s -gapopen 10 -gapextend 0.5 -outfile %s -aformat markx3 2> /dev/null"

def calculateErrors(node,seq,correct_ancs,prot):
	corrfname = "%sXXTEMPXXcorrect.fasta" % prot
	infrfname = "%sXXTEMPXXinferred.fasta" % prot
	outfname  = "%sXXTEMPXX.fasta" % prot

	corrseq = correct_ancs[node]
	# print correct sequence #
	outf = open(corrfname, "w")
	outf.write(">%s\n%s\n" % (node,corrseq))
	outf.close()
	# print inferred sequence #
	outf = open(infrfname, "w")
	outf.write(">%s\n%s\n" % (node,seq))
	outf.close()
	# align sequences #
	os.system(needlecmd % (corrfname, infrfname, outfname))
	# read aligned sequences #
	corr_aligned = ""
	infr_aligned = ""
	handle = open(outfname, "r")
	line = handle.readline()
	while line:
		if line[0] == ">":
			se = ""
			line = handle.readline()
			while len(line) > 1 and line[0] != ">":
				se += line.strip()
				line = handle.readline()
			if corr_aligned == "":
				corr_aligned = se
			else:
				infr_aligned = se
				break
		else:
			line = handle.readline()
	handle.close()
	# clean up files #
	os.system("rm %s %s %s" % (corrfname, infrfname, outfname))
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
	return (length,errors,inserts,deletes)

if len(sys.argv) < 2:
	sys.stderr.write("usage: %s PROTEIN [PROTEIN...]\n" % sys.argv[0])
	sys.stderr.write("  for example, PROTEIN = DSRM3\n")
	sys.exit(1)

for prot in sys.argv[1:]:
	if prot[-1] == "/":
		prot = prot[:-1]
	outf = open("%s.pairwiseErrors.csv" % prot, "w")
	outf.write("alignment,replicate,node,AlnLen,ResErrors,InsertErrors,DeleteErrors\n")
	for rep in glob.glob("%s/rep*" % prot):
		replicate = rep.split("/")[-1]
		# read unaligned correct ancestral sequences #
		unaligned_correct_ancestrals = {}
		handle = open("%s/correctancestral.fasta" % rep)
		line = handle.readline()
		while line:
			if line[0] == ">":
				id = line.strip()[1:]
				se = ""
				line = handle.readline()
				while line and line[0] != ">":
					se += line.strip()
					line = handle.readline()
				unaligned_correct_ancestrals[id] = se.replace("-", "")
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
						(length,errors,inserts,deletes) = calculateErrors(node,seq,unaligned_correct_ancestrals,prot)
						outf.write("%s,%s,%s,%d,%d,%d,%d\n" % (alignment,replicate,node,length,errors,inserts,deletes))
						node = mynode
						seq  = ""
				mypps  = [float(x) for x in linearr[2:]]
				maxi = -1
				maxpp = 0.0
				for i in range(len(mypps)):
					if mypps[i] > maxpp:
						maxi = i
						maxpp = mypps[i]
				# we don't want gap characters #
				if maxi > 0:
					seq += residues[maxi]
			# last one is ROOT; we'll skip that one #
			handle.close()

