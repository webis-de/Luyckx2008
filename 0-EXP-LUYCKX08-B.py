from LuyckxFeatures import *
import personae
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import os
import timblClassification as timbl
from collections import Counter
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)


personae_path = 'personae/'
ex_path       = os.path.dirname(personae_path + 'experiment/')
if not os.path.exists(ex_path):
    os.makedirs(ex_path)

nAuthors = [2, 50, 145]
pData    = np.arange(0.1, 1.1, 0.1)
accuracy = np.zeros( (len(nAuthors), len(pData)) )
authors  = personae.getFeaturedAuthors(max(nAuthors), False)
fkey     = 'lex1'

for idn, na in enumerate(nAuthors):
    docs     = getAllDocuments(authors[0:na])
    gFeature = globalFeature(fkey, docs)
    fName = '%s/ex2%s.c5' % (ex_path, fkey)
    exportC5(docs, authors[0:na-1], gFeature, 50, fName)
    for idp, p in enumerate(pData):
        accuracy[idn,idp] = timbl.cross_validate(fName, 5, False, p)
    os.remove(fName)


# PLOTTING
plt.figure(figsize=(6, 6), dpi=300, facecolor='w', edgecolor='k')
for idn in range(0,len(nAuthors)):
    plt.plot(pData, accuracy[idn,:], '-', label= 'Timbl %d-authors' % nAuthors[idn])
plt.legend(bbox_to_anchor=(0,1.02,1,0.2),
           loc="lower left",
           mode="expand",
           borderaxespad=0,
           ncol = 2 )
plt.xlabel('percentage of training data provided')
plt.ylabel('accuracy')
plt.savefig('%s/figure_5.pdf' %  ex_path)

