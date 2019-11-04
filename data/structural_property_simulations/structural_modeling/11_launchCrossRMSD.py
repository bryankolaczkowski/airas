#!/usr/bin/env python3

import sys
import glob
import os

scrstr="""#!/bin/bash

#SBATCH --job-name=xrmsd%d
#SBATCH --output=xrmsd%d.out
#SBATCH --error=xrmsd%d.err
#SBATCH --ntasks=1
#SBATCH --mem=100M
#SBATCH --time=24:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load modeller

for d in `ls -d %s/D*/S*`;
do
	f="${d}/rmsd.done"
	if ! [ -f "${f}" ];
	then
		cd ${d}
		../../../../../calcCrossRMSDs.py
		cd ../../../../../
	fi
done

date
"""

idx = 1
for dr in glob.glob("models/*/rep*"):
	aln = dr.split("/")[1]
	if aln == "correct_anc_seqs_aligned":
		continue

	outfname = "xrmsd%d.bash" % idx
	outf = open(outfname, "w")
	outf.write(scrstr % (idx,idx,idx,dr))
	outf.close()
	os.system("sbatch %s" % outfname)

	idx += 1

