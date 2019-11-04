#!/bin/bash

#SBATCH --job-name=createAlnTemps
#SBATCH --output createAlnTemps.out
#SBATCH --error createAlnTemps.err
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=24:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load python3
module load mafft

./02_createAlnTemplates.py

date

