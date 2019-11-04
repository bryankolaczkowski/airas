#!/usr/bin/env python3

import sys
import os
import glob

proteins = ["CARD1", "DSRM1", "DSRM2", "DSRM3", "RD1"]

for protein in proteins:
    outf = open("../%s.origCorrects.csv" % protein, "w")
    outf.write("alignment,rep,node,alnLen,ResCorrect,GapCorrect,meanPP_ResCorrect,meanPP_GapCorrect\n")
    for f in glob.glob("%s.rep*.*.SeqCorrect_orig.csv" % protein):
        rep = f.split(".")[1]
        aln = f.split(".")[2]

        # read alignment length #
        fname = "../%s/%s/airas_RESULTS_correct_anc_seqs_aligned.fasta" % (protein,rep)
        handle = open(fname, "r")
        handle.readline()
        aln_len = len(handle.readline().strip())
        handle.close()

        # collect errors and such for each node #
        results = {}
        handle = open(f, "r")
        handle.readline()
        for line in handle:
            linearr = line.strip().split(",")
            node  = linearr[0]
            corrR = linearr[2]
            corrP = float(linearr[3])
            if node not in results.keys():
                results[node] = [0,0,[],[]]

            # insert gap: 1,3 #
            if corrR == "-":
                results[node][1] += 1
                results[node][3].append(corrP)

            # insert residue: 0,2 #
            else:
                results[node][0] += 1
                results[node][2].append(corrP)


        # print results to outfile #
        for node in results.keys():
            outf.write("%s,%s,%s,%d" % (aln,rep,node,aln_len))

            res_cors = results[node][0]
            res_PP = 0.0
            if res_cors > 0:
                res_PP = sum(results[node][2])/len(results[node][2])

            gap_cors = results[node][1]
            gap_PP = 0.0
            if gap_cors > 0:
                gap_PP = sum(results[node][3])/len(results[node][3])

            outf.write(",%d,%d,%.4f,%.4f\n" % (res_cors,gap_cors, res_PP,gap_PP))
