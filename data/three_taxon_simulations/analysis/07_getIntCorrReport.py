#!/usr/bin/env python3

import sys
import os

alignments = ["aligned_clustalw",
              "aligned_mafft",
              "aligned_msaprobs",
              "aligned_muscle",
              "aligned_probalign",
              "aligned_probcons",
              "aligned_tcoffee"]

err_type = "all"
if len(sys.argv) > 1:
    err_type = sys.argv[1]

err_types = ["all", "res", "ins", "del"]

if err_type not in err_types:
    sys.stderr.write("ERROR: error type must be %s\n" % err_types)
    sys.exit(1)

bls = ["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8"]
irs = ["0.01", "0.02", "0.03", "0.04", "0.05", "0.06", "0.07", "0.08"]
reps = [ str(x) for x in range(100) ]

def getAlnErrs(bl,ir,rep):
    result = {}
    correct = {}
    for aln in alignments + ["integratedaln"]:
        result[aln] = {}
        correct[aln] = {}
        alnname = aln
        if aln.find("aligned_") != -1:
            alnname = aln + ".fasta"
        fname = "err_reports_01/B%s_R%s.R%s.%s.SeqErrors_orig.csv" % (bl,ir,rep,alnname)
        if not os.path.exists(fname):
            return (None,None)
        handle = open(fname, "r")
        handle.readline()
        for line in handle:
            linearr = line.strip().split(",")
            position = int(linearr[1])
            error    = linearr[4]
            corr     = linearr[2]
            result[aln][position] = error
            correct[aln][position] = corr
        handle.close()
    return (result,correct)


sys.stdout.write("BranchLength,IndelRate,Replicate,Position,alignment,P(same_error),P(different_error),P(no_error)\n")

for bl in bls:
    for ir in irs:
        for rep in reps:
            (aln_errs,aln_corr) = getAlnErrs(bl,ir,rep)
            if not aln_errs:  # skip missing reps
                continue

            for aln in alignments:
                for error_position in aln_errs[aln].keys():
                    error_state = aln_errs[aln][error_position]
                    correct_state = aln_corr[aln][error_position]
                    if error_position in aln_errs["integratedaln"].keys():
                        continue
                    if err_type == err_types[1] and (error_state == "-" or correct_state == "-"):
                        continue
                    elif err_type == err_types[2] and (error_state == "-" or correct_state != "-"):
                        continue
                    elif err_type == err_types[3] and (error_state != "-" or correct_state == "-"):
                        continue

                    count_same = 0.0
                    count_diff = 0.0
                    count_corr = 0.0
                    for otheraln in alignments:
                        if otheraln == aln:
                            continue
                        other_errs = aln_errs[otheraln]
                        if error_position in other_errs.keys():
                            if other_errs[error_position] == error_state:
                                count_same += 1
                            else:
                                count_diff += 1
                        else:
                            count_corr += 1

                    count_same /= (len(alignments)-1.0)
                    count_diff /= (len(alignments)-1.0)
                    count_corr /= (len(alignments)-1.0)

                    sys.stdout.write("%s,%s,%s,%d,%s,%.4f,%.4f,%.4f\n" % (bl,ir,rep,error_position,aln,count_same,count_diff,count_corr))
