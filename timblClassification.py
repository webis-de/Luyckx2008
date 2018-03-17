import numpy as np
from subprocess import call
import os
from LuyckxFeatures import exportC5, importC5
from collections import Counter
"""
Wraps the Tillburg Memory Based Learner (TIMBL) into python, including some help functions, e.g. to calculate confusion
matrices, the F-score and accuracy.
"""
def classify(trainData, testData, nNumFeatures, verbosity = False):
    """
    Classifies a C5-file TESTDATA by means of a trained model, using the file TRAINDATA, returning the predicitions.

    Arguments
    ---------
    trainData : string
        C5-file containing the training data
    testData : string
        C5-file containing the test data
    testData : integer
        number of features per document in the C5 file
    verbosity : bool (optional)
        If false, the command line output is partially suppressed

    Returns
    -------
    predict : list
        list of the predicted authors
    """
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
    if verbosity:
        call(callCommand)
    else:
        with open(os.devnull, 'w') as devnull:
            call(callCommand, stdout=devnull, stderr=devnull)
    predictV, predict = importC5(outName)
    os.remove(outName)
    return predict
    
def cross_validate(featureFile, nFolds, verbosity = False, percentTData = 1., extype='attribution'):
    """
    Performs a n-fold cross validation on the data in featureFile.

    Arguments
    ---------
    featureFile : string
        C5-file containing the test data
    nFolds : integer
        number of folds tested
     verbosity : bool (optional)
        If false, the command line output is partially suppressed
    percentTData : float between 0 and 1 (optional, standard = 100%)
        percentage of the data used for training
    extype : string (optional, standard = attribution)
        Option to choose whether an attribution or verification task should be performed

    Returns
    -------
    cMatrix : numerical matrix
        confusion matrix of the performed experiment
    """
    oData,aData = importC5(featureFile)
    nAuthors    = len(set(aData))
    if extype == 'attribution' and np.mean(Counter(aData).values()) != Counter(aData).values()[0]:
        print('Number of docs per author should be equal in attribution experiment')
    docsPerFold = len(oData) / nFolds
    cMatrix     = np.zeros( (nAuthors, nAuthors) )

    for N in range(0,nFolds):
        testAuthors = list()
        trainAuthors= list()
        testData    = list()
        trainData   = list()
        for idv in range(0,len(oData)):
            if (N+idv) % nFolds == 0:
                testData.append(oData[idv])
                testAuthors.append(aData[idv])
            else:
                trainData.append(oData[idv])
                trainAuthors.append(aData[idv])  
        teFile = '%s.cvtest' % (os.path.splitext(featureFile)[0])
        trFile = '%s.cvtrain' % (os.path.splitext(featureFile)[0])
        tAmount = int(round(len(trainAuthors) * percentTData))  # limit training data
        exportFoldFile(testData, testAuthors, teFile)
        exportFoldFile(trainData[0:tAmount], trainAuthors[0:tAmount], trFile)
        predict = classify(trFile, teFile, len(oData[0]))
        if extype != 'attribution':
            cMatrix += confusionMatrix(testAuthors, predict, extype)
        os.remove(teFile)
        os.remove(trFile)
    if percentTData != 1.0: print('Ran CV only with %.f %% (%d docs) of training data.' % (percentTData * 100, tAmount))
    return cMatrix
           
def exportFoldFile(vectors, authors, fileName):
    """
    Help function for the n-fold classification function.
    """
    with open(fileName, "w") as fFile:
        for idv, vec in enumerate(vectors):
            [fFile.write(str(val)+',') for val in vec]
            fFile.write(authors[idv] + '\n')
        
def confusionMatrix(actual, predict, truePositiveClass=''):
    """
    If the original authors are available (e.g. for a cross validation task), the confusion matrix can be calculated.

    Arguments
    ---------
    actual : list of strings
        list containing the actual authors
    predict : list of strings
        list containing the predicted authors
    truePositiveClass : list, optional
        provide further authors which are not in the actual list

    Returns
    -------
    cmatrix : matrix
        confusion matrix
    """
    classes  = list(set(actual + predict))
    if len(truePositiveClass) > 0:
        id0 = classes.index(truePositiveClass)
        classes[id0] = classes[0]
        classes[0]   = truePositiveClass
    cMatrix  = np.zeros( (len(classes), len(classes)) )

    for i in range(0,len(predict)):
        ida = classes.index(actual[i])
        idp = classes.index(predict[i])
        cMatrix[ida][idp] += 1
    return cMatrix

def accuracy(cMatrix):
    """
    Calculates the accuracy using the confusion matrix.
    """
    return np.sum(np.diag(cMatrix)) / np.sum(cMatrix)

def precision(cMatrix):
    """
    Calculates the precision using the confusion matrix.
    """
    return cMatrix[0,0] / np.sum(cMatrix[0,:])

def recall(cMatrix):
    """
    Calculates the recall using the confusion matrix.
    """
    return cMatrix[0,0] / np.sum(cMatrix[:,0])

def fScore(cMatrix):
    """
    Calculates the F-score using the confusion matrix.
    """
    if precision(cMatrix) + recall(cMatrix) == 0:
        return precision(cMatrix)
    else:
        return 2 * precision(cMatrix) * recall(cMatrix) / (precision(cMatrix) + recall(cMatrix))


















