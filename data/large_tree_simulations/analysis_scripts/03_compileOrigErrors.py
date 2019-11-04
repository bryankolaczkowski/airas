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

    handle = open("../%s.origErrors.csv" % protein, "r")
    handle.readline()
    for line in handle:
        linearr = line.strip().split(",")
        alignment  = linearr[0]
        node       = linearr[2]
        alnlen     = float(linearr[3])
        res_errs   = float(linearr[4]) / alnlen
        ins_errs   = float(linearr[5]) / alnlen
        del_errs   = float(linearr[6]) / alnlen
        res_err_PP = float(linearr[7])
        ins_err_PP = float(linearr[8])
        del_err_PP = float(linearr[9])
        res_cor_PP = float(linearr[10])
        ins_cor_PP = float(linearr[11])
        del_cor_PP = float(linearr[12])

        all_errs   = ( float(linearr[4]) + float(linearr[5]) + float(linearr[6]) ) / alnlen

        all_err_PP = 0.0
        all_cor_PP = 0.0

        all_err_PP = ( res_err_PP * float(linearr[4]) + ins_err_PP * float(linearr[5]) + del_err_PP * float(linearr[6]) ) / ( float(linearr[4]) + float(linearr[5]) + float(linearr[6]) )
        all_cor_PP = ( res_cor_PP * float(linearr[4]) + ins_cor_PP * float(linearr[5]) + del_cor_PP * float(linearr[6]) ) / ( float(linearr[4]) + float(linearr[5]) + float(linearr[6]) )

        id = node + "|" + alignment

        if id not in results.keys():
            results[id] = [ [],[],[],[], [],[],[],[], [],[],[],[] ]

        results[id][0].append(all_errs)
        results[id][1].append(res_errs)
        results[id][2].append(ins_errs)
        results[id][3].append(del_errs)

        if all_errs > 1.0e-6:
            results[id][4].append(all_err_PP)
            results[id][8].append(all_cor_PP)

        if res_errs > 1.0e-6:
            results[id][5].append(res_err_PP)
            results[id][9].append(res_cor_PP)

        if ins_errs > 1.0e-6:
            results[id][6].append(ins_err_PP)
            results[id][10].append(ins_cor_PP)

        if del_errs > 1.0e-6:
            results[id][7].append(del_err_PP)
            results[id][11].append(del_cor_PP)

    handle.close()

    # print results #
    outf = open("../%s.compiledErrors.csv" % protein, "w")
    outf.write("node,branchLength,distFromRoot,nodesFromRoot,alignment,AllErrors,ResErrors,InsErrors,DelErrors,meanPP_AllErrors,meanPP_ResErrors,meanPP_InsErrors,meanPP_DelErrors,corrPP_AllErrors,corrPP_ResErrors,corrPP_InsErrors,corrPP_DelErrors,SEAllErrors,SEResErrors,SEInsErrors,SEDelErrors,SEmeanPP_AllErrors,SEmeanPP_ResErrors,SEmeanPP_InsErrors,SEmeanPP_DelErrors,SEcorrPP_AllErrors,SEcorrPP_ResErrors,SEcorrPP_InsErrors,SEcorrPP_DelErrors\n")
    for id in results.keys():
        node = id.split("|")[0]
        alignment = id.split("|")[1]
        (blen, blen_dist, node_dist) = root_dists[node]
        outf.write("%s,%s,%s,%s,%s," % (node,blen,blen_dist,node_dist,alignment))

        result = results[id]

        all_errs    = 0.0
        all_errPP   = 0.0
        all_corPP   = 0.0
        SEall_errs  = 0.0
        SEall_errPP = 0.0
        SEall_corPP = 0.0

        res_errs    = 0.0
        res_errPP   = 0.0
        res_corPP   = 0.0
        SEres_errs  = 0.0
        SEres_errPP = 0.0
        SEres_corPP = 0.0

        ins_errs    = 0.0
        ins_errPP   = 0.0
        ins_corPP   = 0.0
        SEins_errs  = 0.0
        SEins_errPP = 0.0
        SEins_corPP = 0.0

        del_errs    = 0.0
        del_errPP   = 0.0
        del_corPP   = 0.0
        SEdel_errs  = 0.0
        SEdel_errPP = 0.0
        SEdel_corPP = 0.0

        # do the calculations... #
        while len(result[0]) < 10:
            result[0].append(0.0)
        all_errs = sum(result[0])/len(result[0])
        if all_errs > 1.0e-6:
            all_errPP   = sum(result[4])/len(result[4])
            all_corPP   = sum(result[8])/len(result[8])
            if len(result[0]) > 2:
                SEall_errs  = stats.sem(result[0])
            if len(result[4]) > 2:
                SEall_errPP = stats.sem(result[4])
            if len(result[8]) > 2:
                SEall_corPP = stats.sem(result[8])

        while len(result[1]) < 10:
            result[1].append(0.0)
        res_errs = sum(result[1])/len(result[1])
        if res_errs > 1.0e-6:
            res_errPP   = sum(result[5])/len(result[5])
            res_corPP   = sum(result[9])/len(result[9])
            if len(result[1]) > 2:
                SEres_errs  = stats.sem(result[1])
            if len(result[5]) > 2:
                SEres_errPP = stats.sem(result[5])
            if len(result[9]) > 2:
                SEres_corPP = stats.sem(result[9])

        while len(result[2]) < 10:
            result[2].append(0.0)
        ins_errs = sum(result[2])/len(result[2])
        if ins_errs > 1.0e-6:
            ins_errPP   = sum(result[6])/len(result[6])
            ins_corPP   = sum(result[10])/len(result[10])
            if len(result[2]) > 2:
                SEins_errs  = stats.sem(result[2])
            if len(result[6]) > 2:
                SEins_errPP = stats.sem(result[6])
            if len(result[10]) > 2:
                SEins_corPP = stats.sem(result[10])

        while len(result[3]) < 10:
            result[3].append(0.0)
        del_errs = sum(result[3])/len(result[3])
        if del_errs > 1.0e-6:
            del_errPP   = sum(result[7])/len(result[7])
            del_corPP   = sum(result[11])/len(result[11])
            if len(result[3]) > 2:
                SEdel_errs  = stats.sem(result[3])
            if len(result[7]) > 2:
                SEdel_errPP = stats.sem(result[7])
            if len(result[11]) > 2:
                SEdel_corPP = stats.sem(result[11])

        outf.write("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n" % (all_errs,res_errs,ins_errs,del_errs, all_errPP,res_errPP,ins_errPP,del_errPP, all_corPP,res_corPP,ins_corPP,del_corPP,SEall_errs,SEres_errs,SEins_errs,SEdel_errs, SEall_errPP,SEres_errPP,SEins_errPP,SEdel_errPP, SEall_corPP,SEres_corPP,SEins_corPP,SEdel_corPP))

    outf.close()
