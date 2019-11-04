#!/bin/bash

#SBATCH --job-name=probcons
#SBATCH --output probcons.out
#SBATCH --error probcons.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=20G
#SBATCH --time=24:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

h=/home/bryank/gator2/src/probcons
${h}/probcons unaligned.fasta > aligned_probcons.fasta

echo "done"
exit 0
