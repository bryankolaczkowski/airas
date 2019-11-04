#!/bin/bash

#SBATCH --job-name=mafft
#SBATCH --output mafft.out
#SBATCH --error mafft.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=20G
#SBATCH --time=24:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load mafft

ginsi unaligned.fasta > aligned_mafft.fasta

echo "done"
exit 0
