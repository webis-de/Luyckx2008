import jsonhandler
from LuyckxFeatures import *
import timblClassification as timbl
import os
import numpy as np
from collections import Counter


def parseC10(c10_path):
    jsonhandler.loadJson(c10_path)
    jsonhandler.loadTraining()
    candidates = jsonhandler.candidates
    unknowns   = jsonhandler.unknowns
    files      = list()
    for cand in candidates:
        for fileName in jsonhandler.trainings[cand]:
            files.append('%s/%s/%s' % (c10_path, cand, fileName) )
    for unknown in unknowns:
        files.append('%s/unknown/%s' % (c10_path, unknown) )
    
    parseCorpus(files)
    
    
dictPath = "c10"
jsonhandler.loadJson(dictPath)
jsonhandler.loadTraining()
candidates = jsonhandler.candidates
unknowns   = jsonhandler.unknowns
authors    = list()
uAuthors   = list()
for cand in candidates:
    a = author(cand)
    for fileName in jsonhandler.trainings[cand]:
        fName = '%s/%s/%s' % (dictPath, cand, fileName)
        pName = '%s/%s/%s' % (dictPath, cand, os.path.splitext(fileName)[0] + '.mbsp')
        a.addDoc(fName, pName)
    authors.append(a)
for unknown in unknowns:
    fName = '%s/unknown/%s' % (dictPath, unknown)
    pName = '%s/unknown/%s' % (dictPath, os.path.splitext(unknown)[0] + '.mbsp')
    a     = author(os.path.splitext(unknown)[0])
    a.addDoc(fName, pName)
    uAuthors.append(a)
        
docs = getAllDocuments(authors + uAuthors)
globalFeatures = dict.fromkeys((docs[0].features.keys()))
accuracy       = dict.fromkeys((docs[0].features.keys()))
predict        = dict.fromkeys((docs[0].features.keys()))
for idk, key in enumerate(globalFeatures.keys()):
    globalFeatures[key] = globalFeature(key, docs)
    train_fName         = '%s/%s_training.c5' % (dictPath, key)
    test_fName          = '%s/%s_test.c5' % (dictPath, key)
    exportC5(getAllDocuments(authors), authors, globalFeatures[key], 50, train_fName)
    exportC5(getAllDocuments(uAuthors), uAuthors, globalFeatures[key], 50, test_fName)
    noFeatures      = len(Counter(globalFeatures[key].chi2).most_common(50))
    predict[key]    = timbl.classify(train_fName, test_fName, noFeatures)
    os.remove(train_fName)
    os.remove(test_fName)
#    jsonhandler.storeJson(unknowns, predict)
    
jsonhandler.loadGroundTruth()
with open('%s/results' % dictPath, 'w') as rHandle:
    for key in globalFeatures.keys():
        cMatrix       = timbl.confusionMatrix(jsonhandler.trueAuthors, predict[key])
        accuracy[key] = np.sum(np.diag(cMatrix)) / np.sum(cMatrix)
        rHandle.write('%s \t %.4f \n' % (key, accuracy[key]))
