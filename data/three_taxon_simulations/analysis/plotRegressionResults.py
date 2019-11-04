#!/usr/bin/env python3

import sys
import numpy as np
from scipy import stats

alignments = ["aligned_clustalw",
              "aligned_mafft",
              "aligned_msaprobs",
              "aligned_muscle",
              "aligned_probalign",
              "aligned_probcons",
              "aligned_tcoffee",
              "correctaligned",
              "integratedaln"]

def parseData():
    nbrlens = nindelrs = 8

    results = {}
    indelrs = []
    brlens  = []

    handle = open("err_report.all.csv", "r")
    handle.readline()
    for line in handle:
        linearr = line.strip().split(",")
        brlen  = float(linearr[0])
        indelr = float(linearr[1])
        alnerrs = [ float(x) for x in linearr[2:11] ]
        if brlen not in brlens:
            brlens.append(brlen)
        if indelr not in indelrs:
            indelrs.append(indelr)
        # update values #
        for i in range(len(alnerrs)):
            error     = alnerrs[i]
            alignment = alignments[i]
            if brlen not in results.keys():
                results[brlen] = {}
            if indelr not in results[brlen].keys():
                results[brlen][indelr] = {}
            results[brlen][indelr][alignment] = error
    handle.close()

    return (results, indelrs, brlens)


(results, indelrs, brlens) = parseData()

# first, regress errors vs branch lengths, for each indelr #
sys.stdout.write("IndelRate,Alignment,Slope,SE(Slope),P(Slope>0),Intercept,r2\n")
for indelr in indelrs:
    for alignment in alignments:
        X = brlens
        Y = []
        for brlen in brlens:
            Y.append(results[brlen][indelr][alignment])
        slope, intercept, r_value, p_value, std_err = stats.linregress(X,Y)
        sys.stdout.write("%.2f,%s,%.4f,%.4e,%.4e,%.4f,%.4f\n" % (indelr,alignment,slope,std_err,p_value,intercept,r_value*r_value))

# second, regress errors vs indelrs, for each branch length #
sys.stdout.write("BranchLength,Alignment,Slope,SE(Slope),P(Slope>0),Intercept,r2\n")
for brlen in brlens:
    for alignment in alignments:
        X = indelrs
        Y = []
        for indelr in indelrs:
            Y.append(results[brlen][indelr][alignment])
        slope, intercept, r_value, p_value, std_err = stats.linregress(X,Y)
        sys.stdout.write("%.1f,%s,%.4f,%.4e,%.4e,%.4f,%.4f\n" % (brlen,alignment,slope,std_err,p_value,intercept,r_value*r_value))
