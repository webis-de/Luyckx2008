import jsonhandler
from LuyckxFeatures import *
import timblClassification as timbl
import os
import numpy as np
from collections import Counter

def parsePAN(panPath, panSet):
    dictPath = panPath % panSet
    jsonhandler.loadJson(dictPath)
    jsonhandler.loadTraining()
    candidates = jsonhandler.candidates
    unknowns   = jsonhandler.unknowns
    files      = list()
    for cand in candidates:
        for fileName in jsonhandler.trainings[cand]:
            files.append('%s/%s/%s' % (dictPath, cand, fileName) )
    for unknown in unknowns:
        files.append('%s/unknown/%s' % (dictPath, unknown) )
    
    parseCorpus(files)
    
    
panPath = "pan11-authorship-attribution-test-dataset-%s-2015-10-20"
panSets = ['small']

for panSet in panSets:
    dictPath = panPath % panSet
    jsonhandler.loadJson(dictPath)
    jsonhandler.loadTraining()
    candidates = jsonhandler.candidates
    unknowns = jsonhandler.unknowns
    authors = list()
    uAuthors = list()
    print('Loading Candidates...')
    for cand in candidates:
        a = author(cand)
        for fileName in jsonhandler.trainings[cand]:
            fName = '%s/%s/%s' % (dictPath, cand, fileName)
            pName = '%s/%s/%s' % (dictPath, cand, os.path.splitext(fileName)[0] + '.mbsp')
            a.addDoc(fName, pName)
        authors.append(a)
    print('Loading Unknowns...')
    for unknown in unknowns:
        fName = '%s/unknown/%s' % (dictPath, unknown)
        pName = '%s/unknown/%s' % (dictPath, os.path.splitext(unknown)[0] + '.mbsp')
        a = author(os.path.splitext(unknown)[0])
        a.addDoc(fName, pName)
        uAuthors.append(a)

    print('Loading Documents...')
    docs = getAllDocuments(authors + uAuthors)
    globalFeatures = dict.fromkeys((docs[0].features.keys()))
    accuracy = dict.fromkeys((docs[0].features.keys()))
    predict = dict.fromkeys((docs[0].features.keys()))
    for idk, key in enumerate(globalFeatures.keys()):
        print('Loading Feature %s...' % key)
        globalFeatures[key] = globalFeature(key, docs)
        train_fName = '%s/%s_training.c5' % (dictPath, key)
        test_fName = '%s/%s_test.c5' % (dictPath, key)
        exportC5(getAllDocuments(authors), authors, globalFeatures[key], 50, train_fName)
        exportC5(getAllDocuments(uAuthors), uAuthors, globalFeatures[key], 50, test_fName)
        noFeatures = len(Counter(globalFeatures[key].chi2).most_common(50))
        print('Running Classification...')
        predict[key] = timbl.classify(train_fName, test_fName, noFeatures)
    #    os.remove(train_fName)
    #    os.remove(test_fName)
    #    jsonhandler.storeJson(unknowns, predict)

    jsonhandler.loadGroundTruth()
    with open('pan11/results_%s' % panSet, 'w') as rHandle:
        for key in globalFeatures.keys():
            cMatrix = timbl.confusionMatrix(jsonhandler.trueAuthors, predict[key])
            accuracy[key] = np.sum(np.diag(cMatrix)) / np.sum(cMatrix)
            rHandle.write('%s \t %.4f \n' % (key, accuracy[key]))

# scp -r LuyckxFeatures.py classify.py personae.py pan12.py pan12 kolleg@gammaweb01.medien.uni-weimar.de:~/ytaege/Luyckx2008

