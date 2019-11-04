#!/usr/bin/env python3

import sys
import glob
import os

scrstr="""#!/bin/bash

#SBATCH --job-name=rnglm
#SBATCH --output=rnglm%a.out
#SBATCH --error=rnglm%a.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=100M
#SBATCH --time=24:00:00
#SBATCH --array=0-{len}
#SBATCH --qos=bryankol-b
date;hostname;pwd

module load python
module load gcc
module load R

# location of GLMScore #
GLMS="/ufrc/bryankol/bryank/src/GLM-Score-master"

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
		f="${{d}}/glm.done"
		if ! [ -f "${{f}}" ];
		then
			cd ${{d}}

			# link GLM-Score files            #
			# this only needs to be done once #
			ln -s ${{GLMS}}/asa ./
			ln -s ${{GLMS}}/R ./
			ln -s ${{GLMS}}/hydrophobicity.param ./
			ln -s ${{GLMS}}/tension.param ./

			# copy RNA ligand files into working directory #
			cp ../../../../../struct_templates/RNA_ligand.pdb ./
		  cp ../../../../../struct_templates/RNA_ligand.mol2 ./

			for f in `ls seq.BESTMODEL_*.pdb`;
			do
				r="${{f}}.results"
				if ! [ -f "${{r}}" ];
				then
					# extract protein chain #
					../../../../../extractChain.py ${{f}} A > TEMP.protein.pdb
					# run GLM score #
					${{GLMS}}/GLM-Score TEMP.protein.pdb RNA_ligand.pdb RNA_ligand.mol2 RNA
					# move results files #
					mv RNA_ligand.mol2.interaction_terms.txt ${{r}}.interaction_terms
					mv RNA_ligand_result.txt ${{r}}
					# clean up temp files #
					rm TEMP.protein.pdb
					rm bonds.log
					rm RNA_ligand_H-Bonds.pdb
				fi	
			done

			# unlink GLM-Score files    #
			# and clean up ligand files #
			rm asa
			rm R
			rm hydrophobicity.param
			rm tension.param
			rm RNA_ligand.pdb
			rm RNA_ligand.mol2
			rm core.*

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

outfname = "rnglm.bash"
outf = open(outfname, "w")
outf.write(outstr)
outf.close()
os.system("sbatch %s" % outfname)

