#!/usr/bin/env python3

import sys
import numpy as np
import scipy.interpolate
import matplotlib
import matplotlib.pyplot as plt

proteins = ["CARD", "DSRM1", "DSRM2", "DSRM3", "RD"]
alnments = ["structaligned", "aligned_clustalw", "aligned_mafft",
            "aligned_msaprobs", "aligned_muscle", "aligned_probalign",
            "aligned_probcons", "aligned_tcoffee"]
datanames = [["Alignment Length", "Gap Proportion"], ["Variable-Site Proportion", "Parsimony-Informative Proportion"]]
data = {}

mindata =  100000.0
maxdata = -100000.0

handle = open("summary_vs_correct.txt", "r")
line = handle.readline()
prot = "XX"
for line in handle:
    linearr = line.split()
    if len(linearr) == 1:
        prot = linearr[0]
        data[prot] = {}
    else:
        alnmethod = linearr[0]
        results = [float(x) for x in linearr[1:]]
        data[prot][alnmethod] = results
        for res in results:
            if res < mindata:
                mindata = res
            if res > maxdata:
                maxdata = res
handle.close()

print(mindata,maxdata)

### plotting ###
fig, axs = plt.subplots(nrows=len(datanames),ncols=len(datanames[0]),sharex=True,sharey=True,
                        figsize=(6.5,6.5))

vmin = -2.0
vmax =  2.0

index = 0
for row in range(len(datanames)):
    for col in range(len(datanames[0])):

        mydataarr = []
        for rowname in proteins:
            myrow = []
            for colname in alnments:
                mydata = data[rowname][colname][index]
                myrow.append(mydata)
            mydataarr.append(myrow)

        mydata = np.array(mydataarr)

        ax  = axs[row,col]
        ret = ax.imshow(mydata, vmin=vmin, vmax=vmax, cmap='bwr')
        fig.colorbar(ret,ax=ax)

        ax.set_xticks(np.arange(len(alnments)))
        ax.set_yticks(np.arange(len(proteins)))

        if row == 1:
            ax.set_xticklabels(alnments)
            ax.set_xlabel("Alignment Method")

        if col == 0:
            ax.set_yticklabels(proteins)
            ax.set_ylabel("Protein Domain")

        ax.set_title(datanames[row][col])

        plt.setp(ax.get_xticklabels(), rotation=-45, ha="left", rotation_mode="anchor")

        index += 1

#plt.savefig("FIG.pdf", dpi=300)
plt.show()
