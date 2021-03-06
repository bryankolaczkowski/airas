#!/usr/bin/env python3

import sys
import glob
import os

scrstr="""#!/bin/bash

#SBATCH --job-name=rnmd
#SBATCH --output runmd%a.out
#SBATCH --error runmd%a.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=100M
#SBATCH --time=12:00:00
#SBATCH --array=0-{len}
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load modeller

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

	d=${{drs[${{run}}]}}

	f="${{d}}/seq.done"
	if ! [ -f "${{f}}" ];
	then
		echo "  running ${{d}}"
		cd ${{d}}
		../../../../../runModelling.bash
		cd ../../../../../
	fi
done

date
echo $SLURM_ARRAY_TASK_ID done.

"""

pertask  = 10

dirarr = []
handle = open("MISSING.txt", "r")
for line in handle:
	dirarr.append(line.strip())
handle.close()


lastjob  = int( ( len(dirarr) / pertask ) -1 )
thedirs  = " ".join('"{0}"'.format(x) for x in dirarr)
outstr   = scrstr.format(len=lastjob, dirs=thedirs, pertask=pertask)

outfname = "runmd.bash"
outf = open(outfname, "w")
outf.write(outstr)
outf.close()
os.system("sbatch %s" % outfname)

