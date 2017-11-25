from LuyckxFeatures import *

''' small test  
aNames   = ['a', 'b', 'c']
fileList = [['t1'], ['t2'], ['t3']]
authors  = list()
for ida, aName in enumerate(aNames):
    authors.append(author(aName))
    authors[ida].setDocs(fileList[ida])

docs = getAllDocuments(authors);
globalFeatures = dict.fromkeys((docs[0].features.keys()));

for key in globalFeatures:
    globalFeatures[key] = globalFeature(key, docs);
    exportARFF(docs, authors, globalFeatures[key], 5, 'features/'+key+'.arff')
''' 
    

authorDict = personae.getAuthorFileList(145)
authors    = list();
for idak, authorKey in enumerate(authorDict.keys()):
    authors.append(author(authorKey))
    print 'Loading documents of author %s...' % authorKey,
    authors[idak].setDocs(authorDict[authorKey])
    print 'done.'

docs = getAllDocuments(authors);
globalFeatures = dict.fromkeys((docs[0].features.keys()));

for key in globalFeatures:
    globalFeatures[key] = globalFeature(key, docs);
    exportARFF(docs, authors, globalFeatures[key], 50, 'features/'+key+'.arff')

f = 'pos1'
x = globalFeatures[f]
y = docs[0].features[f]

