#!/bin/bash

#SBATCH --job-name=glmres
#SBATCH --output glmres.out
#SBATCH --error glmres.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=100M
#SBATCH --time=24:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

./combineGLM.py > RESULTS_pkd.csv

date

