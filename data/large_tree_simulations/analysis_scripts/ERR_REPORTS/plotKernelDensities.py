#!/usr/bin/env python3

import sys
from scipy.stats import gaussian_kde, entropy, sem
import numpy
import matplotlib
import matplotlib.pyplot as plt

nodedists = []
alns      = []
alnerrs   = []
kernelds  = []

max_error = -1.0
min_error = 100000.0

BEG = 4
END = 14

def getHighestMode(x,y):
    max_y = -1.0
    max_x = -1.0
    for i in range(len(x)):
        if y[i] > max_y:
            max_y = y[i]
            max_x = x[i]
    return max_x


handle = open(sys.argv[1], "r")

line = handle.readline()
linearr = line.strip().split(",")
for i in range(BEG,END):
    alns.append(linearr[i])
    alnerrs.append([])

for line in handle:
    linearr = line.strip().split(",")
    nodedists.append(float(linearr[3]))
    for i in range(BEG,END):
        r = float(linearr[i])
        alnerrs[i-BEG].append(r)
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
sys.stdout.write("alignment ,meanErrorRate ,medianErrorRate ,highestMode ,SEmean\n")
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
    sys.stdout.write("%s ,%.4e ,%.4e ,%.4e ,%.4e\n" % (aln,mean,median,mode,stderr))

# plot kernel densities #
plt.figure(figsize=(9,7))

plt.subplot(1,1,1)

legendarr = []
for i in range(len(alns)):
    lab = alns[i]
    den = kernelds[i]
    if i > (END-BEG)-4:
        hand, = plt.plot(ndX, den, label=lab, linewidth=2)
        plt.fill_between(ndX, 0, den, alpha=0.05)
    else:
        hand, = plt.plot(ndX, den, label=lab, linewidth=1, linestyle=':', alpha=0.5)
        plt.fill_between(ndX, 0, den, alpha=0.01)
    legendarr.append(hand)

plt.legend(handles=legendarr)

plt.xlabel("Error Rate")
plt.ylabel("Kernel Density")

plt.show()
