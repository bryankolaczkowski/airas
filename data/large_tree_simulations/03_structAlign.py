#!/usr/bin/python

import os
import glob

sbatch_str = """#!/bin/bash

#SBATCH --job-name=salign%d
#SBATCH --output salign%d.out
#SBATCH --error salign%d.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=4G
#SBATCH --time=4:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load mafft
./structAlign.py %s

date

"""

i = 1
for f in glob.glob("*/rep*/unaligned.fasta"):
	# write sbatch script #
	outf = open("salign%d.bash" % i, "w")
	outf.write(sbatch_str % (i,i,i,f))
	outf.close()
	# launch script #
	os.system("sbatch salign%d.bash" % i)
	i += 1
