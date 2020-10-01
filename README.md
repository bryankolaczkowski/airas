# airas
alignment-integrated reconstruction of ancestral sequences

This repository contains scripts (mostly python and bash) and data/results
files associated with the Kolaczkowski Lab's AIRAS project, which calculates
ancestral protein sequences while integrating over different alignments.

Further information on the methodology can be found in the project's main
peer-reviewed publication:

https://doi.org/10.1093/gbe/evaa164

All data and results files used in the above publication, as well as all
scripts and spreadsheets used for data analysis and visualization can be
found in the data/ directory. Please see the data/README.md file for more
information on data/results files and analysis/visualization scripts available
in data/

The main airas.py executable is a Python script that performs
alignment-integrated ancestral sequence reconstruction. It has been tested on
MAX OS X and should work on any version of UNIX. It requires the following:

  1. RAxML to perform the ancestral sequence reconstruction. We recommend
     using RAxML v8
      https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3998144/
      https://github.com/stamatak/standard-RAxML
    You will need to edit line 35 of airas.py to set the RAXML variable to
    the RAxML v8 executable on your system.

  2. MAFFT to perform the mapping among all input alignments. We recommend
     using MAFFT v7
      https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3603318/
      https://mafft.cbrc.jp/alignment/software/
    You will need to edit line 36 of airas.py to set the MAFFT variable to
    the MAFFT v7 executable on your system.

  To perform an ancestral sequence reconstruction using airas.py, you first
  need to generate a binary phylogenetic tree for the sequences you want to
  analyze. You will also need alignments of your sequences, which you can
  produce using any sequence-based alignment method (see data/ for the
  alignment methods used in the AIRAS publication). Once you have a binary
  tree and multiple different alignments of the same extant sequences, airas.py
  will integrate ancestral sequence reconstructions at every node on the
  phylogeny, incorporating information from all sequence alignments.

  run ./airas.py -h for usage information.

All information in this repository is provided under the included LICENSE
