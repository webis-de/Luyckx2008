from collections import Counter
import numpy as np
import MBSP
import pickle
import arff
import re
import codecs
from os.path import splitext, isfile


def parseText(text, fileName):
    """
    Parses the text TEXT of a file FILENAME using the Memory Based Sharlow Parser (MBSP), extracting the following
    features:
        uni-, bi and trigrams of lexical features
        uni-, bi and trigrams of part-of-speech tags
        feature words

    The features are stored as a feature object in a PICKLE file filename.mbsp for later analysis, due to the amount
    of time parsing takes.

    Arguments
    ---------
    text : text
       text of the file FILENAME
    fileName :
        path and name of the file
    """

    try:
        p = MBSP.parse(text)
    except AssertionError: 
        p = MBSP.parse('')
        print('WARNING. FILE COULD NOT BE PARSED.')
    s = MBSP.split(p)
    fwd = [u'']
    pos = [u'']
    for sentence in s:
        fwd += [w.string for w in sentence.word]
        pos += sentence.parts_of_speech
    
    features = dict()
    
    for n in range(1,4):
        features['lex%d'%n] = feature('lex%d'%n, ngram(text,n))
        features['pos%d'%n] = feature('pos%d'%n, ngram(pos,n))
    
    features['fwd1']    = feature('fwd1', fwd)
    
    # TODO: TOC, CGP ???
    
    with open(fileName, 'w') as f:
        pickle.dump(features, f)
        
def parseCorpus(fileList, reparse = False):
    """
    Parses the corpus, in the list FILELIST to MBSP-files. If REPARSE is false (standard), existing mbsp files are
    not reparsed again.

    Arguments
    ---------
    fileList : list
       fileList containing the respective textFiles of the corpus
    reparse : bool
        Ignoring existing MBSP files
    """
    N = len(fileList)
    for idf, fName in enumerate(fileList):
        lidf = len(str(N))
        s    = 'Loading file %%s (%%%d.d of %%d)...' % lidf
        print s % (fName, idf+1, N),
        pName = splitext(fName)[0] + '.mbsp'
        if not isfile(pName) or reparse:
            with codecs.open(fName, 'r', encoding = 'utf-8') as f:
                text = f.read()
                parseText(text, pName)
        else:
            print('File %s already exists. Skipping...' % pName)
        print ' %.4f %% done.' % (100.*(idf+1)/N)


def ngram(flist, n):    
    """
    Returns the n-gram of a list of features

    Arguments
    ---------
    flist : list
       List containing the features to be n-gramed
    n : int
        specifies n for an n-gram

    Returns
    -------
    list
        List of n-grams
    """
    return [''.join(flist[idn:idn+n]) for idn in xrange(len(flist)-n+1)]
        
        
def convert2Frequency(featureDict):
    """
    Converts the count values of the feature dictionary to frequencies.

    Arguments
    ---------
    featureDict : dict
        dictionary of document with the respective values


    Returns
    -------
    featureDict : dict
        containing the corresponding frequencies converted to absolute numbers
    """
    if sum(featureDict.values()) != 0:
        invTotalNumber = 1.0 / sum(featureDict.values())
    else:
        invTotalNumber = 1.0
    featureDict.update((k, invTotalNumber*v) for k,v in featureDict.items())
    return featureDict
        
def getAllDocuments(authorlist):
    """
    Returns the documents of all authors in AUTHORLIST for feature extraction.

    Arguments
    ---------
    authorList : list
        list with all authors


    Returns
    -------
    documentList : list
        list containing all documents of authors in authorlist
    """
    documentlist = []
    for authors in authorlist:
        [documentlist.append(doc) for doc in authors.docs]
    return documentlist

def iterMean(meanValue, newValue, N):
    """ Iterative mean value calculation """
    return 1.0 * (N-1) / N * meanValue + 1. / N * newValue
    

class document(object):
    """
    Document class for handling documents, i.e. files with FILENAME, its parsed version, and the respective author
    """
    def __init__(self, author, filename, parsedFileName):
        self.features       = dict()
        self.author         = author
        self.fileName       = filename
        self.parsedFileName = parsedFileName
    
    def loadFeatures(self):
        with open(self.parsedFileName, 'r') as f:
            self.features = pickle.load(f)
    
    def addFeature(self, feature):
        self.features[feature.name] = feature 
  
class author(object):
    """
    Document class for handling documents, i.e. name and DOCUMENT class files
    """
    def __init__(self, name):
        self.name       = name
        self.docFiles   = list()
        self.docs       = list()

    def addDoc(self, fileName, parsedFileName):
        self.docFiles.append(fileName)
        temp_doc = document(self.name, fileName, parsedFileName)
        temp_doc.loadFeatures()
        self.docs.append(temp_doc)
            
       
class feature(object):
    """
    Feature class for handling documents' features, i.e. name and DOCUMENT class files
    """
    def __init__(self, name, rawFeature):
        self.name        = name
        self.featureDict = convert2Frequency(dict(Counter(rawFeature)))
        
    def getFeatureVector(self, globalFeature, n):
        topFeatures     = dict(Counter(globalFeature.chi2).most_common(n))
        return [self.featureDict[key] if self.featureDict.has_key(key) else 0 for key in topFeatures.keys()]


     
class globalFeature(object):
    """
    Class defining a 'global feature', summarizing all existing (and parsed) documents features all together. Used to
    calculate frequencies and chi squared values. Expects a list with all documents when created.
    """
    def __init__(self, name, docList):
        self.name = name
        self.featureDict = dict()
        for idd, doc in enumerate(docList):
            if not doc.features.has_key(self.name):
                raise Exception('No feature named ' + self.name + ' in ' + doc.name)
            dfDict = doc.features[name].featureDict
            for key in set(self.featureDict.keys() + dfDict.keys()):
                if self.featureDict.has_key(key) and dfDict.has_key(key):
                    self.featureDict[key] = iterMean(self.featureDict[key], dfDict[key], idd + 1)
                elif self.featureDict.has_key(key) and not dfDict.has_key(key):
                    self.featureDict[key] = iterMean(self.featureDict[key], 0., idd + 1)
                else:
                    self.featureDict[key] = 1. / (idd + 1) * dfDict[key]
        self.chiSquared(docList)

    def chiSquared(self, docList):            
        self.chi2 = dict.fromkeys(self.featureDict.keys(), 0)
        for key in self.featureDict.keys():
            val_i = np.zeros(len(docList))
            for idd, doc in enumerate(docList):
                if doc.features[self.name].featureDict.has_key(key):
                    val_i[idd] = doc.features[self.name].featureDict[key]
                 
            chi_i = (val_i - self.featureDict[key] ) ** 2
            self.chi2[key] = sum(1.0 * chi_i / self.featureDict[key])
            
    def getAttributeNames(self, n):
        topFeatures     = dict(Counter(self.chi2).most_common(n))
        return topFeatures.keys()


def exportARFF(docList, authorList, gFeature, n, fileName):
    """
    Exports the doclist's document features to an ARFF file, ready to read by e.g. the WEKA package. Requires a global
    feature of the document list.

    Arguments
    ---------
    docList : list
        list containing all documents as document objects
    authorList : list containing the respective authors
        list containing the respective author objects
    gFeature : globalFeature
        globalFeature handle to extract the relevant frequencies and chi-squared values
    n : integer
        number of features with highest chi-squared value to be exported
    fileName : string
        file name of the document
    """
    data = dict()
    data['attributes'] = list()
    for ida, attribute in enumerate(gFeature.getAttributeNames(n)):
        aName = re.sub("[^A-Za-z0-9]+", 'x', attribute.decode(errors='replace'))
        aName = gFeature.name + '_' + str(ida) + '_' + aName
        data['attributes'].append( (aName, 'REAL') )
    
    data['attributes'].append(('author', list([author.name for author in authorList])))
    data['data'] = list()

    for idd, doc in enumerate(docList):
        data['data'].append(doc.features[gFeature.name].getFeatureVector(gFeature, n))
        data['data'][idd].append(doc.author)

    data['description'] = ''
    data['relation'] = gFeature.name

    fHandle = open(fileName, "w")
    arff.dump(data, fHandle)
    fHandle.close()
    return(data)
    
def exportC5(docList, gFeature, n, fileName):
    """
    Exports the doclist's document features to a C5 file, ready to read by e.g. TIMBL. Requires a global
    feature of the document list.

    Arguments
    ---------
    docList : list
        list containing all documents as document objects
    gFeature : globalFeature
        globalFeature handle to extract the relevant frequencies and chi-squared values
    n : integer
        number of features with highest chi-squared value to be exported
    fileName : string
        file name of the document
    """
    with open(fileName, "w") as fHandle:
        for doc in docList:
            [fHandle.write(str(val)+',') for val in doc.features[gFeature.name].getFeatureVector(gFeature, n)]
            fHandle.write(doc.author + '\n')

def importC5(fileName):
    """
    Imports a C5 file

    Arguments
    ---------
    filename : string
        name and path of the file to be imported

    Returns
    ---------
    fVectors : list
        list of numerical feature vectors
    authors : list
        list containing the authors as strings

    """
    fVectors = list()
    authors  = list()
    with open(fileName, "r") as fHandle:
        c5_input = list()
        for line in fHandle:
            inVec = line.strip('\n').split(',')
            fVectors.append(inVec[:-1])
            authors.append(inVec[-1])
    return fVectors, authors
    

