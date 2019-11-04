#!/usr/bin/env python3

import sys

if len(sys.argv) < 3:
    sys.stderr.write("usage: %s protein errtype\n" % sys.argv[0])
    sys.stderr.write("  where protein = CARD1 | DSRM1 | DSRM2 | DSRM3 | RD1\n")
    sys.stderr.write("    and errtype = all | res | ins | del\n")
    sys.exit(1)

alignments = [  "aligned_clustalw",
                "aligned_mafft",
                "aligned_msaprobs",
                "aligned_muscle",
                "aligned_probalign",
                "aligned_probcons",
                "aligned_tcoffee",
                "structaligned",
                "correctaligned",
                "integratedaln"     ]

protein = sys.argv[1]
errtype = sys.argv[2]

base_index = 0
index_inc  = 4
if errtype == "all":
    base_index = 0
elif errtype == "res":
    base_index = 1
elif errtype == "ins":
    base_index = 2
elif errtype == "del":
    base_index = 3

# write output header #
sys.stdout.write("node,branchLength,distFromRoot,nodesFromRoot")
for aln in alignments:
    sys.stdout.write(",%s" % aln)
for aln in alignments:
    sys.stdout.write(",SE%s" % aln)


results = {}
handle = open("../%s.compiledPairwiseErrors.csv" % protein, "r")
handle.readline()
for line in handle:
    linearr = line.strip().split(",")
    node = linearr[0]
    blen = float(linearr[1])
    blen_dist = float(linearr[2])
    node_dist = int(linearr[3])

    if node not in results.keys():
        results[node] = [(blen,blen_dist,node_dist), {}]

    alignment = linearr[4]

    data = [float(x) for x in linearr[5:]]
    err     = data[base_index]
    SEerr   = data[base_index + index_inc]

    results[node][1][alignment] = (err, SEerr)
handle.close()

for node in results.keys():
    (blen,blen_dist,node_dist) = results[node][0]
    sys.stdout.write("%s,%.4f,%.4f,%d" % (node, blen,blen_dist,node_dist))
    alnres = results[node][1]

    for i in range(2):
        for aln in alignments:
            if aln not in alnres.keys():
                sys.stdout.write(",0.0")
            else:
                val = alnres[aln][i]
                sys.stdout.write(",%.4f" % val)
    sys.stdout.write("\n")
