import jsonhandler as json
import LuyckxFeatures as lf
import timblClassification as timbl
import os
from collections import Counter
import sys

""" LUYCKX2008.py
This python script is the "to-go" version of a reimplementation of an authorship verification and attribution approach 
by Luyckx et al. [2008]. The feature extraction methods may be found in "LuyckxFeatures.py", and the classification 
wrapper in "timblClassification.py".
"""

def prepareInputCorpus(corpus, reparseCorpus):
    """
    Parses the entire corpus to MBSP files. This step takes most of the time and should be done as a background
    task. The actual classification step is faster. Creates an MBSP file of the original text.
    Example: unknown.txt -> unknown.mbsp

    Arguments
    ---------
    corpus : list
        List containing all files which need to be parsed
    reparseCorpus : bool
        If true, existing mbsp files are ignored and reparsed.

    Returns
    -------
    authors : list
        List containing author objects of the known authors.
    uAuthors : list
        List containing author objects of the unknown authors.
    """
    json.loadJson(corpus)
    json.loadTraining()
    candidates = json.candidates
    unknowns   = json.unknowns

    files    = list()
    authors  = list()
    uAuthors = list()
    for cand in candidates:
        for fileName in json.trainings[cand]:
            files.append('%s/%s/%s' % (corpus, cand, fileName))
    for unknown in unknowns:
        files.append('%s/unknown/%s' % (corpus, unknown))

    print('Parsing corpus... this may take a while.')

    lf.parseCorpus(files, reparseCorpus)

    print('Loading Candidates...')
    for cand in candidates:
        a = lf.author(cand)
        for fileName in json.trainings[cand]:
            fName = '%s/%s/%s' % (corpus, cand, fileName)
            pName = '%s/%s/%s' % (corpus, cand, os.path.splitext(fileName)[0] + '.mbsp')
            a.addDoc(fName, pName)
        authors.append(a)
    print('Loading Unknowns...')
    for unknown in unknowns:
        fName = '%s/unknown/%s' % (corpus, unknown)
        pName = '%s/unknown/%s' % (corpus, os.path.splitext(unknown)[0] + '.mbsp')
        a = lf.author(os.path.splitext(unknown)[0])
        a.addDoc(fName, pName)
        uAuthors.append(a)

    return authors, uAuthors


# PARAMETERS
reparseCorpus = False   # if true, the corpus is completely reparsed, even if mbsp-files exist.
eFeature = 'lex1'       # can be changed to lex1, lex2, lex3, pos1, pos2, pos3, fwd
corpus  = sys.argv[1]
outFile = sys.argv[2]


print('Loading Documents...')
authors, uAuthors = prepareInputCorpus(corpus,reparseCorpus)
docs = lf.getAllDocuments(authors + uAuthors)
globalFeatures = dict.fromkeys((docs[0].features.keys()))
accuracy = dict.fromkeys((docs[0].features.keys()))
predict = dict.fromkeys((docs[0].features.keys()))

key = eFeature
print('Loading Feature %s...' % key)
train_fName = '%s/%s_training.c5' % (corpus, key)
globalFeatures[key] = lf.globalFeature(key, docs)
test_fName = '%s/%s_test.c5' % (corpus, key)
lf.exportC5(lf.getAllDocuments(authors), authors, globalFeatures[key], 50, train_fName)
lf.exportC5(lf.getAllDocuments(uAuthors), uAuthors, globalFeatures[key], 50, test_fName)
noFeatures = len(Counter(globalFeatures[key].chi2).most_common(50))

print('Running Classification...')
predict = timbl.classify(train_fName, test_fName, noFeatures)
os.remove(train_fName)
os.remove(test_fName)
json.storeJson(outFile, json.unknowns, predict)