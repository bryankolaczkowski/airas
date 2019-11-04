#!/usr/bin/env python3

import sys
import glob

GAPCUTOFF = 0.5

for i in range(1,11):
    repdir = "rep%d" % i
    for infile in glob.glob("%s/airas_RESULTS_*.asr.csv" % repdir):
        alnname = infile.split("RESULTS_")[1].split(".")[0]
        # read anc prob dists #
        prob_dists_by_node = {}
        ancstates = []
        handle = open(infile, "r")
        ancstates = handle.readline().strip().split(",")[2:]
        for line in handle:
            linearr = line.strip().split(",")
            node = linearr[0]
            col  = linearr[1]
            pps  = [float(x) for x in linearr[2:]]
            if node in prob_dists_by_node.keys():
                prob_dists_by_node[node].append(pps)
            else:
                prob_dists_by_node[node] = [pps]
        handle.close()
        # write ML ancestral sequences #
        outfname = "%s/airas_RESULTS_%s.fasta" % (repdir,alnname)
        handle = open(outfname, "w")
        for id in prob_dists_by_node.keys():
            seq = ""
            for ppdist in prob_dists_by_node[id]:
                if ppdist[0] >= GAPCUTOFF:
                    seq += ancstates[0]
                else:
                    maxpp = -1.0
                    maxi  = 0
                    for j in range(1,len(ancstates)):
                        if ppdist[j] > maxpp:
                            maxpp = ppdist[j]
                            maxi  = j
                    seq += ancstates[maxi]
            handle.write(">%s\n%s\n" % (id,seq))
        handle.close()
        
