#!/usr/bin/env python3

import sys
import matplotlib
import matplotlib.pyplot as plt

nodenums  = []
nodedists = []
alns      = []
alnerrs   = []

BEG = 4
END = 14

handle = open(sys.argv[1], "r")

line = handle.readline()
linearr = line.strip().split(",")
for i in range(BEG,END):
    alns.append(linearr[i])

indx = 1
for line in handle:
    linearr = line.strip().split(",")
    nodedists.append(float(linearr[3]))
    nodenums.append(indx)
    indx += 1
    ndata = []
    for i in range(BEG,END):
        ndata.append(float(linearr[i]))
    alnerrs.append(ndata)
handle.close()

def getkey(item):
    return "%.4f_%.4f_%.4f" % (item[-2], item[-3], item[-1])

# sort by integrated alignment error rate #
sorted_alnerrs = sorted(alnerrs, key=getkey)

# now separate sorted alignment errors into series #
series_alnerrs = []
for a in alns:
    series_alnerrs.append([])
for x in sorted_alnerrs:
    for i in range(len(x)):
        series_alnerrs[i].append(x[i])

#plt.figure(figsize=(3,1.5))
plt.figure(figsize=(16,6))

plt.subplot(1,1,1)

legendarr = []
for i in range(len(alns)):
    arr = series_alnerrs[i]
    lab = alns[i]
    hand, = plt.plot(nodenums,arr, label=lab, linewidth=0, marker='o', markersize=4, alpha=0.6, markeredgewidth=0, markevery=4)
    legendarr.append(hand)

plt.legend(handles=legendarr)

plt.xlabel("Node Number")
plt.ylabel("Expected Errors per Site")

plt.show()
