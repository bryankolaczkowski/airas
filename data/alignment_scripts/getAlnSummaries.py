#!/usr/bin/env python3

import sys
import os

proteins = ["CARD1", "DSRM1", "DSRM2", "DSRM3", "RD1"]

alignments = ["correctaligned.fasta",
"structaligned.fasta",
"aligned_clustalw.fasta",
"aligned_mafft.fasta",
"aligned_msaprobs.fasta",
"aligned_muscle.fasta",
"aligned_probalign.fasta",
"aligned_probcons.fasta",
"aligned_tcoffee.fasta"]

reps = range(1,11,1)

outfname = "summary.txt"
cmd = "./AMAS-master/amas/AMAS.py summary -d aa -f fasta -i %s > /dev/null" 

basedir = "simulated_sequences"

sys.stdout.write("protein,alignment,rep,alnLen,pGaps,pVar,pPars\n")

for protein in proteins:
    for alignment in alignments:
        for rep in reps:
            fname = "%s/%s/rep%s/%s" % (basedir,protein,rep,alignment)
            alnmethodname = alignment.split(".fasta")[0]
            os.system(cmd % fname)
            # parse summary.txt file #
            handle = open("summary.txt", "r")
            handle.readline()
            linearr = handle.readline().split()
            handle.close()

            aln_len     = int(linearr[2])
            p_gaps      = float(linearr[5])/100.0
            p_variable  = float(linearr[7])
            p_parsimony = float(linearr[9])

            # clean up #
            os.system("rm summary.txt")

            sys.stdout.write("%s,%s,%d,%d,%.4f,%.4f,%.4f\n" % (protein,alignment,rep,aln_len,p_gaps,p_variable,p_parsimony))
