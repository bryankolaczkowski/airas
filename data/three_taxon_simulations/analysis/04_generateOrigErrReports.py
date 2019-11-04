#!/usr/bin/env python3

import sys
import os
import glob

proteins = [ s.split("/")[-1] for s in glob.glob("../asr/B*_R*") ]
errors   = ["all", "res", "ins", "del"]

for protein in proteins:
    for error in errors:
        cmd = "./plotOrigErrors.py %s %s > err_reports_04/%s.%s.csv" % (protein,error, protein,error)
        os.system(cmd)
