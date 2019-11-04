#!/bin/bash

#SBATCH --job-name=DSRM3edata
#SBATCH --output DSRM3edata.out
#SBATCH --error DSRM3edata.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=24:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load emboss

./getPairwiseASRdata.py DSRM3

date

