#!/bin/bash

#SBATCH --job-name=DSRM2edata
#SBATCH --output DSRM2edata.out
#SBATCH --error DSRM2edata.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=96:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load emboss

./getPairwiseASRdata.py DSRM2

date

