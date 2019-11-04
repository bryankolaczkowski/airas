#!/usr/bin/env python3

import sys
import os
from statistics import mean

prots = ["CARD1", "DSRM1", "DSRM2", "DSRM3", "RD1"]
reps  = ["rep1", "rep2", "rep3", "rep4", "rep5", "rep6", "rep7", "rep8", "rep9", "rep10"]
alns  = ["aligned_clustalw",
         "aligned_mafft",
         "aligned_msaprobs",
         "aligned_muscle",
         "aligned_probalign",
         "aligned_probcons",
         "aligned_tcoffee",
         "structaligned"]

sys.stdout.write("prot,rep,aln,alnDist,allErr,resErr,insErr,delErr\n")

for prot in prots:
    for rep in reps:
        for aln in alns:
            aln_dist = -1.0
            all_errs = {}
            res_errs = {}
            ins_errs = {}
            del_errs = {}

            # get aln dist #
            handle = open("../%s/%s/d_pos.csv" % (prot,rep), "r")
            header = handle.readline().strip().split(",")
            indx = -1
            for i in range(len(header)):
                if header[i] == aln:
                    indx = i
            dists = [float(x) for x in handle.readline().strip().split(",")]
            aln_dist = dists[indx]
            handle.close()

            # get errors #
            handle = open("%s.%s.%s.fasta.SeqErrors_orig.csv" % (prot,rep,aln), "r")
            for line in handle:
                linearr = line.strip().split(",")
                node = linearr[0]
                corr = linearr[2]
                err  = linearr[4]
                if node not in all_errs.keys():
                    all_errs[node] = 0
                    res_errs[node] = 0
                    ins_errs[node] = 0
                    del_errs[node] = 0
                all_errs[node] += 1
                if corr == "-":
                    ins_errs[node] += 1
                elif err == "-":
                    del_errs[node] += 1
                else:
                    res_errs[node] += 1
            handle.close()

            # get sequences with no errors #
            handle = open("%s.%s.%s.fasta.SeqCorrect_orig.csv" % (prot,rep,aln), "r")
            for line in handle:
                linearr = line.strip().split(",")
                node = linearr[0]
                if node not in all_errs.keys():
                    all_errs[node] = 0
                    res_errs[node] = 0
                    ins_errs[node] = 0
                    del_errs[node] = 0
            handle.close()

            # calculate alignment length #
            aln_len = 0
            handle = open("../%s/%s/%s.fasta" % (prot,rep,aln), "r")
            handle.readline()
            line = handle.readline()
            while line[0] != ">":
                aln_len += len(line.strip())
                line = handle.readline()
            handle.close()

            # calculate average error rates #
            ave_all_err = mean(all_errs.values()) / aln_len
            ave_res_err = mean(res_errs.values()) / aln_len
            ave_ins_err = mean(ins_errs.values()) / aln_len
            ave_del_err = mean(del_errs.values()) / aln_len

            # print results #
            sys.stdout.write("%s,%s,%s,%.4e,%.4e,%.4e,%.4e,%.4e\n" % (prot,rep,aln,aln_dist,ave_all_err,ave_res_err,ave_ins_err,ave_del_err))
