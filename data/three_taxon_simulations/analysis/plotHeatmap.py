#!/usr/bin/env python3

import sys
import numpy as np
import scipy.interpolate
import matplotlib
import matplotlib.pyplot as plt

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


def getData(fname, column):

    dx = 0.1
    dy = 0.01

    XY = []
    C = []

    handle = open(fname, "r")
    handle.readline()
    for line in handle:
        linearr = [ float(x) for x in line.strip().split(",") ]
        brlen  = linearr[0]
        indelr = linearr[1]
        data   = linearr[column]
        XY.append([brlen,indelr])
        C.append(data)
    handle.close()
    return (XY,C)

fname = sys.argv[1]


fig, axs = plt.subplots(nrows=3,ncols=3,sharex=True,sharey=True,figsize=(6.5,5.5))
the_axs = []

for i in range(len(alnmethods)):
    alnmethod = alnmethods[i]

    # get results #
    (xy,c) = getData(fname, startindex+i)
    xx,yy = np.meshgrid(np.arange(0.1,0.81,0.01),np.arange(0.01,0.081,0.001))
    grid_x, grid_y = np.mgrid[0:1:100j, 0:1:100j]
    zz = scipy.interpolate.griddata(xy,c, (xx,yy), method='cubic')

    # get axes #
    col = i//3
    row = i%3
    ax  = axs[row,col]
    the_axs.append(ax)
    ret = ax.pcolormesh(xx,yy,zz, vmin=0.0, vmax=0.1, shading='gouraud', antialiased=True, cmap='plasma')
    ax.set_title(alnmethod)
    fig.colorbar(ret,ax=ax)

    if row == 2:
        ax.set_xlabel("Branch Length")

    if col == 0:
        ax.set_ylabel("Indel Rate")

#fig.colorbar(ret, ax=axs, location='right')
plt.show()
