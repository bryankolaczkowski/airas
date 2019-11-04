#!/usr/bin/env python

# Homology modeling with ligand transfer from the template
from modeller import *              # Load standard Modeller classes
from modeller.automodel import *    # Load the automodel class
import datetime

#####------------        CONTROL VARIABLES       ------------ #####
##             you should only have to change these.             ##
ALNFILE = 'alignment.ali' # alignment file from command-line
# names of templates (known structures)
KNOWNS  = ['5n8l','1DI2','1RC7','2l2k','2L3C','2L3J_DSRM1','2L3J_DSRM2','3VYX','5DV7_DSRM1','5DV7_DSRM2','5N8L_DSRM1']
SEQ     = 'seq'           # name of target (sequence of unknown structure)
NMODELS = 50              # number of models to build
##                                                               ##
#####------------      END CONTROL VARIABLES     ------------ #####

log.verbose()    # request verbose output
env = environ()  # create a new MODELLER environment to build this model in

# directories for input atom files
env.io.atom_files_directory = ['../../../../../struct_templates/']

# Read in HETATM and water records from template PDBs
#env.io.hetatm = True
#env.io.water  = True

a = automodel(env, alnfile=ALNFILE,knowns=KNOWNS, sequence=SEQ,
              assess_methods=(assess.DOPE, assess.DOPEHR))
a.starting_model = 1                # index of the first model
a.ending_model   = NMODELS          # index of the last model
a.make()                            # do the actual homology modeling

# write 'done' file #
outfile = open("seq.done", "w")
today = datetime.date.today()
outfile.write("%s\n" % today)
outfile.close()
