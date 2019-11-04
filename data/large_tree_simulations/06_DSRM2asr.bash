#!/bin/bash

#SBATCH --job-name=DSRM2asr
#SBATCH --output DSRM2asr.out
#SBATCH --error DSRM2asr.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=10G
#SBATCH --time=24:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load mafft
module load raxml

./runAiras.py DSRM2

date
