#!/usr/bin/env python3

import sys
import glob

proteins = ["CARD1", "DSRM1", "DSRM2", "DSRM3", "RD1"]
outdir = "ALNDST_REPORTS"

for protein in proteins:
    data = {}

    for fname in glob.glob("../%s/rep*/d_pos.csv" % protein):
        rep = fname.split("/")[-2]
        handle = open(fname, "r")
        header = handle.readline().strip().split(",")
        distances = [float(x) for x in handle.readline().strip().split(",")]
        for i in range(len(header)):
            alnmethod = header[i]
            distance  = distances[i]
            if alnmethod in data.keys():
                data[alnmethod].append(distance)
            else:
                data[alnmethod] = [distance]
        handle.close()

    # print results #
    outfile = open("%s/%s.alndists.csv" % (outdir,protein), "w")
    outfile.write("AlnMethod,DistancesFromCorrectAln\n")
    for (alnmethod,distances) in data.items():
        outfile.write(alnmethod)
        for distance in distances:
            outfile.write(",%f" % distance)
        outfile.write("\n")
    outfile.close()
