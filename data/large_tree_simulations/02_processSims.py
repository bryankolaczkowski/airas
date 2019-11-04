#!/usr/bin/python

import sys
import os
import glob

for prot in ["CARD1"]:  # ["DSRM1", "DSRM2", "DSRM3", "RD1", "CARD1"]
	for infname in glob.glob("%s/rep*/evolved.ma" % prot):
		outdir = "/".join(infname.split("/")[:-1])

		outaln_extant    = "%s/correctaligned.fasta" % outdir
		outaln_ancestral = "%s/correctancestral.fasta" % outdir
		out_unaligned    = "%s/unaligned.fasta" % outdir

		outf_extant    = open(outaln_extant,"w")
		outf_ancestral = open(outaln_ancestral,"w")
		outf_unaligned = open(out_unaligned,"w")

		handle = open(infname, "r")
		line = handle.readline()
		while line:
			if line[0] == ">":
				myid = line.strip()
				myse = ""
				line = handle.readline()
				while line and line[0] != ">" and line[0] != "\n":
					myse += line.strip()
					line = handle.readline()
				# output sequences #
				if myid.find("_") > -1:	# it's an extant sequence
					outf_extant.write("%s\n%s\n" % (myid,myse))
					outf_unaligned.write("%s\n%s\n" % (myid,myse.replace("-","")))
				else:	# it's an ancestral sequence
					outf_ancestral.write("%s\n%s\n" % (myid,myse))
			else:
				line = handle.readline()

		handle.close()

		outf_extant.close()
		outf_ancestral.close()
		outf_unaligned.close()
