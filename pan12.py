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
dictPath = "pan12/pan12-authorship-attribution-test-dataset-problem-a-2015-10-20";

jsonhandler.loadJson(dictPath)
candidates = jsonhandler.candidates
unknowns   = jsonhandler.unknowns

jsonhandler.loadGroundTruth()
jsonhandler.loadTraining()



authors    = list();
idc = 0;
for cand in candidates:
	a = author(cand)
	text = '';
	for file in jsonhandler.trainings[cand]:
	    text = text + jsonhandler.getTrainingText(cand, file);
	for idu, file in enumerate(unknowns):
	    if jsonhandler.trueAuthors[idu] == cand:
	        text = text + jsonhandler.getUnknownText(file)
	sText = text.split()
	nWords = len(sText);
	nPart = int(round(nWords/10))
	aDocs = list()
	for idp in range(0,10):
	    pName = dictPath + '/' + cand + '_' + str(idp) + '.txt'
	    outHandle = open(pName, 'w')
	    outHandle.write(' '.join(sText[idp*nPart:(idp+1)*nPart]));
	    outHandle.close();
	    aDocs.append(pName);
	a.setDocs(aDocs);
	authors.append(a);
	print('Loading... %.f %% done' % 100*idc/len(cand) )
	
nAuthors = range(0, len(candidates))

for idna, na in enumerate(nAuthors):
    docs = getAllDocuments(authors[0:na]);    
    globalFeatures = dict.fromkeys((docs[0].features.keys()));
    for key in globalFeatures:
        globalFeatures[key] = globalFeature(key, docs);
        fName = '%s/N-%.3d_%s.arff' % (dictPath, na, key)
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
