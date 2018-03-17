# META_FNAME - name of the meta-file.json
# GT_FNAME - name of the ground-truth.json
# OUT_FNAME - file to write the output in (answers.json)
# encoding - encoding of the texts (from json)
# language - language of the texts (from json)
# upath - path of the 'unknown' dir in the corpus (from json)
# candidates - list of candidate author names (from json)
# unknowns - list of unknown filenames (from json)
# trainings - dictionary with lists of filenames of trainingtexts for each author
# 	{"candidate2":["file1.txt", "file2.txt", ...], "candidate2":["file1.txt", ...] ...}
# trueAuthors - list of true authors of the texts (from GT_FNAME json)
# correstponding to 'unknowns'
# scp -r LuyckxFeatures.py classify.py personae.py pan12.py pan12 kolleg@gammaweb01.medien.uni-weimar.de:~/ytaege/Luyckx2008

import jsonhandler
from LuyckxFeatures import *
import timblClassification as timbl
import os
import numpy as np

def parsePAN(panPath, panSet):
    dictPath = panPath % panSet;
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
    
    
panPath = "pan12-authorship-attribution-test-dataset-problem-%s-2015-10-20"
panSets = ['i']
accuracy = np.zeros( (len(panSets), 7) )
predict  = dict()
for ids, panSet in enumerate(panSets):  
    dictPath = panPath % panSet;
    #parsePAN(panPath, panSet)
    dictPath = panPath % panSet;
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
    globalFeatures = dict.fromkeys((docs[0].features.keys()));
    jsonhandler.loadGroundTruth()
    for idk, key in enumerate(globalFeatures.keys()):
        globalFeatures[key] = globalFeature(key, docs);
        train_fName         = '%s/%s_training.c5' % (dictPath, key)
        test_fName          = '%s/%s_test.c5' % (dictPath, key)
        exportC5(getAllDocuments(authors), authors, globalFeatures[key], 50, train_fName)
        exportC5(getAllDocuments(uAuthors), uAuthors, globalFeatures[key], 50, test_fName)
        noFeatures = len(Counter(globalFeatures[key].chi2).most_common(50));
        predict[key] = timbl.classify(train_fName, test_fName, noFeatures)
        os.remove(train_fName)
        os.remove(test_fName)

    jsonhandler.loadGroundTruth()
    with open('%s/results' % dictPath, 'w') as rHandle:
        for idk, key in enumerate(globalFeatures.keys()):
            cMatrix = timbl.confusionMatrix(jsonhandler.trueAuthors, predict[key])
            accuracy[ids,idk] = np.sum(np.diag(cMatrix)) / np.sum(cMatrix)
            rHandle.write('%s \t %.4f \n' % (key, accuracy[ids, idk]))

with open('pan12/results', 'w') as rHandle:
    for idk, key in enumerate(globalFeatures.keys()):
        a = np.mean(accuracy[:,idk])
        rHandle.write('%s \t %.4f \n' % (key, a))

        
        
        
        
        
        
        
