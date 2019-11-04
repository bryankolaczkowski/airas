#!/bin/bash

#SBATCH --job-name=muscle
#SBATCH --output muscle.out
#SBATCH --error muscle.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=15G
#SBATCH --time=24:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load muscle

muscle -in unaligned.fasta -out aligned_muscle.fasta

echo "done"
exit 0
