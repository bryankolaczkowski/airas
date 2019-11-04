#!/bin/bash

#SBATCH --job-name=mapcorr
#SBATCH --output=mapcorr.out
#SBATCH --error=mapcorr.err
#SBATCH --ntasks=1
#SBATCH --mem=200M
#SBATCH --time=12:00:00
#SBATCH --qos=bryankol-b
date;hostname;pwd

./calcCorrectNodeLocations.py

date
echo "done."

