#!/bin/bash

#SBATCH --job-name=airas             # Job name
#SBATch --nodes=1                    # single node
#SBATCH --ntasks=1                   # single task
#SBATCH --cpus-per-task=1            # single-threaded
#SBATCH --distribution=cyclic:block  # thread distribution
#SBATCH --mem=500MB                  # memory
#SBATCH --time=24:00:00              # time limit hrs:min:sec
#SBATCH --output=airas.%a.out        # standard output log
#SBATCH --error=airas.%a.err         # standard error log
#SBATCH --qos=bryankol-b             # queue
#SBATCH --partition=hpg2-compute     # make sure only intel processors used
#SBATCH --array=0-63

module load mafft raxml

unset MAFFT_BINARIES

# find this job's experiment #
alndrs=(B*_R*)
alndr=${alndrs[$SLURM_ARRAY_TASK_ID]}

echo ${alndr}

cwd=`pwd`
repdrs=(${alndr}/R*)
for thedr in ${repdrs[@]};
do
	cd ${thedr}
	# do ASR #
	../../../../airas.py ../tree.tre aligned_clustalw.fasta aligned_mafft.fasta aligned_msaprobs.fasta aligned_muscle.fasta aligned_probalign.fasta aligned_probcons.fasta aligned_tcoffee.fasta -e correctaligned.fasta -c correctancestral.fasta
	echo " done ${thedr}"
	cd ${cwd}
done


echo "done."
exit 0

