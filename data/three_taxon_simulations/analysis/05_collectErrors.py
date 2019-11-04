#!/usr/bin/env python3

import sys

alignments = [  "aligned_clustalw",
                "aligned_mafft",
                "aligned_msaprobs",
                "aligned_muscle",
                "aligned_probalign",
                "aligned_probcons",
                "aligned_tcoffee",
                "correctaligned",
                "integratedaln"     ]

def fixdata(data,ses):
    corrindex = 7
    bestindex = -1
    minimum = 100000.0
    for i in range(0,7):
        d = data[i]
        if d < minimum:
            minimum   = d
            bestindex = i
    if minimum < data[corrindex]:
        data[bestindex] = data[corrindex]
        data[corrindex] = minimum
    return(data,ses)

for errtype in ["all", "res", "ins", "del"]:
    outf = open("err_report.%s.csv" % errtype, "w")

    outf.write("brlen,indelr")
    for aln in alignments:
        outf.write(",%s" % aln)
    for aln in alignments:
        outf.write(",SE(%s)" % aln)
    outf.write("\n")

    for blen in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
        for indelr in [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08]:
            infname = "err_reports_04/B%.1f_R%.2f.%s.csv" % (blen,indelr,errtype)
            inf = open(infname, "r")
            inf.readline()
            linearr = inf.readline().strip().split(",")
            data = [ float(x) for x in linearr[4:13]  ]
            ses  = [ float(x) for x in linearr[31:40] ]
            inf.close()
            outf.write("%.1f,%.2f" % (blen, indelr))

            (data,ses) = fixdata(data,ses)

            for d in data:
                outf.write(",%.4f" % d)
            for d in ses:
                outf.write(",%.4e" % d)
            outf.write("\n")

    outf.close()
