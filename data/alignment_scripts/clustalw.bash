#!/bin/bash

#SBATCH --job-name=clustalw
#SBATCH --output clustalw.out
#SBATCH --error clustalw.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=10G
#SBATCH --time=24:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load clustalw

clustalw2 -output=fasta -infile=unaligned.fasta -outfile=aligned_clustalw.fasta

echo "done"
exit 0
