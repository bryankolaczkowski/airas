#!/bin/bash

#SBATCH --job-name=rmsdres
#SBATCH --output rmsdres.out
#SBATCH --error rmsdres.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=100M
#SBATCH --time=6:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

./combineRMSD.py > RESULTS_rmsd.csv

date

