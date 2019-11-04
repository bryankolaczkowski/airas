#!/usr/bin/env python3

import sys
import numpy as np
import scipy.interpolate
import matplotlib
import matplotlib.pyplot as plt

alnmethods = ["all", "res", "ins", "del"]
labels = ["Total Errors", "Residue Errors", "Insertion Errors", "Deletion Errors"]

theindex = 4


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

fig, axs = plt.subplots(nrows=4,ncols=2,sharex=False,sharey='col',figsize=(3,4.5))


for i in range(len(alnmethods)):
    alnmethod = alnmethods[i]

    # get results #
    fname = "IntCorrReport.%s.ave.csv" % alnmethod
    (xy,c) = getData(fname, theindex)
    xx,yy = np.meshgrid(np.arange(0.1,0.81,0.01),np.arange(0.01,0.081,0.001))
    grid_x, grid_y = np.mgrid[0:1:100j, 0:1:100j]
    zz = scipy.interpolate.griddata(xy,c, (xx,yy), method='cubic')

    # get axes #
    ax  = axs[i,0]
    ret = ax.pcolormesh(xx,yy,zz, vmin=0.5, vmax=0.9, shading='gouraud', antialiased=True, cmap='plasma')
    ax.set_title(labels[i])
    fig.colorbar(ret,ax=ax)

    if i == 3:
        ax.set_xlabel("Branch Length")

    ax.set_ylabel("Indel Rate")



piesizes = {}
handle = open("IntProps.report.csv", "r")
handle.readline()
for line in handle:
    linearr = line.strip().split(",")
    id = linearr[0]
    sizes = [ float(x)*10.0 for x in linearr[1:] ]
    piesizes[id] = sizes
handle.close()

for i in range(len(alnmethods)):
    sizes = piesizes[alnmethods[i]]
    ax = axs[i,1]
    ax.pie(sizes, labels=['correct', 'different', 'same', 'other'])
    ax.axis('equal')

fig.tight_layout()
plt.show()
