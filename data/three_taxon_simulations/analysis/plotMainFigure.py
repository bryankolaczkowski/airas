#!/usr/bin/env python3

import sys
import numpy as np
import scipy.interpolate
import matplotlib
import matplotlib.pyplot as plt

vmin = -0.03
vmax =  0.03
# 0.3
# 0.1
# 0.1

alnmethods = ["aligned_clustalw",
              "aligned_mafft",
              "aligned_msaprobs",
              "aligned_muscle",
              "aligned_probalign",
              "aligned_probcons",
              "aligned_tcoffee",
              "correctaligned",
              "integratedaln"]

startindex = 2

def getData(fname):

    correct_index = 9

    dx = 0.1
    dy = 0.01

    XY = []
    C_aln = []
    C_int = []

    handle = open(fname, "r")
    handle.readline()
    for line in handle:
        linearr = [ float(x) for x in line.strip().split(",") ]
        brlen  = linearr[0]
        indelr = linearr[1]
        cor_d  = linearr[correct_index]
        aln_d  = min(linearr[2:9])
        int_d  = linearr[10]
        XY.append([brlen,indelr])
        C_aln.append(cor_d - aln_d)
        C_int.append(cor_d - int_d)
    handle.close()
    return (XY,C_aln,C_int)


fig, axs = plt.subplots(nrows=4,ncols=2,sharex=True,sharey=True,figsize=(3.5,4.5))

fnameparts = ["all", "res", "ins", "del"]
err_types  = ["Total Errors", "Residue Errors", "Insertion Errors", "Deletion Errors"]
for row in range(len(fnameparts)):
    fname = "err_report.%s.csv" % fnameparts[row]

    # get results #
    (xy,c_aln,c_int) = getData(fname)
    xx,yy = np.meshgrid(np.arange(0.1,0.81,0.01),np.arange(0.01,0.081,0.001))
    grid_x, grid_y = np.mgrid[0:1:100j, 0:1:100j]
    zz_aln = scipy.interpolate.griddata(xy,c_aln, (xx,yy), method='cubic')
    zz_int = scipy.interpolate.griddata(xy,c_int, (xx,yy), method='cubic')
    results = [zz_aln, zz_int]

    for i in range(2):
        # get axes #
        col = i
        ax  = axs[row,col]
        ret = ax.pcolormesh(xx,yy,results[i], vmin=vmin, vmax=vmax, shading='gouraud', antialiased=True, cmap='bwr_r')
        fig.colorbar(ret,ax=ax)

        if row == 3:
            ax.set_xlabel("Branch Length")

        if col == 0:
            ax.set_ylabel("%s\nIndel Rate" % err_types[row])

        if row == 0 and col == 0:
            ax.set_title("Sequence Alignment")
        elif row == 0 and col == 1:
            ax.set_title("Integrated Alignment")

#plt.savefig("FIG.pdf", dpi=300)
plt.show()
