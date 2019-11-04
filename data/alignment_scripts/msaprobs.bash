#!/bin/bash

#SBATCH --job-name=msaprobs
#SBATCH --output msaprobs.out
#SBATCH --error msaprobs.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=10G
#SBATCH --time=24:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

h=/home/bryank/gator2/src/MSAProbs-0.9.7/MSAProbs

${h}/msaprobs -num_threads 8 unaligned.fasta > aligned_msaprobs.fasta

echo "done"
exit 0
