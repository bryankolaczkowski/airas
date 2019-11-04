#!/usr/bin/python

import sys
import glob

for prot in ["CARD1", "DSRM1", "DSRM2", "DSRM3", "RD1"]:
	ordered_labels = []
	distances_by_alignment = {}

	for thef in glob.glob("../%s/rep*/d_pos.csv" % prot):
		handle = open(thef, "r")
		labels = handle.readline().strip().split(",")
		dists  = [float(x) for x in handle.readline().strip().split(",")]
		for i in range(1,len(labels)):
			label = labels[i]
			dist  = dists[i]
			if label in distances_by_alignment.keys():
				distances_by_alignment[label].append(dist)
			else:
				distances_by_alignment[label] = [dist]
				ordered_labels.append(label)
		handle.close()

	outf = open("./%s.AlnDists.boxplotresults.csv" % prot, "w")
	for label in ordered_labels:
		outf.write(label)
		for x in distances_by_alignment[label]:
			outf.write(",%f" % x)
		outf.write("\n")
	outf.close()
