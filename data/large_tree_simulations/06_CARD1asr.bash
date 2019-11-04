#!/bin/bash

#SBATCH --job-name=CARD1asr
#SBATCH --output CARD1asr.out
#SBATCH --error CARD1asr.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=10G
#SBATCH --time=24:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load mafft
module load raxml

./runAiras.py CARD1

date

