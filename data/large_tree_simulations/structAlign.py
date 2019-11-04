#!/usr/bin/python

import sys
import os
import glob

f = sys.argv[1]

outdir = "/".join(f.split("/")[:-1])
domain = f.split("/")[0]
unnum_domain = domain[:-1]

cmd = "ginsi --seed ../structures/%s_it.trimmed.fasta %s > %s/structaligned.raw.fasta" % (unnum_domain,f,outdir)
os.system(cmd)

# parse raw structure alignment - remove _seed sequences and remove all-gap columns #
seqids  = []
seqs    = []
newseqs = []

handle = open("%s/structaligned.raw.fasta" % outdir, "r")
line = handle.readline()
while line:
	if line[0] == ">":
		id = line[1:].strip()
		se = ""
		line = handle.readline()
		while line and line[0] != ">":
			se += line.strip()
			line = handle.readline()
		if id.find("_seed") != 0:
			seqids.append(id)
			seqs.append(se)
			newseqs.append("")
handle.close()

alnlen = len(seqs[0])
for i in range(alnlen):
	allgaps = True
	for s in seqs:
		if s[i] != "-":
			allgaps=False
			break
	if not allgaps:
		for j in range(len(seqids)):
			newseqs[j] += seqs[j][i]

# print new alignment #
outf = open("%s/structaligned.fasta" % outdir, "w")
for i in range(len(seqids)):
	outf.write(">%s\n%s\n" % (seqids[i],newseqs[i]))
outf.close()

os.remove("%s/structaligned.raw.fasta" % outdir)
