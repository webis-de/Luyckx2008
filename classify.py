import numpy as np
from subprocess import call
import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt  
from LuyckxFeatures import exportC5, importC5


def __init__(self):
    self.ready = True
def classify(trainData, testData, nNumFeatures):
    path         = os.path.dirname(trainData)
    trainFile    = os.path.basename(trainData)
    testFile     = os.path.basename(testData)
    outName      = os.path.splitext(testData)[0] + '.out'
    callCommand  = ['Timbl']
    callCommand.append('-mO:N1-%d' % nNumFeatures)
    callCommand.append('-o')
    callCommand.append(outName)
    callCommand.append('-P')
    callCommand.append(path)
    callCommand.append('-f')
    callCommand.append(trainFile)
    callCommand.append('-t')
    callCommand.append(testFile)
    call(callCommand)
    outClasses = [a[-1] for a in importC5(outName)]
    os.remove(outName)
    return outClasses
    
    def cross_validate(featureFile, nFolds):
        fListName   = os.path.splitext(featureFile)[0] + '.cv5list'
        original    = importC5(featureFile)
        docDict     = dict.fromkeys(set([a[-1] for a in original]))
        nDocs       = np.zeros(len(docDict.keys()))
        for idk, key in enumerate(docDict.keys()):
            vecs         = [vec for vec in original if vec[-1]==key]
            if len(vecs) % nFolds != 0:
                print('# of docs per author (%d) must be divisable by nFolds = %d' %
                   (nDocs[0], nFolds) )
                #return None
            else:
                ndf          = len(vecs) / nFolds
                docDict[key] = [vecs[ndf*i:ndf*(i+1)] for i in xrange(0,nFolds)]
                nDocs[idk]   = len(docDict[key])
        if nDocs[0] != np.mean(nDocs): 
            print('There is an unequal number of documents per author')
            #return None
        else:
            for N in xrange(0, nFolds):
                train   = dict()
                test    = dict()
                train['file'] = '%s.cvtrain' % (os.path.splitext(featureFile)[0])
                test['file']  = '%s.cvtest' % (os.path.splitext(featureFile)[0])
                train['vecs'] = sum([docDict[key][i] for i in range(0,5) if i!=N], [])
                test['vecs']  = sum([docDict[key][i] for i in range(0,5) if i==N], [])
                exportFoldFile(train)
                exportFoldFile(test)
                
                   
    def exportFold(fold):
        with open(fold['file'], "w") as fFile:
            for vec in fold['vecs']:
                [fFile.write(str(val)+',') for val in vec[:-1]]
                fFile.write(vec[-1] + '\n')
                
        
    
'''
nAuthors = [2,3]
features = ('fwd1', 'lex1', 'lex2', 'lex3', 
            'pos1', 'pos2', 'pos3')
fPath = "pan12/pan12-authorship-attribution-test-dataset-problem-a-2015-10-20";
            
accuracy = np.zeros( (len(nAuthors), len(features)) )

for idn,n in enumerate(nAuthors):
    for idk,key in enumerate(features):
        a = np.zeros(5)
        #data = loader.load_file
        for N in range(0,5):
            fName = '%s/features/N-%.3d_%s_cv%d.arff.cv.%%' % (fPath, n, key, N+1)
            call(['Timbl', '+%', '-t', 'cross_validate', '-f', fName[:-14:] + '_files', '-F', 'ARFF']);
            fHandle = open(fName, "r")
            a[N] = float(fHandle.readline())
            fHandle.close()
        
        accuracy[idn, idk] = 0.01 * np.mean(a);
        
fMarkers = ('+', 'd', '.', '^', 'o', '+', 'v', 'r')
for idk in range(0, len(features)):
    plt.plot(nAuthors, accuracy[:,idk], fMarkers[idk]+':');

plt.legend(features)
plt.savefig('%s/features/features.pdf' % fPath)
    
    
#jvm.stop()
'''
