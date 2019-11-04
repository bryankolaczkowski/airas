#!/bin/bash

#SBATCH --job-name=DSRM1edata
#SBATCH --output DSRM1edata.out
#SBATCH --error DSRM1edata.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=96:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load emboss

./getPairwiseASRdata.py DSRM1

date

