This directory contains all data/results files and analysis/visualization
scripts used in the large-tree simulations presented in the AIRAS publication.

The simulation of structure-based data required indel-seq-gen (we used
v2.1.03). https://www.ncbi.nlm.nih.gov/pubmed/17158778

Directory Structure and Index:

  README.md - this README file; contains the directory index

  The main simulation scripts are numbered 00_ - 08_, and they will need to be
  run in order. These will generate the simulated sequence data and run the
  AIRAS analyses. The un-numbered scripts are helper scripts used the the main
  simulation scripts; typically you would not run these directly.

  analysis_scripts/ - contains all data analysis and visualization scripts for
  the large-tree simulation studies presented in the AIRAS publication. As with
  other directories in this project, the numbered scripts (00_ - 10_) perform
  the main analysis; they must be run in order, and the other scripts are
  generally 'helper' scripts that should not be run on their own. The
  COR_REPORTS/ and ERR_REPORTS/ subdirectories contain scripts for analyzing
  and visualizing information about the correct ASR states and ASR errors,
  respectively. 
