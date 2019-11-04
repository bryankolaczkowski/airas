#!/usr/bin/env python3

import sys
import os
import glob
import re

proteins = list(glob.glob("../asr/B*_R*"))
reps = []
for i in range(0,100):
    reps.append("R%d" % i)

def readFasta(infname):
    result = {}
    handle = open(infname, "r")
    id = ""
    for line in handle:
        if line[0] == ">":
            id = line[1:].strip()
            result[id] = ""
        else:
            result[id] += line.strip()
    handle.close()
    return result

def readppdists(infname):
    names = []
    ppdists = {}
    handle = open(infname, "r")
    line = handle.readline().strip()
    names = line.split(",")[2:]
    for line in handle:
        linearr = line.strip().split(",")
        node = linearr[0]
        col  = linearr[1]
        pps  = [float(x) for x in linearr[2:]]
        if node in ppdists.keys():
            ppdists[node].append(pps)
        else:
            ppdists[node] = [pps]
    handle.close()
    return (names,ppdists)

for protein in proteins:
    for rep in reps:
        ## read correct sequences ##
        if not os.path.exists("%s/%s/airas_RESULTS_correct_anc_seqs_aligned.fasta" % (protein,rep)):
            sys.stderr.write("ERROR: no results for %s %s\n" % (protein,rep))
            continue

        correct_sequences_aligned = readFasta("%s/%s/airas_RESULTS_correct_anc_seqs_aligned.fasta" % (protein,rep))

        ## get all posterior distributions for each alignment ##
        alnpatt = re.compile(".+/airas_RESULTS_(.+)\.asr\.csv")
        for f in glob.glob("%s/%s/airas_RESULTS_*.asr.csv" % (protein,rep)):
            alignment = alnpatt.search(f).group(1)
            (names,ppdists) = readppdists(f)
            outfile = open("corr_reports_01/%s.%s.%s.SeqCorrects_orig.csv" % (protein.split("/")[-1],rep,alignment), "w")
            outfile.write("node,position,correct_res,correct_pp\n")
            for node in ppdists.keys():
                if node == "ROOT" or node == "5":
                    continue
                correct_seq = correct_sequences_aligned[node]
                ppdist_list = ppdists[node]
                for i in range(len(correct_seq)):
                    correct_char = correct_seq[i]
                    ppdist = ppdist_list[i]

                    # calculate PP of correct char #
                    correct_index = -1
                    for j in range(len(names)):
                        if names[j] == correct_char:
                            correct_index = j
                            break
                    correct_pp = ppdist[correct_index]
                    if correct_index != 0 and ppdist[0] < 1.0:
                        correct_pp /= (1.0 - ppdist[0])
                    if correct_pp < 0.0:
                        correct_pp = 0.0

                    # calculate PP of ML char #
                    inferred_char = ""
                    inferred_pp   = 0.0
                    gappp = ppdist[0]
                    if ppdist[0] > 0.5:
                        inferred_char = "-"
                        inferred_pp = ppdist[0]
                    else:
                        for j in range(1,len(names)):
                            res = names[j]
                            pp  = ppdist[j]
                            if ppdist[0] < 1.0:
                                pp /= (1.0 - ppdist[0])
                            if pp > inferred_pp:
                                inferred_char = res
                                inferred_pp   = pp

                    # write corrects #
                    if inferred_char == correct_char:
                        outfile.write("%s,%d,%s,%.4f\n" % (node,i,correct_char,correct_pp))

            outfile.close()
            sys.stdout.write("done %s %s %s\n" % (protein,rep,alignment))
