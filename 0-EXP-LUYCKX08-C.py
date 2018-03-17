import LuyckxFeatures as lf
import personae
import numpy as np
import os
import timblClassification as timbl
from collections import Counter

personae_path = 'personae/'
ex_path       = os.path.dirname(personae_path + 'experiment/')
if not os.path.exists(ex_path):
    os.makedirs(ex_path)

authors = personae.getFeaturedAuthors(60, False)
aid = 5
for ida, author in enumerate(authors):
    if ida == aid:
        author.name  = 'suspect'
        for d in author.docs:
            d.author = author.name
        a0           = authors[0]
        authors[0]   = author
        authors[ida] = a0
    else:
        author.name = 'other'
        for d in author.docs:
            d.author = author.name

docs = lf.getAllDocuments(authors)
features  = ['fwd1', 'lex1', 'lex2', 'lex3', 'pos1', 'pos2', 'pos3']
globalFeatures = dict()
precision = dict()
recall    = dict()
fscore    = dict()
accuracy  = dict()
rName     = '%s/table_1' % ex_path
rHandle = open(rName, 'w')
rHandle.write('feature set \t precision \t recall \t F-score \t Accuracy \n')
for key in features:
    globalFeatures[key] = lf.globalFeature(key, docs)
    fName = '%s/%s_validation.c5' % (ex_path, key)
    print 'Cross Validation for feature %s' % key
    lf.exportC5(docs, authors, globalFeatures[key], 50, fName)
    cMatrix = timbl.cross_validate(fName, 5, False, 1.0, 'suspect')
    precision[key] = timbl.precision(cMatrix) * 100.
    recall[key]    = timbl.recall(cMatrix) * 100.
    fscore[key]    = timbl.fScore(cMatrix) * 100.
    accuracy[key]  = timbl.accuracy(cMatrix) * 100.
    rHandle.write('%s \t\t %.2f \t\t %.2f \t\t %.2f \t\t %.2f \n' %
                  (key, precision[key], recall[key], fscore[key], accuracy[key]))
rHandle.close()