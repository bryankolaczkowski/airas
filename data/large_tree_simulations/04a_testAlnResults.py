#!/usr/bin/python

import sys

def countSeqs(filename):
	count = 0
	handle = open(filename, "r")
	for line in handle:
		if line[0] == ">":
			count += 1
	handle.close()
	return count


for prot in ["CARD1", "DSRM1", "DSRM2", "DSRM3", "RD1"]:
	# count how many sequences there should be #
	correct_count = countSeqs("%s/rep1/unaligned.fasta" % prot)

	for i in range(1,11):
		rep = "rep%d" % i
		for aln in ["clustalw", "msaprobs", "probalign", "tcoffee", "mafft", "muscle", "probcons"]:
			# count how many sequences there are in alignment #
			fname = "%s/%s/aligned_%s.fasta" % (prot, rep, aln)
			mycount = countSeqs(fname)
			if mycount != correct_count:
				sys.stdout.write("%s\n" % fname)

