#!/usr/bin/env python3

import sys
from scipy import stats


alignments = ["aligned_clustalw",
              "aligned_mafft",
              "aligned_msaprobs",
              "aligned_muscle",
              "aligned_probalign",
              "aligned_probcons",
              "aligned_tcoffee",
              "structaligned",
              "correctaligned",
              "integratedaln"]

correctanc = "correct_anc_seqs_aligned"


# parse distances from root first #
dists_from_root = {}
handle = open("../dists_from_root.csv", "r")
handle.readline()
for line in handle:
    linearr = line.strip().split(",")
    node = linearr[0]
    bl   = float(linearr[1])
    dfr  = float(linearr[2])
    nfr  =   int(linearr[3])
    dists_from_root[node] = (bl,dfr,nfr)
handle.close()


# now parse the data #
aln_data = {}
cor_data = {}

for aln in alignments:
    aln_data[aln] = {}

handle = open(sys.argv[1], "r")
handle.readline()
for line in handle:
    linearr = line.strip().split(",")
    aln  = linearr[0]
    rep  = linearr[1]
    node = linearr[2]
    data = [float(x) for x in linearr[3:]]
    mean = sum(data)/len(data)
    if aln == correctanc:
        if node in cor_data.keys():
            cor_data[node][rep] = mean
        else:
            cor_data[node] = {}
            cor_data[node][rep] = mean
    else:
        if node in aln_data[aln].keys():
            aln_data[aln][node][rep] = mean
        else:
            aln_data[aln][node] = {}
            aln_data[aln][node][rep] = mean
handle.close()


# normalize data as distance from correct, if needed #
if len(cor_data.keys()) > 0:
    for aln in alignments:
        for node in aln_data[aln].keys():
            for rep in aln_data[aln][node].keys():
                d = aln_data[aln][node][rep]
                c = cor_data[node][rep]
                dist = max(d,c) - min(d,c)
                aln_data[aln][node][rep] = dist


# build results header #
header = "node,branchLength,distFromRoot,nodesFromRoot"
for aln in alignments:
    header += "," + aln
for aln in alignments:
    header += ",SE" + aln

# print results #
sys.stdout.write(header)
sys.stdout.write("\n")


for node in aln_data[alignments[0]].keys():

    # make sure we have data from all alignments for this node #
    good = True
    for aln in alignments:
        if node not in aln_data[aln].keys():
            good = False
            break
    if not good:
        continue

    # good data, print it... #
    (bl,dfr,nfr) = dists_from_root[node]
    sys.stdout.write("%s,%.4f,%.4f,%d" % (node,bl,dfr,nfr))

    for aln in alignments:
        data = list(aln_data[aln][node].values())
        ave  = sum(data)/len(data)
        sys.stdout.write(",%.4f" % ave)
    for aln in alignments:
        data = list(aln_data[aln][node].values())
        se   = stats.sem(data)
        sys.stdout.write(",%.4f" % se)
    sys.stdout.write("\n")
