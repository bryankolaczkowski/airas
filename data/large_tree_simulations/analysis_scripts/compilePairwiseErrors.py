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

    handle = open("../%s.pairwiseErrors.csv" % protein, "r")
    handle.readline()
    for line in handle:
        linearr = line.strip().split(",")
        alignment  = linearr[0]
        if alignment.find(".fasta") > -1:
            alignment = alignment.split(".fasta")[0]
        node       = linearr[2]
        alnlen     = float(linearr[3])
        res_errs   = float(linearr[4]) / alnlen
        ins_errs   = float(linearr[5]) / alnlen
        del_errs   = float(linearr[6]) / alnlen

        all_errs   = ( float(linearr[4]) + float(linearr[5]) + float(linearr[6]) ) / alnlen

        id = node + "|" + alignment

        if id not in results.keys():
            results[id] = [ [],[],[],[] ]

        results[id][0].append(all_errs)
        results[id][1].append(res_errs)
        results[id][2].append(ins_errs)
        results[id][3].append(del_errs)
    handle.close()

    # print results #
    outf = open("../%s.compiledPairwiseErrors.csv" % protein, "w")
    outf.write("node,branchLength,distFromRoot,nodesFromRoot,alignment,AllErrors,ResErrors,InsErrors,SEAllErrors,SEResErrors,SEInsErrors,SEDelErrors\n")
    for id in results.keys():
        node = id.split("|")[0]
        alignment = id.split("|")[1]
        (blen, blen_dist, node_dist) = root_dists[node]
        outf.write("%s,%s,%s,%s,%s," % (node,blen,blen_dist,node_dist,alignment))

        result = results[id]

        all_errs    = 0.0
        res_errs    = 0.0
        ins_errs    = 0.0
        del_errs    = 0.0

        # do the calculations... #
        while len(result[0]) < 10:
            result[0].append(0.0)
        all_errs = sum(result[0])/len(result[0])
        SEall_errs = stats.sem(result[0])

        while len(result[1]) < 10:
            result[1].append(0.0)
        res_errs = sum(result[1])/len(result[1])
        SEres_errs  = stats.sem(result[1])

        while len(result[2]) < 10:
            result[2].append(0.0)
        ins_errs = sum(result[2])/len(result[2])
        SEins_errs  = stats.sem(result[2])

        while len(result[3]) < 10:
            result[3].append(0.0)
        del_errs = sum(result[3])/len(result[3])
        SEdel_errs  = stats.sem(result[3])

        outf.write("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n" % (all_errs,res_errs,ins_errs,del_errs, SEall_errs,SEres_errs,SEins_errs,SEdel_errs))

    outf.close()
