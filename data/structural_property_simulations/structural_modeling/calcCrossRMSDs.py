#!/usr/bin/env python

import sys
import glob
import shutil
import os
from datetime import datetime
from modeller import *

# read locations file to get locations of sequences and structures #
handle = open("corr_node_location.txt", "r")
corrseqdir = "../../../../../%s" % handle.readline().strip()
handle.close()

# read aligned sequences into memory #
corrseq = ""
myseq  = ""
handle = open("%s/seq.txt" % corrseqdir, "r")
for line in handle:
    corrseq += line.strip()
handle.close()
handle = open("seq.txt", "r")
for line in handle:
    myseq += line.strip()
handle.close()

# write sequences into PIR format #
outf = open("tempalignment.ali", "w")
outf.write(">P1;corrseq\nstructure:corrstruct::A::A::::\n%s*\n" % corrseq)
outf.write(">P1;myseq\nstructure:mystruct::A::A::::\n%s*\n" % myseq)
outf.close()

# set up modeller environment #
#log.verbose()
env = environ()
env.io.atom_files_directory = ["./"]

# calculate RMSDs over all pairs of anc-des structures #
corrstructures = glob.glob("%s/seq.BESTMODEL_*.pdb" % corrseqdir)
corrstructures.sort()
mystructures = glob.glob("seq.BESTMODEL_*.pdb")
mystructures.sort()

total_rms_needed = min(len(corrstructures), len(mystructures))
all_pos_rms = []

for i in range(total_rms_needed):
    # copy structure files to current directoy #
    shutil.copy(corrstructures[i], "corrstruct.pdb")
    shutil.copy(mystructures[i], "mystruct.pdb")

    # build modeller alignment #
    aln = alignment(env)
    aln.append(file="tempalignment.ali", align_codes="all")

    # do RMSD comaprison #
    original = sys.stdout
    sys.stdout = open("modeller.log", "w")
    aln.compare_structures(output='SHORT')
    sys.stdout = original

    # parse modeller log for Positional RMS number #
    handle = open("modeller.log", "r")
    line = handle.readline()
    while line:
        if line.strip() == "Position comparison (FIT_ATOMS):":
            handle.readline()
            handle.readline()
            handle.readline()
            handle.readline()
            handle.readline()
            handle.readline()
            line = handle.readline()
            rms = float(line.split()[-1])
            all_pos_rms.append(rms)
            break
        else:
            line = handle.readline()
    handle.close()
    os.remove("modeller.log")

    # remove local structure files #
    os.remove("corrstruct.pdb")
    os.remove("mystruct.pdb")

# remove local alignment file #
os.remove("tempalignment.ali")

# write rms values to file #
outf = open("RMSDs_ca.csv", "w")
outf.write("%f" % all_pos_rms[0])
for r in all_pos_rms[1:]:
    outf.write(",%f" % r)
outf.write("\n")
outf.close()

# write done file if everything went okay #
# write rmsd.done file if everything went okay #
if len(all_pos_rms) == total_rms_needed:
    outf = open("rmsd.done", "w")
    outf.write("%s\n" % datetime.now())
    outf.close()
