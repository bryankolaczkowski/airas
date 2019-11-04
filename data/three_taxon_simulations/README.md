This directory contains all data/results files and analysis/visualization
scripts used in the 3-taxon simulations in the AIRAS publication.

Directory Structure and Index:

  README.md - this README file; contains the directory index

  simulations/ - contains scripts for executing the 3-taxon simulations
  using indel-seq-gen (we used v2.1.03). isg.bash runs the simulations,
  using the input.tre file

  asr/ - contains scripts for executing 3-taxon ancestral sequence
  reconstruction using AIRAS. airas.bash executes the ancestral reconstruction,
  using simulated date from the simulations/ directory.

  analysis/ - contains scripts for 3-taxon data analysis and visualization.
  The python scripts for data analysis are numbered 01_ - 10_, and must be
  run in order. The "plot..." python scripts were used to generate figures
  for the publication; they also generate statistics data that was used in
  the publication.
