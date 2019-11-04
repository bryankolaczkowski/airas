#!/usr/bin/env python3

import sys
import glob
import os

scrstr="""#!/bin/bash

#SBATCH --job-name=rndgr
#SBATCH --output=rndgr%a.out
#SBATCH --error=rndgr%a.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=100M
#SBATCH --time=36:00:00
#SBATCH --array=0-{len}
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load gcc

drs=({dirs})

#Set the number of runs that each SLURM task should do
PER_TASK={pertask}

# Calculate the starting and ending values for this task based
# on the SLURM task and the number of runs per task.
START_NUM=$(( $SLURM_ARRAY_TASK_ID * $PER_TASK ))
END_NUM=$(( ( ( $SLURM_ARRAY_TASK_ID + 1 ) * $PER_TASK ) - 1 ))

# Print the task and run range
echo This is task $SLURM_ARRAY_TASK_ID, which will do runs $START_NUM to $END_NUM

# Run the loop of runs for this task.
for (( run=$START_NUM; run<=$END_NUM; run++ )); do
	echo This is SLURM task $SLURM_ARRAY_TASK_ID, run number $run

	myd=${{drs[${{run}}]}}

	for d in `ls -d ${{myd}}/S*`;
	do
		f="${{d}}/dgr.done"
		if ! [ -f "${{f}}" ];
		then
			cd ${{d}}
			../../../../../runDgrem.bash
			cd ../../../../../
		fi
	done
done

date
echo $SLURM_ARRAY_TASK_ID done.
"""

pertask  = 10

dirarr   = glob.glob("models/*/rep*/D*")
lastjob  = int( ( len(dirarr) / pertask ) -1 )
thedirs  = " ".join('"{0}"'.format(x) for x in dirarr)
outstr   = scrstr.format(len=lastjob, dirs=thedirs, pertask=pertask)

outfname = "rndgr.bash"
outf = open(outfname, "w")
outf.write(outstr)
outf.close()
os.system("sbatch %s" % outfname)

