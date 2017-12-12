from LuyckxFeatures import *
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt  

authorDict = personae.getAuthorFileList(145)
authors    = list();
for idak, authorKey in enumerate(authorDict.keys()):
    authors.append(author(authorKey))
    print 'Loading documents of author %s...' % authorKey,
    authors[idak].setDocs(authorDict[authorKey])
    print 'done.'

nAuthors = [2, 5, 10, 20, 50, 100, 145];
fTest = dict();

for idna, na in enumerate(nAuthors):
    docs = getAllDocuments(authors[0:na]);    
    globalFeatures = dict.fromkeys((docs[0].features.keys()));
    for key in globalFeatures:
        globalFeatures[key] = globalFeature(key, docs);
        fName = 'features/N-%.3d_%s.arff' % (na, key)
        exportARFF(docs, authors[0:na], globalFeatures[key], 50, fName)
        fHandle = open('features/N-%.3d_%s_files' % (na, key), "w")
        for N in xrange(0,5):
            fName = 'features/N-%.3d_%s_cv%d.arff' % (na, key, N+1)
            fHandle.write(fName);            
            fHandle.write('\n');
            exportARFF(docs[N::5], authors, globalFeatures[key], 50, fName)
        fHandle.close();      
        if idna == 0:
            t0                  = dict(Counter(globalFeatures[key].chi2).most_common(5))
            fTest[key]          = dict();
            fTest[key]['feat']  = t0.keys()
            fTest[key]['data']  = np.zeros( (len(nAuthors),5) );
            fTest[key]['data'][0,:] = t0.values();
        else:
            fTest[key]['data'][idna,:] = [globalFeatures[key].chi2[fkey] for fkey in fTest[key]['feat']]


N = len(fTest) * 100 + 11
x = np.transpose(np.tile( np.array(nAuthors), (5,1) ));
for idk, key in enumerate(fTest.keys()):
    plt.subplot(N + idk)
    plt.plot(x, fTest[key]['data'], ':')
    plt.legend(fTest[key]['feat'], loc=5)

plt.savefig('chi2_evo.pdf')

