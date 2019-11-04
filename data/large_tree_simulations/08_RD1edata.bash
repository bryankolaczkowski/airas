#!/bin/bash

#SBATCH --job-name=RD1edata
#SBATCH --output RD1edata.out
#SBATCH --error RD1edata.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=48:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load emboss

./getPairwiseASRdata.py RD1

date

