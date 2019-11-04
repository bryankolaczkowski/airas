#!/bin/bash

#SBATCH --job-name=dgremres
#SBATCH --output dgremres.out
#SBATCH --error dgremres.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=100M
#SBATCH --time=24:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

./combineDGREM.py > RESULTS_dgrem.csv

date

