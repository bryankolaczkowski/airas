#!/usr/bin/env python3

import sys
from scipy.stats import gaussian_kde, entropy, sem, tstd
import numpy
import matplotlib
import matplotlib.pyplot as plt

def getHighestMode(x,y):
    max_y = -1.0
    max_x = -1.0
    for i in range(len(x)):
        if y[i] > max_y:
            max_y = y[i]
            max_x = x[i]
    return max_x

# set up plot for kernel densities #
fig,ax = plt.subplots(nrows=1, ncols=len(sys.argv[1:]), sharex=False, sharey=False, figsize=(6.5,2.5))

index = 0
for fname in sys.argv[1:]:
    alnerrs   = []
    kernelds  = []

    max_error = -1.0
    min_error = 100000.0

    handle = open(fname, "r")
    handle.readline()

    for line in handle:
        linearr = line.strip().split(",")
        if linearr[0] != "correctaligned":
            continue
        valarr  = [float(x) for x in linearr[3:]]
        for r in valarr:
            alnerrs.append(r)
            if r > max_error:
                max_error = r
            if r < min_error:
                min_error = r
    handle.close()

    # calculate X axis #
    ndX = []
    SCALE = 500
    for i in range(SCALE+1):
        ndX.append(min_error + ((max_error-min_error)/SCALE)*i)

    # calculate kernel density #
    kernel   = gaussian_kde(alnerrs)
    kernelds = kernel.pdf(ndX)


    # print mean error rate   #
    # print median error rate #
    # print highest mode      #
    sys.stdout.write("%s\n" % fname)
    sys.stdout.write("meanDistance ,medianDistance ,highestMode ,StDev ,SEmean ,maxAbs\n")

    aln    = alnerrs
    pdf    = kernelds
    mode   = getHighestMode(ndX,pdf)
    mean   = sum(aln)/len(aln)
    median = numpy.median(aln)
    stdev  = tstd(aln)
    stderr = sem(aln)
    maxX   = max(aln)
    sys.stdout.write("%.4e ,%.4e ,%.4e ,%.4e ,%.4e ,%.4e\n" % (mean,median,mode,stdev,stderr,maxX))

    myaxs = ax[index]

    hand, = myaxs.plot(ndX, kernelds, linewidth=1)
    myaxs.fill_between(ndX, 0, kernelds, alpha=0.01)



    mylab  = ""
    if fname == "RESULTS_dgrem.csv":
        mylab = "Structural Stability"
#        myaxs.set_xlim([0.0,0.1])
#        myaxs.set_ylim([0.0,50.0])
    elif fname == "RESULTS_pkd.csv":
        mylab = "Binding Affinity"
#        myaxs.set_xlim([0.0,2.0])
#        myaxs.set_ylim([0.0,100.0])

    myaxs.set_xlabel("%s Value" % mylab)
    myaxs.set_ylabel("Kernel Density")

    index += 1


plt.show()
