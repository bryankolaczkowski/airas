#!/usr/bin/python

import sys
import os

# number of simulated datasets to generate per tree #
NUM_RUNS = 10

constraints = {
"DSRM1":"2222222000022222222222222000000000000000000000000000000000000000000222200000000000222222222000000000000222000000000000000000000000000000222200222222222222222222222",
"DSRM2":"2220002222000222022220222200000000000000000000000000000000000222200022222222000000000000000000222022220222222222000000002222222000000000000000",
"DSRM3":"222222222222222022222222222000002222000000022222222220000222220222222202222222222222200000000000",
"RD1":"00000000022222220222222222200002220000002222222220000000000000000000000000000000000000002222000022200000000002220000022222222000000000222000000022200022222222200000222222222222220000000000000000000000222022222220002222200000",
"CARD1":"22222222222000000000000000000222002220000000000000000000000000000000222222000000000000000000000000000222000000000000000000000022222222222222222222222222"}

max_indels = {"DSRM1":4, "DSRM2":4, "DSRM3":2, "RD1":5, "CARD1":2}

for prot in ["DSRM1", "DSRM2", "DSRM3", "RD1", "CARD1"]:
	inalnfname = "../real_sequences/%s/structaligned.fasta" % prot
	ordered_ids = []
	alndict = {}
	alnlen  = 0
	idlen   = 0
	handle = open(inalnfname, "r")
	line = handle.readline()
	while line:
		if line[0] == ">":
			myid = line[1:].strip()
			myse = ""
			line = handle.readline()
			while line and line[0] != ">":
				myse += line.strip()
				line = handle.readline()
			alnlen = len(myse)
			ordered_ids.append(myid)
			alndict[myid] = myse
			if len(myid) > idlen:
				idlen = len(myid)
	handle.close()

	# output alignment in weirdo format #
	outfname = "%s/input.aln" % prot
	handle = open(outfname, "w")

	# write all these zeros #
	for i in range(idlen):
		handle.write(" ")
	handle.write(" ")
	handle.write(constraints[prot])
	handle.write("\n")

	for myid in ordered_ids:
		handle.write(myid)
		for i in range(len(myid),idlen):
			handle.write(" ")
		handle.write(" ")
		handle.write(alndict[myid])
		handle.write("\n")

	handle.close()

	# output control file #
	treefname = "%s/consensus_nosupport.tre" % prot
	tree = ""
	handle = open(treefname, "r")
	for line in handle:
		tree += line.strip()
	handle.close()

	outfname = "%s/input.tre" % prot
	handle = open(outfname, "w")
	handle.write("[:../input.aln(,,r)] {%d,0,} " % max_indels[prot])
	handle.write(tree)
	handle.write("\n")
	handle.close()

	# for convenience, output bash script to run indel model #
	# need separate one for each replicate directory         #
	for i in range(1,NUM_RUNS+1):
		outfname = "%s/rep%d/evolve.bash" % (prot,i)
		handle = open(outfname, "w")
		handle.write("#!/bin/bash\n\n")
		handle.write("#SBATCH --job-name=evolve\n")
		handle.write("#SBATCH --output evolve.out\n")
		handle.write("#SBATCH --error evolve.err\n")
		handle.write("#SBATCH --ntasks=1\n")
		handle.write("#SBATCH --mem-per-cpu=10G\n")
		handle.write("#SBATCH --time=48:00:00\n")
		handle.write("#SBATCH --qos=bryankol-b\n\n")
		handle.write("module load gcc\n\n")
		handle.write("../../../../indel-seq-gen-2.1.03/src/indel-seq-gen -g 4 -a 1.75 -m JTT -n 1 -o f -w -e evolved < ../input.tre\n\n")
		handle.write("date\n")
		handle.close()
		os.system("chmod 755 %s" % outfname)
