#!/usr/bin/python

import sys
import os

swbase = "airas"

if len(sys.argv) < 3:
	sys.stderr.write("Usage: %s.py tree.tre [-e] aln1.fasta [-e] aln2.fasta [[-e] aln3.fasta...] [-c correct.ancs.fasta\n" % swbase)
	sys.stderr.write("  where tree.tre is a phylogeny in newick format\n")
	sys.stderr.write("    and alnK.fasta are different alignments of the same sequences in the tree\n\n")
	sys.stderr.write("  Reconstructs ancestral sequences at every node on the input tree\n")
	sys.stderr.write("  integrating over the input alignments. Additionally maps all the alignments\n")
	sys.stderr.write("  to one another, and calculates ancestral sequences on each individual\n")
	sys.stderr.write("  alignment.\n\n")
	sys.stderr.write("  The optional '-e' flag indicates the following alignment should be excluded\n")
	sys.stderr.write("  from the integrated sequence reconstruction, although it is still mapped\n")
	sys.stderr.write("  to the other alignments, and ancestral sequences are calculated on it. You\n")
	sys.stderr.write("  should specify at least 2 alignments without the -e flag to get an integrated\n")
	sys.stderr.write("  reconstruction. Otherwise, you will only get reconstructions on each\n")
	sys.stderr.write("  individual alignment.\n\n")
	sys.stderr.write("  The optional '-c' flag indicates that the following alignment contains the correct\n")
	sys.stderr.write("  ancestral sequences (ie, they were simulated or otherwise recorded). This alignment\n")
	sys.stderr.write("  is mapped to the others, but no ancestral sequences are calculated using it. You\n")
	sys.stderr.write("  should only flag one alignment with '-c'; if there are multiples, only the last\n")
	sys.stderr.write("  one will be included.\n")
	sys.exit(1)
	
################################################
#  constants defining where to find necessary  #
#  applications on your system.                #
#  You can also add global options here, to    #
#  control program behavior.                   #
#                                              #
RAXML = "raxmlHPC"
MAFFT = "mafft"

## for debugging, you can turn off the RAxML and/or MAFFT program execution  ##
## the program will then only work if you have pre-computed files from these ##
## programs                                                                  ## 
RUN_RAXML = True
RUN_MAFFT = True

#####################################################
#  function for converting an amino-acid algnment   #
#  into a 1/0 presence-absence alignment for indel  #
#  reconstruction                                   #
#                                                   #
#  Returns the name of the 1/0 alignment file       #
#                                                   #
def convert_zero_one(alnfname):
	outfname = alnfname + ".indelaln"
	handle   = open(alnfname, "r")
	outf     = open(outfname, "w")
	line = handle.readline()
	while line:
		if line[0] == ">":
			sid = line[1:].strip()
			seq = ""
			line = handle.readline()
			while line and line[0] != ">":
				seq += line.strip()
				line = handle.readline()
			# convert to 0-1 matrix #
			indelseq = ""
			for c in seq:
				if c == "-":
					indelseq += "0"
				else:
					indelseq += "1"
			outf.write(">%s\n%s\n" % (sid, indelseq))
	handle.close()
	outf.close()
	return outfname
	
###########################################################
#  function for converting RAxML posterior probability    #
#  distributions into a comma-separated format. Also      #
#  incorporates indel reconstruction and missing columns  #
#                                                         #
#  Returns the name of the comma-separated results file   #
#                                                         #
def parse_sub_aln_pps(seq_aln_fname, gap_aln_fname, missing_col_fname, out_basename):
	resultsfname = swbase + "_RESULTS_" + out_basename + ".asr.csv"

	# first read in missing column list #
	missing_cols = set([])
	handle = open(missing_col_fname, "r")
	for line in handle:
		missing_cols.add(int(line))
	handle.close()
	
	# read in probability of gap #
	gap_probs = {}
	handle = open("RAxML_marginalAncestralProbabilities.%s" % gap_aln_fname, "r")
	line = handle.readline()
	while line:
		nodenum = line.strip()
		gap_probs[nodenum] = []
		line = handle.readline().strip()
		index = 0
		while line and line != "":
			if index in missing_cols:
				gap_probs[nodenum].append(1.0)
				index += 1
			else:
				pgap = float(line.split()[0])
				gap_probs[nodenum].append(pgap)
				index += 1
				line = handle.readline().strip()
		line = handle.readline()  # skip to the next node id #
	handle.close()
	
	# read in sequence probabilities and print the results file #
	resultsf = open(resultsfname, "w")
	resultsf.write("node,col,-,A,R,N,D,C,Q,E,G,H,I,L,K,M,F,P,S,T,W,Y,V\n")
	
	nodenum = ""
	index   = 0
	
	handle = open("RAxML_marginalAncestralProbabilities.%s" % seq_aln_fname, "r")
	line = handle.readline()
	while line:
		nodenum = line.strip()
		line = handle.readline().strip()
		index = 0
		while line and line != "":
			if index in missing_cols:
				resultsf.write("%s,%d,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0\n" % (nodenum,index))
				index += 1
			else:
				pgap     = gap_probs[nodenum][index]
				probstrs = line.split()
				resultsf.write("%s,%d,%f" % (nodenum,index,pgap))
				for s in probstrs:
					pres = float(s) * (1.0-pgap)
					resultsf.write(",%f" % pres)
				resultsf.write("\n")
				index += 1
				line = handle.readline().strip()
		# now we need to fill in any missing data at the end #
		while index in missing_cols:
			resultsf.write("%s,%d,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0\n" % (nodenum,index))
			index += 1
		line = handle.readline()  # skip to the next node id #
	handle.close()
	resultsf.close()
	
	return resultsfname
	
################################################
#  MAIN ROUTINE                                #
#                                              #
intreefname        = sys.argv[1]
inalnfnames        = []
excludedalnfnames  = []
correctasralnfname = ""

i = 2
while i < len(sys.argv):
	if sys.argv[i] == "-e":
		i += 1
		excludedalnfnames.append(sys.argv[i])
		inalnfnames.append(sys.argv[i])
		i += 1
	elif sys.argv[i] == "-c":
		i += 1
		correctasralnfname = sys.argv[i]
		inalnfnames.append(sys.argv[i])
		i += 1
	else:
		inalnfnames.append(sys.argv[i])
		i += 1

## copy the alignment files into the current directory,         ##
## renaming ids so they indicate which alignment they came from ##
excluded_aln_basicnames = []
input_aln_filenames     = []
orig_aln_basicnames     = []
orig_correct_basicname  = ""
filenum = 1
seqnum  = 1
found_filenames = set([])

mafft_mergetable_fname = swbase + "_mergetable.txt"
mergetablef            = open(mafft_mergetable_fname, "w")

mafft_mergeinput_aln_fname = swbase + "_metaalninput.fasta"
mergeinputf                = open(mafft_mergeinput_aln_fname, "w")

for afname in inalnfnames:
	basicname = afname
	if afname.find("/") != -1:
		basicname = afname.split("/")[-1]
		
	# check if name is a duplicate #
	if basicname in found_filenames:
		sys.stderr.write("I'm sorry, this program does not work with duplicate filenames,\n")
		sys.stderr.write("even if the files are in different directories.\n")
		sys.stderr.write("%s is a duplicate, please rename.\n" % basicname)
		sys.exit(1)
		
	found_filenames.add(basicname)
	
	# copy alignment into current directory, renaming sequence IDs #
	outfname = swbase + "_inputaln%d.fasta" % filenum
	filenum += 1
	
	handle = open(afname, "r")
	outf   = open(outfname, "w")
	line = handle.readline()
	while line:
		if line[0] == ">":
			sid = line[1:].strip() + "___" + basicname
			seq = ""
			line = handle.readline()
			while line and line[0] != ">":
				seq += line.strip()
				line = handle.readline()
			outs = ">%s\n%s\n" % (sid,seq)
			outf.write(outs)
			mergeinputf.write(outs)
			mergetablef.write(" %d" % seqnum)
			seqnum += 1
		else:
			line = handle.readline()
	mergetablef.write("\n")
	outf.close()
	handle.close()
	
	input_aln_filenames.append(outfname)
	orig_aln_basicnames.append(basicname)
	if afname in excludedalnfnames:
		excluded_aln_basicnames.append(basicname)
	if afname == correctasralnfname:
		orig_correct_basicname = basicname
	
mergeinputf.close()
mergetablef.close()
	
## use mafft to merge the input alignments into one big alignment ##
mafft_merged_aln_fname = swbase + "_metaalnoutput.fasta"
cmd = "%s --merge %s %s > %s" % (MAFFT, mafft_mergetable_fname, mafft_mergeinput_aln_fname, mafft_merged_aln_fname)
if RUN_MAFFT:
	os.system(cmd)

## extract sub-alignments from the mafft merged alignment, remove gap-only columns ##
## and keep track of which columns are removed from each sub-alignment. This will  ##
## be used later to combine ancestral sequence reconstructions from each sub-aln   ##
## Just dump the correct alignment to a standard file                              ##
handle = open(mafft_merged_aln_fname, "r")
line   = handle.readline()

raxml_input_alns   = []
raxml_missing_cols = []

for i in range(len(input_aln_filenames)):
	idtag        = orig_aln_basicnames[i]
	
	if idtag != orig_correct_basicname:
		outfname     = input_aln_filenames[i] + ".raxmlinaln"
		missingfname = input_aln_filenames[i] + ".missingcols"
	
		raxml_input_alns.append(outfname)
		raxml_missing_cols.append(missingfname)
	
	corr_ids  = []
	corr_seqs = []
	
	ids     = []
	seqs    = []
	newseqs = []

	# read in sub-alignment #
	idarr = line.strip().split("___")
	myid  = idarr[0][1:]
	mytag = idarr[1]
	while mytag == idtag:
		se = ""
		line = handle.readline()
		while line and line[0] != ">":
			se += line.strip()
			line = handle.readline()
		if idtag != orig_correct_basicname:
			ids.append(myid)
			seqs.append(se)
			newseqs.append("")
		else:
			corr_ids.append(myid)
			corr_seqs.append(se)
		if line:
			idarr = line.strip().split("___")
			myid  = idarr[0][1:]
			mytag = idarr[1]
		else:
			myid  = ""
			mytag = ""

	## print correct ancestral sequences, if they exist ##
	if idtag == orig_correct_basicname:
		corroutf = open(swbase + "_RESULTS_correct_anc_seqs_aligned.fasta", "w")
		for j in range(len(corr_ids)):
			corroutf.write(">%s\n%s\n" % (corr_ids[j],corr_seqs[j]))
		corroutf.close()
		continue

	# find all-gap columns and remove them from the sequences #
	# Note that RAxML does not like "X" for ASR, so we count  #
	# these 'undetermined' amino acids as "missing" for this  #
	# analysis                                                #
	# also save the indices of the missing columns            #
	outmisf = open(missingfname, "w")
	for j in range(len(seqs[0])):
		all_gaps = True
		for k in range(len(seqs)):
			if (seqs[k][j] != "-") and seqs[k][j] != "X":
				all_gaps = False
				break
		if all_gaps:
			outmisf.write("%d\n" % j)
		else:
			for k in range(len(seqs)):
				newseqs[k] += seqs[k][j]
	outmisf.close()
	
	# write alignment with all-gap cols removed #
	outseqf = open(outfname, "w")
	for j in range(len(ids)):
		outseqf.write(">%s\n%s\n" % (ids[j], newseqs[j]))
	outseqf.close()
	
	# write mapped alignment, including all-gap cols #
	outseqf = open(swbase + "_RESULTS_" + idtag + ".mappedaln.fasta", "w")
	for j in range(len(ids)):
		outseqf.write(">%s\n%s\n" % (ids[j], seqs[j]))
	outseqf.close()
	
handle.close()

raxml_input_presabs = []

## convert each raxml input file to presence/absence matrix ##
for f in raxml_input_alns:
	raxml_input_presabs.append(convert_zero_one(f))
	
## reconstruct ancestral sequences and ancestral indels for each sub-alignment ##
for i in range(len(raxml_input_alns)):
	seqaln   = raxml_input_alns[i]
	indelaln = raxml_input_presabs[i]
	# reconstruct sequences #
	cmd = "%s -f A -m PROTCATLGF -t %s -s %s -n %s" % (RAXML, intreefname, seqaln, seqaln)
	if RUN_RAXML:
		os.system(cmd)
	# reconstruct indels #
	cmd = "%s -f A -m BINCAT     -t %s -s %s -n %s" % (RAXML, intreefname, indelaln, indelaln)
	if RUN_RAXML:
		os.system(cmd)
	
## copy node-labelled tree to a 'standard' results file ##
os.system("cp RAxML_nodeLabelledRootedTree.%s %s_RESULTS_nodelabelledtree.tre" % (raxml_input_alns[0],swbase))
	
## parse individual sub-alignment ancestral probability distributions ##
ind_asr_files = []
for i in range(len(raxml_input_alns)):
	rfname = parse_sub_aln_pps(raxml_input_alns[i], raxml_input_presabs[i], raxml_missing_cols[i], orig_aln_basicnames[i])
	if orig_aln_basicnames[i] not in excluded_aln_basicnames:
		ind_asr_files.append(rfname)
	
## combine individual-alignment posterior probability distributions ##
outf = open(swbase + "_RESULTS_integratedaln.asr.csv", "w")

handles = []
for f in ind_asr_files:
	handles.append(open(f,"r"))

lines    = []
linearrs = []
header   = ""
for f in handles:
	header = f.readline()
	lines.append(f.readline())
	linearrs.append([])
	
outf.write(header)
	
while lines[0]:
	for i in range(len(handles)):
		linearrs[i] = lines[i].strip().split(",")
		
	node = linearrs[0][0]
	col  = linearrs[0][1]
	outf.write("%s,%s" % (node,col))
	
	for i in range(2,len(linearrs[0])):
		pp = 0.0
		for j in range(len(handles)):
			pp += float(linearrs[j][i])
		pp /= len(handles)
		outf.write(",%f" % pp)
	outf.write("\n")

	for i in range(len(handles)):
		lines[i] = handles[i].readline()

for f in handles:
	f.close()
outf.close()

