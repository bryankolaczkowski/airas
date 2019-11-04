#!/usr/bin/env python3

import sys
import os
import shutil
import glob

SEQS_PER_DIR = 100
SEQPATT = "<<PROTEINSEQUENCEALIGNED>>"

seqs_written = 0
dirs_written = 0

def processSequence(id,seq,basedir):
    # define global variables we will be reassigning #
    global seqs_written
    global dirs_written

    # setup numberings #
    if seqs_written >= SEQS_PER_DIR:
        seqs_written = 0
        dirs_written += 1

    # setup directories to write to #
    outdir = "D%d" % dirs_written
    if dirs_written < 10:
            outdir = "D0%d" % dirs_written

    seqdir = "S%d" % seqs_written
    if seqs_written < 10:
        seqdir = "S0%d" % seqs_written

    # create directories as needed #
    if not os.path.isdir("models/%s/%s" % (basedir,outdir)):
        os.mkdir("models/%s/%s" % (basedir,outdir))
    os.mkdir("models/%s/%s/%s" % (basedir,outdir,seqdir))

    # write sequence ID and SEQ files #
    outf = open("models/%s/%s/%s/id.txt" % (basedir,outdir,seqdir), "w")
    outf.write("%s\n" % id)
    outf.close()

    outf = open("models/%s/%s/%s/seq.txt" % (basedir,outdir,seqdir), "w")
    outf.write("%s\n" % seq)
    outf.close()

    # write alignment file #
    outf = open("models/%s/%s/%s/alignment.ali" % (basedir,outdir,seqdir), "w")
    handle = open("data/%s/alntemplate.ali" % basedir, "r")
    for line in handle:
        newline = line.replace(SEQPATT, seq)
        outf.write(newline)
    handle.close()
    outf.close()

    # done #
    seqs_written += 1
    return

for d1 in glob.glob("data/*"):
    alndr = d1.split("/")[-1]
    if not os.path.isdir("models/%s" % alndr):
        os.mkdir("models/%s" % alndr)
    for d2 in glob.glob("%s/rep*" % d1):
        repdr = d2.split("/")[-1]
        bdir = "%s/%s" % (alndr,repdr)
        if not os.path.isdir("models/%s" % bdir):
            os.mkdir("models/%s" % bdir)

        # reset for each aln+rep #
        seqs_written = 0
        dirs_written = 0

        # whew! parse alignment #
        inputfilename = "%s/alnancseqs.fasta" % d2
        handle = open(inputfilename, "r")
        line = handle.readline()
        while line:
            if line[0] == ">":
                id = line[1:].strip()
                se = ""
                line = handle.readline()
                while line and line[0] != ">":
                    se += line.strip()
                    line = handle.readline()
                processSequence(id,se,bdir)
        handle.close()
