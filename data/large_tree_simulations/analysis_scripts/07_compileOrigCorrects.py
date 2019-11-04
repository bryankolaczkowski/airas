#!/usr/bin/env python3

import sys
from scipy import stats

proteins = ["CARD1", "DSRM1", "DSRM2", "DSRM3", "RD1"]

for protein in proteins:

    # read in phylogenetic distances #
    root_dists = {}
    handle = open("../%s/dists_from_root.csv" % protein, "r")
    handle.readline()
    for line in handle:
        linearr = line.strip().split(",")
        node  = linearr[0]
        blen  = linearr[1]
        bdist = linearr[2]
        ndist = linearr[3]
        root_dists[node] = (blen,bdist,ndist)
    handle.close()

    # read in errors #
    results = {}

    handle = open("../%s.origCorrects.csv" % protein, "r")
    handle.readline()
    for line in handle:
        linearr = line.strip().split(",")
        alignment  = linearr[0]
        node       = linearr[2]
        alnlen     = float(linearr[3])
        res_cors   = float(linearr[4]) / alnlen
        gap_cors   = float(linearr[5]) / alnlen
        res_cor_PP = float(linearr[6])
        gap_cor_PP = float(linearr[7])

        all_cors   = ( float(linearr[4]) + float(linearr[5]) ) / alnlen
        all_cor_PP = ( res_cor_PP * float(linearr[4]) + gap_cor_PP * float(linearr[5]) ) / ( float(linearr[4]) + float(linearr[5]) )

        id = node + "|" + alignment

        if id not in results.keys():
            results[id] = [ [],[],[], [],[],[] ]

        results[id][0].append(all_cors)
        results[id][1].append(res_cors)
        results[id][2].append(gap_cors)

        if all_cors > 1.0e-6:
            results[id][3].append(all_cor_PP)

        if res_cors > 1.0e-6:
            results[id][4].append(res_cor_PP)

        if gap_cors > 1.0e-6:
            results[id][5].append(gap_cor_PP)

    handle.close()

    # print results #
    outf = open("../%s.compiledCorrects.csv" % protein, "w")
    outf.write("node,branchLength,distFromRoot,nodesFromRoot,alignment,AllCorrects,ResCorrects,GapCorrects,meanPP_AllCorrects,meanPP_ResCorrects,meanPP_GapCorrects,SEAllCorrects,SEResCorrects,SEGapCorrects,SEmeanPP_AllCorrects,SEmeanPP_ResCorrects,SEmeanPP_GapCorrects\n")
    for id in results.keys():
        node = id.split("|")[0]
        alignment = id.split("|")[1]
        (blen, blen_dist, node_dist) = root_dists[node]
        outf.write("%s,%s,%s,%s,%s," % (node,blen,blen_dist,node_dist,alignment))

        result = results[id]

        all_cors    = 0.0
        all_corPP   = 0.0
        SEall_cors  = 0.0
        SEall_corPP = 0.0

        res_cors    = 0.0
        res_corPP   = 0.0
        SEres_cors  = 0.0
        SEres_corPP = 0.0

        gap_cors    = 0.0
        gap_corPP   = 0.0
        SEgap_cors  = 0.0
        SEgap_corPP = 0.0

        # do the calculations... #
        while len(result[0]) < 10:
            result[0].append(0.0)
        all_cors = sum(result[0])/len(result[0])
        if all_cors > 1.0e-6:
            all_corPP = sum(result[3])/len(result[3])
            if len(result[0]) > 2:
                SEall_cors  = stats.sem(result[0])
            if len(result[3]) > 2:
                SEall_corPP = stats.sem(result[3])

        while len(result[1]) < 10:
            result[1].append(0.0)
        res_cors = sum(result[1])/len(result[1])
        if res_cors > 1.0e-6:
            res_corPP = sum(result[4])/len(result[4])
            if len(result[1]) > 2:
                SEres_cors  = stats.sem(result[1])
            if len(result[4]) > 2:
                SEcor_PP = stats.sem(result[4])

        while len(result[2]) < 10:
            result[2].append(0.0)
        gap_cors = sum(result[2])/len(result[2])
        if gap_cors > 1.0e-6:
            gap_corPP = sum(result[5])/len(result[5])
            if len(result[2]) > 2:
                SEgap_cors  = stats.sem(result[2])
            if len(result[5]) > 2:
                SEgap_corPP = stats.sem(result[5])

        outf.write("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n" % (all_cors,res_cors,gap_cors, all_corPP,res_corPP,gap_corPP, SEall_cors,SEres_cors,SEgap_cors, SEall_corPP,SEres_corPP,SEgap_corPP))

    outf.close()
