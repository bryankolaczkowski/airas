This directory contains all data/results files and analysis/visualization
scripts used in the main AIRAS peer-reviewed publication. You should be able
to completely replicate the published work using only the files contained
in this directory and the main airas.py application file.

Directory Structure and Index:

  README.md - this README file; contains the directory index

  alignment_scripts/ - contains bash scripts used to perform sequence alignments
    requires: clustalw, mafft, msaprobs, probalign, probcons, tcoffee and/or
              any sequence-alignment program you would like to use.

  real_sequences/ - contains biological sequence data and protein-family trees
  used to generate the large_tree_simulations data. Trees (brlens_and_labels.tre)
  and structurally-aligned sequences (structaligned.fasta) are available for
  CARD1, DSRM1, DSRM2, DSRM3 and RD1 protein domains.

  large_tree_simulations/ - contains data and analysis/visualization scripts
  for generating and analyzing the large-tree simulations presented in the
  AIRAS publication.

  structural_property_simulations/ - contains data and analysis/visualization
  scripts for generating and analyzing the DSRM1 structural property simulations
  presented in the AIRAS publication.

  three_taxon_simulations/ - contains data and analysis/visualization scripts
  for generating and analyzing the 3-taxon simulations presented in the AIRAS
  publication.
