#!/bin/bash

#SBATCH --job-name=RD1asr
#SBATCH --output RD1asr.out
#SBATCH --error RD1asr.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=10G
#SBATCH --time=24:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load mafft
module load raxml

./runAiras.py RD1

date

