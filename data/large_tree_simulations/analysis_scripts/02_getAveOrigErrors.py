#!/usr/bin/env python3

import sys
import os
import glob

proteins = ["CARD1", "DSRM1", "DSRM2", "DSRM3", "RD1"]

for protein in proteins:
    outf = open("../%s.origErrors.csv" % protein, "w")
    outf.write("alignment,rep,node,alnLen,ResErrors,InsErrors,DelErrors,meanPP_ResErrors,meanPP_InsErrors,meanPP_DelErrors,corrPP_ResErrors,corrPP_InsErrors,corrPP_DelErrors\n")
    for f in glob.glob("%s.rep*.*.SeqErrors_orig.csv" % protein):
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
            errR  = linearr[4]
            errP  = float(linearr[5])
            if node not in results.keys():
                results[node] = [0,0,0,[],[],[],[],[],[]]

            # insert error: 1,4,7 #
            if corrR == "-":
                results[node][1] += 1
                results[node][4].append(errP)
                results[node][7].append(corrP)

            # delete error: 2,5,8 #
            elif errR == "-":
                results[node][2] += 1
                results[node][5].append(errP)
                results[node][8].append(corrP)

            # substitution error: 0,3,6 #
            else:
                results[node][0] += 1
                results[node][3].append(errP)
                results[node][6].append(corrP)

        # print results to outfile #
        for node in results.keys():
            outf.write("%s,%s,%s,%d" % (aln,rep,node,aln_len))
            res_errs = results[node][0]
            resE_PP = 0.0
            resC_PP = 0.0
            if res_errs > 0:
                resE_PP  = sum(results[node][3])/len(results[node][3])
                resC_PP  = sum(results[node][6])/len(results[node][6])
            ins_errs = results[node][1]
            insE_PP = 0.0
            insC_PP = 0.0
            if ins_errs > 0:
                insE_PP  = sum(results[node][4])/len(results[node][4])
                insC_PP  = sum(results[node][7])/len(results[node][7])
            del_errs = results[node][2]
            delE_PP = 0.0
            delC_PP = 0.0
            if del_errs > 0:
                delE_PP  = sum(results[node][5])/len(results[node][5])
                delC_PP  = sum(results[node][8])/len(results[node][8])
            outf.write(",%d,%d,%d,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n" % (res_errs,ins_errs,del_errs,resE_PP,insE_PP,delE_PP,resC_PP,insC_PP,delC_PP))
