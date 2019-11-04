#!/usr/bin/env python3

import sys
from scipy.stats import gaussian_kde, entropy, sem
import numpy
import matplotlib
import matplotlib.pyplot as plt

# 5 = P(error)
# 6 = P(correct)
# 7 = diff(correct-error)
data_col = 6

def getHighestMode(x,y):
    max_y = -1.0
    max_x = -1.0
    for i in range(len(x)):
        if y[i] > max_y:
            max_y = y[i]
            max_x = x[i]
    return max_x

types = ["all", "res", "ins", "del"]

# set up plot for kernel densities #
fig,ax = plt.subplots(nrows=len(types), ncols=1, sharex=False, sharey=False, figsize=(3,7))
fig.suptitle('Posterior Probability of Correct State')

index = 0
for type in types:
    alns      = []
    alnerrs   = []
    kernelds  = []

    max_error = -1.0
    min_error = 100000.0

    for intfixed in ["True", "False"]:
        fname = "BalProbReports/IntFixed.%s.%s.csv" % (type, intfixed)
        alns.append(intfixed)
        alnerrs.append([])

        my_index = 1
        if intfixed == "True":
            my_index = 0

        handle = open(fname, "r")
        handle.readline()
        for line in handle:
            linearr = line.strip().split(",")
            r = float(linearr[data_col])
            alnerrs[my_index].append(r)
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

    # calculate kernel densities #
    for errorarray in alnerrs:
        kernel = gaussian_kde(errorarray)
        kernelds.append(kernel.pdf(ndX))

    longest_aln_name_len = 0
    for s in alns:
        slen = len(s)
        if slen > longest_aln_name_len:
            longest_aln_name_len = slen

    # print mean error rate   #
    # print median error rate #
    # print highest mode      #
    sys.stdout.write("%s\n" % fname)
    sys.stdout.write("alignment ,meanErrorRate ,medianErrorRate ,highestMode ,SEmean ,maxY\n")
    for i in range(len(alns)):
        aln    = alns[i]
        alndiff = longest_aln_name_len - len(aln)
        for j in range(alndiff):
            aln += " "
        pdf    = kernelds[i]
        mode   = getHighestMode(ndX,pdf)
        mean   = sum(alnerrs[i])/len(alnerrs[i])
        median = numpy.median(alnerrs[i])
        stderr = sem(alnerrs[i])
        maxY   = max(pdf)
        sys.stdout.write("%s ,%.4e ,%.4e ,%.4e ,%.4e ,%.4e\n" % (aln,mean,median,mode,stderr,maxY))

    myaxs = ax[index]

    legendarr = []
    for i in range(len(alns)):
        if alns[i] == "True":
            lab = "Alignment-Integration Correct"
        else:
            lab = "Alignment-Integration Incorrect"
        den = kernelds[i]
        hand, = myaxs.plot(ndX, den, label=lab, linewidth=1, alpha=1.0)
        myaxs.fill_between(ndX, 0, den, alpha=0.01)
        legendarr.append(hand)

    if index == 0:
        myaxs.legend(handles=legendarr)

    #myaxs.set_xlim([-1.0,0.5])
    thelab = fname.split(".")[1]
    mylab  = ""
    if thelab == "all":
        mylab = "Total Errors"
    #    myaxs.set_xlim([0.0,1.0])
    #    myaxs.set_ylim([0.0,20.0])
    elif thelab == "res":
        mylab = "Residue Errors"
    #    myaxs.set_xlim([0.0,1.0])
    #    myaxs.set_ylim([0.0,15.0])
    elif thelab == "ins":
        mylab = "Insertion Errors"
    #    myaxs.set_xlim([0.0,1.0])
    #    myaxs.set_ylim([0.0,30.0])
    elif thelab == "del":
        mylab = "Deletion Errors"
    #    myaxs.set_xlim([0.0,1.0])
    #    myaxs.set_ylim([0.0,15.0])

    myaxs.set_xlabel("%s" % mylab)
    myaxs.set_ylabel("Kernel Density")

    index += 1


plt.show()
