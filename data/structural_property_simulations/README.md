This directory contains all data/results files and analysis/visualization
scripts used in the structural property simulations in the AIRAS publication.

Note that this analysis requires DeltaGREM to calculate structural stability,
which is described in the following citations:

  Minning J, Porto M, Bastolla U. Detecting selection for negative design in proteins through an improved model of the misfolded state. Proteins. 2013 81:1102-12.

  Arenas M, Sánchez-Cobos A, Bastolla U. Maximum-Likelihood Phylogenetic Inference with Selection on Protein Folding Stability. Mol Biol Evol. 2015 32:2195-207.

  Bastolla U. Detecting selection on protein stability through statistical mechanical models of folding and evolution. Biomolecules. 2014 4:291-314.

This analysis also requires a machine-learning approach for predicting ligand
affinities. This software is available through the following citation:
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5054890/


Directory Structure and Index:

  README.md - this README file; contains the directory index

  brlens_and_labels.tre - tree file used for ancestral reconstruction of DSRM
  structural domains.

  AIRAS_results/ - contains getMLFasta.py script for extracting ML ancestral
  sequences from AIRAS results.

  structural_modeling/ - contains scripts used to generate structural models
  of ancestral reconstructed sequences and various data analysis/visualization
  scripts. The main analysis scripts are numbered 01_ - 15_, and must be run
  in order. Other scripts are mostly 'helpers' for these main analysis scripts,
  and should generally not be used on their own.
    struct_templates/ - contains structural templates used for homology modeling
    models/ - contains scripts for analyzing and visualizing homology models
    runmd.bash - generates structural homology models
    runDgrem.bash - runs DeltaGrem structural stability analysis
    
