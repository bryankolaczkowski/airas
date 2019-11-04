#!/usr/bin/env python3

import sys
from scipy import stats

def parseAve(fname):
    type = fname.split(".")[1]

    count_same  = 0.0
    count_diff  = 0.0
    count_corr  = 0.0
    count_other = 0.0

    handle = open(fname, "r")
    handle.readline()
    for line in handle:
        linearr = line.strip().split(",")
        psame = float(linearr[-3])
        pdiff = float(linearr[-2])
        pcorr = float(linearr[-1])
        if pcorr >= 0.5:
            count_corr += 1
        elif pdiff >= 0.5:
            count_diff += 1
        elif psame >= 0.5:
            count_same += 1
        else:
            count_other += 1
    handle.close()

    total = count_same + count_diff + count_corr + count_other

    count_same /= total
    count_diff /= total
    count_corr /= total
    count_other /= total

    sys.stdout.write("%s,%.4f,%.4f,%.4f,%.4f\n" % (type,count_corr,count_diff,count_same,count_other))


sys.stdout.write("ErrType,Majority_correct,Majority_different,Majority_same,Other\n")

for fname in sys.argv[1:]:
    parseAve(fname)
