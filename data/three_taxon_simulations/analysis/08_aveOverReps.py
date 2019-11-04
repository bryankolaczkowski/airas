#!/usr/bin/env python3

import sys
from scipy import stats

def parseAve(fname):
    outfname = fname.split(".csv")[0] + ".ave.csv"

    results_same = {}
    results_diff = {}
    results_corr = {}

    handle = open(fname, "r")
    handle.readline()
    for line in handle:
        linearr = line.strip().split(",")
        id = linearr[0] + "," + linearr[1]
        psame = float(linearr[-3])
        pdiff = float(linearr[-2])
        pcorr = float(linearr[-1])
        if id in results_same.keys():
            results_same[id].append(psame)
            results_diff[id].append(pdiff)
            results_corr[id].append(pcorr)
        else:
            results_same[id] = [psame]
            results_diff[id] = [pdiff]
            results_corr[id] = [pcorr]
    handle.close()

    outf = open(outfname, "w")
    outf.write("BranchLength,IndelRate,P(same_error),P(diff_error),P(correct),SE(same),SE(diff),SE(corr)\n")
    for id in results_same.keys():
        mean_same = sum(results_same[id])/len(results_same[id])
        mean_diff = sum(results_diff[id])/len(results_diff[id])
        mean_corr = sum(results_corr[id])/len(results_corr[id])
        se_same   = stats.sem(results_same[id])
        se_diff   = stats.sem(results_diff[id])
        se_corr   = stats.sem(results_corr[id])
        outf.write("%s,%.4f,%.4f,%.4f,%.4e,%.4e,%.4e\n" % (id,mean_same,mean_diff,mean_corr,se_same,se_diff,se_corr))
    outf.close()

for fname in sys.argv[1:]:
    parseAve(fname)
