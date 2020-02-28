#!/bin/bash

#SBATCH --job-name=isg               # Job name
#SBATch --nodes=1                    # single node
#SBATCH --ntasks=1                   # single task
#SBATCH --cpus-per-task=1            # single-threaded
#SBATCH --distribution=cyclic:block  # thread distribution
#SBATCH --mem=500MB                  # memory
#SBATCH --time=24:00:00              # time limit hrs:min:sec
#SBATCH --output=isg.out             # standard output log
#SBATCH --error=isg.err              # standard error log
#SBATCH --qos=bryankol-b             # queue

# simulation parameters #
#seq length - 200
#indel size - 20
#insertion rate - 0.001 - 0.05
#deletion  rate - 0.001 - 0.05
#branch scale - 0.1 - 0.8

module load gcc

alpha=1.75
model=JTT
ndata=200
bscale=0.1
intree=INPUT.TRE
outbase=OUTEVOL

h=/home/bryank/gator2/indel-seq-gen-2.1.03/src
${h}/indel-seq-gen -g 4 -a ${alpha} -m ${model} -b ${bscale} -n ${ndata} -s 10000 -o f -w -e ${outbase} < ${intree}

date
echo "done."
