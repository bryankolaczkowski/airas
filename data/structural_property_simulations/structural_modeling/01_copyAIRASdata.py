#!/usr/bin/env python3

import sys
import shutil
import glob
import os

topdir = "data"

for f in glob.glob("../AIRAS_results/rep*/*.fasta"):
    rep = f.split("/")[2]
    aln = f.split("RESULTS_")[1].split(".fasta")[0]
    if not os.path.exists("%s/%s" % (topdir,aln)):
        os.mkdir("%s/%s" % (topdir,aln))
    if not os.path.exists("%s/%s/%s" % (topdir,aln,rep)):
        os.mkdir("%s/%s/%s" % (topdir,aln,rep))
    # copy file, but not the "ROOT" node #
    handle = open(f, "r")
    outf   = open("%s/%s/%s/ancseqs.fasta" % (topdir,aln,rep), "w")
    line = handle.readline()
    while line:
        if line[0] == ">":
            id = line.strip()[1:]
            se = handle.readline().strip()
            if id != "ROOT":
                outf.write(">%s\n%s\n" % (id,se))
            line = handle.readline()
    handle.close()
    outf.close()
