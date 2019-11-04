#!/usr/bin/env python

import os
import sys

"""
Calculate mean and standard deviation of data x[]:
    mean = {\sum_i x_i \over n}
    std = sqrt(\sum_i (x_i - mean)^2 \over n-1)
"""
def meanstdev(x):
	from math import sqrt
	n, mean, std = len(x), 0, 0
	for a in x:
		mean = mean + a
	mean = mean / float(n)
	for a in x:
		std = std + (a - mean)**2
	std = sqrt(std / float(n-1))
	return (mean, std)

scorefname = sys.argv[1]

handle = open(scorefname, "r")
line = handle.readline()
# skip over all the model-build output #
while line:
	linearr = line.split()
	if len(linearr)>3 and linearr[0]=="Filename" and linearr[1]=="molpdf" and linearr[2]=="DOPE":
		break
	line = handle.readline()

# read model scores #
models = []
molpdf = []
dope   = []
dopehr = []
handle.readline()
line = handle.readline()
while line:
	if line[0] == ">":
		break
	linearr = line.split()
	if len(linearr) > 3:
		models.append(linearr[0])
		molpdf.append(float(linearr[1]))
		dope.append(float(linearr[2]))
		dopehr.append(float(linearr[3]))
	line = handle.readline()
handle.close()

# need to scale by 2 * stdev #
(molpdf_mean, molpdf_stdev) = meanstdev(molpdf)
(  dope_mean,   dope_stdev) = meanstdev(dope  )
(dopehr_mean, dopehr_stdev) = meanstdev(dopehr)

newmolpdf = [(x-molpdf_mean)/(2.0*molpdf_stdev) for x in molpdf]
newdope   = [(x-  dope_mean)/(2.0*dope_stdev)   for x in dope  ]
newdopehr = [(x-dopehr_mean)/(2.0*dopehr_stdev) for x in dopehr]

# now calculate best model #
# ave of scaled scores     #
bestmodel = ""
bestscore = 100000000.0

print "model [molpdf dope dopehr] score"
printlines = []
for i in range(len(models)):
	score = newmolpdf[i] + newdope[i] + newdopehr[i]
	printlines.append((score,"%s [%.3f(%.3f) %.3f(%.3f) %.3f(%.3f)] %.3f" % (models[i], molpdf[i], newmolpdf[i], dope[i], newdope[i], dopehr[i], newdopehr[i], score)))
	if score < bestscore:
		bestscore = score
		bestmodel = models[i]

printlines.sort(reverse=True)
for (s,v) in printlines:
	print v
print "BEST MODEL (out of %d): %s" % (len(models),bestmodel)

# get top 10 models #
printlines.sort()
NMODELS = 10
for i in range(NMODELS):
    (score,info) = printlines[i]
    model = info.split()[0]
    mname = info.split(".")[0]
    cmd = "cp %s ./%s.BESTMODEL_%d.pdb" % (model,mname,i)
    print cmd
    os.system(cmd)
