#!/bin/bash

#SBATCH --job-name=probalign
#SBATCH --output probalign.out
#SBATCH --error probalign.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=40G
#SBATCH --time=24:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load probalign

probalign unaligned.fasta > aligned_probalign.fasta

echo "done"
exit 0
