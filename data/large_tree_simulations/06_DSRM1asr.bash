#!/bin/bash

#SBATCH --job-name=DSRM1asr
#SBATCH --output DSRM1asr.out
#SBATCH --error DSRM1asr.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=10G
#SBATCH --time=24:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load mafft
module load raxml

./runAiras.py DSRM1

date

