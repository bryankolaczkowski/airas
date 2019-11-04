#!/usr/bin/env python3

import sys
import glob
import os

SFASTA   = "TEMP_STRUCTALNFASTA_TEMP.fasta"
CATFASTA = "TEMP_CONCATENATEDFASTA_TEMP.fasta"
MERGET   = "TEMP_MERGETABLE_TEMP"
OUTFASTA = "TEMP_STRUCTFASTAMAP_TEMP.fasta"

SEQHOLDER = """>P1;seq
sequence:::::::::
<<PROTEINSEQUENCEALIGNED>>
/.................../.................*
"""

# read original alignment template #
orig_structure_aln = {}
handle = open("alignedStructures.ali", "r")
line = handle.readline()
while line:
    if line[0] == ">":
        id = line.strip()[1:]
        info = handle.readline().strip()
        se   = handle.readline().strip()
        rna  = ""
        if se[-1] == "*":
            se = se[:-1]
        else:
            rna = handle.readline().strip()
        orig_structure_aln[id] = (info,se,rna)
        line = handle.readline()
handle.close()

# write structural alignment as FASTA #
handle = open(SFASTA, "w")
for id in orig_structure_aln.keys():
    handle.write(">%s\n%s\n" % (id, orig_structure_aln[id][1]))
handle.close()

# now we need to read each of the alignments, mapping the structural aln to #
# the sequence alignment of each replicate, and store the template.         #
for f in glob.glob("./data/*/rep*/ancseqs.fasta"):
    thedir = f.split("ancseqs.fasta")[0]

    # align the structural templates with the ancestral sequence alignment #
    cmd = "cat %s %s > %s" % (SFASTA, f, CATFASTA)
    os.system(cmd)
    cmd = "./makemergetable.rb %s %s > %s" % (SFASTA, f, MERGET)
    os.system(cmd)
    cmd = "ginsi --merge %s %s > %s" % (MERGET, CATFASTA, OUTFASTA)
    os.system(cmd)

    # separate out the ancestral sequences (FASTA) and the structures (.ali) #
    all_seqs_aligned = {}
    id = ""
    handle = open(OUTFASTA, "r")
    for line in handle:
        if line[0] == ">":
            id = line.strip()[1:]
            all_seqs_aligned[id] = ""
        else:
            all_seqs_aligned[id] += line.strip()
    handle.close()

    outalntemplatef = open("%salntemplate.ali" % thedir, "w")
    outalnseqsf     = open("%salnancseqs.fasta" % thedir, "w")
    outalntemplatef.write("%s\n" % SEQHOLDER)

    for (id,se) in all_seqs_aligned.items():
        if id in orig_structure_aln.keys():
            (info,oldseq,rna) = orig_structure_aln[id]
            outalntemplatef.write(">%s\n%s\n%s" % (id,info,se))
            if rna != "":
                outalntemplatef.write("\n%s\n\n" % rna)
            else:
                outalntemplatef.write("*\n\n")
        else:
            outalnseqsf.write(">%s\n%s\n" % (id,se))

    outalntemplatef.close()
    outalnseqsf.close()

    # clean up temporary files #
    cmd = "rm %s %s %s" % (CATFASTA, MERGET, OUTFASTA)
    os.system(cmd)

# remove structure aln #
os.system("rm %s" % SFASTA)

