#!/usr/bin/env python3

import sys
import glob

rep_node_to_corr = {}

for dr in glob.glob("models/correct_anc_seqs_aligned/rep*"):
	curr_rep = dr.split("/")[-1]
	rep_node_to_corr[curr_rep] = {}
	for idf in glob.glob("%s/D*/S*/id.txt" % dr):
		handle = open(idf, "r")
		nodeid = handle.readline().strip()
		handle.close()
		location = idf.split("/id.txt")[0]
		rep_node_to_corr[curr_rep][nodeid] = location

for dr in glob.glob("models/*/rep*"):
	aln = dr.split("/")[-2]
	if aln == "correct_anc_seqs_aligned":
		continue

	rep = dr.split("/")[-1]
	
	for finaldr in glob.glob("%s/D*/S*" % dr):
		handle = open("%s/id.txt" % finaldr, "r")
		id = handle.readline().strip()
		handle.close()

		corr_loc = rep_node_to_corr[rep][id]
		outf = open("%s/corr_node_location.txt" % finaldr, "w")
		outf.write("%s\n" % corr_loc)
		outf.close()


