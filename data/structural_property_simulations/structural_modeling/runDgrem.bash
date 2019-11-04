#!/bin/bash

for f in `ls seq.BESTMODEL_*.pdb`; do

	../../../../../extractChain.py ${f} A > TEMPDG.pdb
	/ufrc/bryankol/bryank/src/DeltaGREM/DeltaGREM ../../../../../DGREM.in
	
	mv EMPDG_DeltaG.dat ${f}.dgremout
	rm TEMPDG.pdb *.dat E_loc_0.txt

done

