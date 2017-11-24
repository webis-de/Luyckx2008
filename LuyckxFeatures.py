from collections import Counter
import numpy as np
import MBSP
import math
import arff
import re
import personae 

def parseText(text):
    p = MBSP.parse(text);
    s = MBSP.split(p);
    lex = [u''];
    pos = [u''];
    for sentence in s:
        lex += [w.string for w in sentence.word];
        pos += sentence.parts_of_speech;  
    
    rawFeatures = dict();
    
    for n in xrange(1,4):
        rawFeatures['lex%d'%n] = ngram(lex,n);
        rawFeatures['pos%d'%n] = ngram(pos,n);
        
    return rawFeatures    
    
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
        return [''.join(flist[idn:idn+n]) for idn in xrange(len(flist)-n+1)];
        
        
def convert2Frequency(featureDict):
    invTotalNumber = 1.0 / sum(featureDict.values());
    featureDict.update((k, invTotalNumber*v) for k,v in featureDict.items());
    return featureDict
        
def getAllDocuments(authorlist):
    documentlist = [];
    for authors in authorlist:
        [documentlist.append(doc) for doc in authors.docs];
    return documentlist;   

def iterMean(meanValue, newValue, N):
    return 1.0 * (N-1) / N * meanValue + 1. / N * newValue;
    

class document(object):
    def __init__(self, author, filename):
        self.features       = dict();
        self.author         = author;
        self.fileName       = filename;
        self.readText();
        
    def textReader(self, filename):
        """ Simple Text Reader """
        f   = open(filename, "r")
        txt = f.read();
        return txt;
        
    def readText(self):
        inText           = self.textReader(self.fileName);
        rawFeatures      = parseText(inText);
        for fName in rawFeatures.keys():
            self.features[fName] = feature(fName, rawFeatures[fName])
             
    def addFeature(self, feature):
        self.features[feature.name] = feature; 
  
class author(object):
    def __init__(self, name):
        self.name = name;
    def setDocs(self, documentFiles):
        self.docFiles = documentFiles;
        self.docs = list();
        for docName in self.docFiles:
            temp_doc = document(self.name, docName);
            self.docs.append(temp_doc);   
       
class feature(object):
    def __init__(self, name, rawFeature):
        self.name        = name; 
        self.featureDict = convert2Frequency(dict(Counter(rawFeature)));
        
    def getFeatureVector(self, globalFeature, n):
        topFeatures     = dict(Counter(globalFeature.chi2).most_common(n))
        return [self.featureDict[key] if self.featureDict.has_key(key) else 0 for key in topFeatures.keys()]


    
class globalFeature(object):
    def __init__(self, name, docList):
        self.name = name;
        self.featureDict = dict()
        for idd, doc in enumerate(docList):
            if not doc.features.has_key(self.name):
                raise Exception('No feature named ' + self.name);
            dfDict = doc.features[name].featureDict;
            for key in set(self.featureDict.keys() + dfDict.keys()):
                if self.featureDict.has_key(key) and dfDict.has_key(key):
                    self.featureDict[key] = iterMean(self.featureDict[key], dfDict[key], idd + 1)
                elif self.featureDict.has_key(key) and not dfDict.has_key(key):
                    self.featureDict[key] = iterMean(self.featureDict[key], 0., idd + 1)
                else:
                    self.featureDict[key] = 1. / (idd + 1) * dfDict[key];
        self.chiSquared(docList)

    def chiSquared(self, docList):            
        self.chi2 = dict.fromkeys(self.featureDict.keys(), 0);
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


def exportARFF(docList, authorList, globalFeature, n, fileName):
    data = dict();
    data['attributes'] = list();
    for ida, attribute in enumerate(globalFeature.getAttributeNames(n)):
        aName = re.sub("[^A-Za-z0-9]+", 'x', attribute.encode('unicode_escape'));
        aName = globalFeature.name + '_' + str(ida) + '_' + aName;
        data['attributes'].append( (aName, 'REAL') )
    
    data['attributes'].append(('author', list([author.name for author in authorList])))
    data['data'] = list();

    for idd, doc in enumerate(docList):
        data['data'].append(doc.features[globalFeature.name].getFeatureVector(globalFeature, n))
        data['data'][idd].append(doc.author)

    data['description'] = ''
    data['relation'] = globalFeature.name

    fHandle = open(fileName, "w")
    arff.dump(data, fHandle)
    fHandle.close()
    return(data)
