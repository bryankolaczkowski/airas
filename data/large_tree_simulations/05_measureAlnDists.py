#!/usr/bin/python

import os
import sys
import glob

alns = ["structaligned", "aligned_clustalw", "aligned_mafft", "aligned_msaprobs", "aligned_muscle", "aligned_probalign", "aligned_probcons", "aligned_tcoffee"]

for protein in ["CARD1", "DSRM1", "DSRM2", "DSRM3", "RD1"]:
	for thedir in glob.glob("%s/rep*" % protein):
		measures = [("d_pos","-p")]

		for (m_id,m_str) in measures:
			outfile = open("%s/%s.csv" % (thedir,m_id), "w")
			fromaln = "%s/correctaligned.fasta" % thedir

			outfile.write("correctaligned")
			for i in range(len(alns)):
				outfile.write(",%s" % alns[i])
			outfile.write("\n")
			outfile.write("0.0")

			for i in range(len(alns)):
				toaln   = "%s/%s.fasta" % (thedir, alns[i])
				cmd     = "metal %s %s %s > TEMP.metal.out" % (m_str, fromaln, toaln)
				sys.stderr.write("running %s %s %s..." % (m_id, fromaln, toaln))
				sys.stderr.flush()
				os.system(cmd)
				handle = open("TEMP.metal.out", "r")
				measure = float(handle.readline().split()[-1])
				handle.close()
				os.system("rm TEMP.metal.out")
				outfile.write(",%f" % measure)
				sys.stderr.write("done.\n")
			outfile.write("\n")

			outfile.close()
