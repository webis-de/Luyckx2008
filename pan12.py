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

import jsonhandler
from LuyckxFeatures import *


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
    
    
panPath = "pan12/pan12-authorship-attribution-test-dataset-problem-%s-2015-10-20"
panSets = ['a', 'b', 'c', 'd', 'i', 'j']

for panSet in panSets:
    parsePAN(panPath, panSet)



