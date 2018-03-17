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
rc('text', usetex=True)

personae_path = 'personae/';
ex_path       = os.path.dirname(personae_path + 'experiment/')
if not os.path.exists(ex_path):
    os.makedirs(ex_path)

authors  = personae.getFeaturedAuthors(145, False)
nAuthors = [2, 5, 10, 20, 50, 100, 145]
accuracy = np.zeros( (len(authors[0].docs[0].features.keys()), len(nAuthors)) )
chi2     = np.zeros( (len(nAuthors), 10) )
chi20    = dict()
chi2key  = 'lex1'
for n, na in enumerate(nAuthors):
    chi2max  = 0
    docs           = getAllDocuments(authors[0:na])
    globalFeatures = dict.fromkeys((docs[0].features.keys()))
    for idk, key in enumerate(globalFeatures.keys()):
        globalFeatures[key] = globalFeature(key, docs)
        fName = '%s/N-%.3d_%s.c5' % (ex_path, na, key)
        print 'Cross Validation for N = %.3d and feature %s' % (na, key)
        exportC5(docs, authors, globalFeatures[key], 50, fName)
        cMatrix = timbl.cross_validate(fName, 5, False)
        accuracy[idk][n] = timbl.accuracy(cMatrix)

        if n == 0 and key == chi2key:
            chi20   = [f[0] for f in Counter(globalFeatures[key].chi2).most_common(10)]
            chi2[n] = [f[1] for f in Counter(globalFeatures[key].chi2).most_common(10)] / max(globalFeatures[key].chi2.values())
        elif key == chi2key:
            chi2[n]  = [globalFeatures[chi2key].chi2[f] for f in chi20[key]] / max(globalFeatures[chi2key].chi2.values())
        os.remove(fName)


np.save('%s/accuracy_2.npy' % ex_path, accuracy)
np.save('%s/chi2_3.npy' % ex_path, chi2)

# PLOTTING    

accuracy = np.load('%s/accuracy_2.npy' % ex_path)
fNames  = ['lex1', 'lex2', 'lex3', 'pos1', 'pos2', 'pos3', 'fwd1']  
markers = ['kd-', 'kd--', 'kd:', 'ko-', 'ko--', 'ko:', 'ks-'];
plt.figure(num=None, figsize=(4, 4), dpi=300, facecolor='w', edgecolor='k')
for idk,key in enumerate(fNames):
    plt.plot(nAuthors, accuracy[idk], markers[idk], label=key)
plt.legend(loc="upper right")
plt.xlabel('number of authors')
plt.ylabel('accuracy')
plt.savefig('%s/figure_2.pdf' %  ex_path)


chi2 = np.load('%s/chi2_3.npy' % ex_path)
markers = ['o', '+', 'v', 's','d', '.', '^', '*', '>', '<'];
plt.figure(num=None, figsize=(6, 6), dpi=300, facecolor='w', edgecolor='k')
for idc, c in enumerate(chi20):
    plt.plot(nAuthors, chi2[:,idc], 'k:' + markers[idc], label = c)
plt.legend(bbox_to_anchor=(0,1.02,1,0.2), 
           loc="lower left", 
           mode="expand", 
           borderaxespad=0, 
           ncol = len(markers)/2 )
plt.xlabel('number of authors')
plt.ylabel('$\chi^2$ / max($\chi^2$)')
plt.savefig('%s/figure_3.pdf' %  ex_path)

