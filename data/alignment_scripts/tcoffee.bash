#!/bin/bash

#SBATCH --job-name=tcoffee
#SBATCH --output tcoffee.out
#SBATCH --error tcoffee.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=40G
#SBATCH --time=24:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load tcoffee

t_coffee -max_n_proc 1 -n_core 1 -seq=unaligned.fasta -outfile=tcoffee.aln
t_coffee -other_pg seq_reformat -in tcoffee.aln -output fasta_aln > aligned_tcoffee.fasta

echo "done"
exit 0

