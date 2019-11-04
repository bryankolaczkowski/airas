#!/bin/bash

#SBATCH --job-name=CARD1edata
#SBATCH --output CARD1edata.out
#SBATCH --error CARD1edata.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=48:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load emboss

./getPairwiseASRdata.py CARD1

date

