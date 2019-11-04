#!/usr/bin/python

import sys

if len(sys.argv) < 3:
	sys.stderr.write("usage: getTree_BLandASRlabels.py BL.tre ASRlabels.tre\n")
	sys.stderr.write("where:\n")
	sys.stderr.write("    BL.tre is a tree with branch length information\n")
	sys.stderr.write("    ASRlabels.tre is the same tree with labeled ancestral nodes\n")
	sys.stderr.write("prints a combined tree with branch lengths and node labels\n")
	sys.stderr.write("to standard out\n")
	sys.exit(1)

# need to point to the tree with branch lengths and the labelled tree #
BL_TREE = sys.argv[1]
LA_TREE = sys.argv[2]

#  we need to parse both the 
#  node-labelled tree - which has labels but no branch lengths, and the
#  ML tree - which has branch lengths but no labels
#
handle = open(LA_TREE, "r")
nodetree = ""
for line in handle:
	nodetree += line.strip()
handle.close()

handle = open(BL_TREE, "r")
brlentree = ""
for line in handle:
	brlentree += line.strip()
handle.close()

# parse trees
structurals = ["(",")",",",":",";"]
numericals  = ["0","1","2","3","4","5","6","7","8","9",".","e","E","-"]
i1 = 0
i2 = 0
while i1 < len(nodetree):
	if nodetree[i1] in structurals:
		sys.stdout.write(nodetree[i1])
		i1 += 1
	else:
		label = ""
		while nodetree[i1] not in structurals:
			label += nodetree[i1]
			i1 += 1
		# get branch length #
		while i2 < len(brlentree) and brlentree[i2] != ":":
			i2 +=1
		brlenstr = ""
		i2 += 1
		while i2 < len(brlentree) and brlentree[i2] in numericals:
			brlenstr += brlentree[i2]
			i2 += 1
		# print labelled information #
		if brlenstr == "":
			brlenstr = "0.0"
		sys.stdout.write("%s:%s" % (label,brlenstr))
		
sys.stdout.write("\n")

