#!/usr/bin/env python3

import sys
import os

proteins = ["CARD1", "DSRM1", "DSRM2", "DSRM3", "RD1"]
errors   = ["all", "res", "gap" ]

for protein in proteins:
    for error in errors:
        cmd = "./plotOrigCorrects.py %s %s > COR_REPORTS/%s.%s.csv" % (protein,error, protein,error)
        os.system(cmd)
