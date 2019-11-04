#!/usr/bin/env python3

import sys
import glob
from ete3 import Tree

proteins = ["CARD1", "DSRM1", "DSRM2", "DSRM3", "RD1"]

for protein in proteins:
    fname = "../%s/brlens_and_labels.tre" % protein
    tre = Tree(fname, format=1)

    outf = open("../%s/dists_from_root.csv" % protein, "w")
    outf.write("Node,branchLength,DistFromRoot,NodesFromRoot\n")

    for node in tre.traverse("preorder"):
        id   = node.name
        blen = node.dist
        dist_from_root  = tre.get_distance(node)
        nodes_from_root = tre.get_distance(node, topology_only=True)
        outf.write("%s,%f,%f,%d\n" % (id,blen,dist_from_root,nodes_from_root))
    outf.close()
