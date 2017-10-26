from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import MBSP
import math

def parseText(text):
    p = MBSP.parse(text);
    s = MBSP.split(p);
    lex = [u''];
    pos = [u''];
    for sentence in s:
        lex += [w.string for w in sentence.word];
        pos += sentence.parts_of_speech;  
    
    features = dict();
    
    for n in xrange(1,4):
        features['lex%d'%n] = ngram(lex,n);
        features['pos%d'%n] = ngram(pos,n);
    return features    
    
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
    
    
    
    
class document(object):
    def __init__(self, author, filename):
        self.author         = author;
        self.fileName       = filename;
        self.readText();
        self.features       = dict();
        
    def textReader(self, filename):
        """ Simple Text Reader """
        f   = open(filename, "r")
        txt = f.read();
        return txt;
        
    def readText(self):
        inText           = self.textReader(self.fileName);
        self.rawFeatures = parseText(inText);
             
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
    def __init__(self, name):
        self.featureDict = dict() 
        self.name        = name;
        
    def makeDocumentFeature(self, doc):
        if not hasattr(self, 'globalFeature'):
            raise Exception('Variable is not a global feature');
        
        newFeatureDict  = dict.fromkeys(self.featureDict.keys(), 0);
        inFeature       = dict(Counter(doc.rawFeatures[self.name]))       
        
        for key in newFeatureDict.keys():
            if inFeature.has_key(key):
                newFeatureDict[key] = inFeature[key];
            else:
                newFeatureDict[key] = 0;
                   
        newFeature             = feature(self.name);
        newFeature.featureDict = convert2Frequency(newFeatureDict);    
        doc.addFeature(newFeature);      
                
    def makeGlobalFeature(self, docList):
        self.globalFeature = 1
        cFeature      = Counter();
        for doc in docList:
            if not doc.rawFeatures.has_key(self.name):
                raise Exception('No raw feature named ' + self.name);
               
            cFeature      += cFeature + Counter(doc.rawFeatures[self.name]);
        
        self.featureDict = convert2Frequency(dict(cFeature));
        
        for doc in docList:
            self.makeDocumentFeature(doc);
            
    def chiSquared(self, docList):
        if not hasattr(self, 'globalFeature'):
            raise Exception('features have to be global')
        
        self.chi2 = dict.fromkeys(self.featureDict.keys(), 0);
        for key in self.featureDict.keys():
            val_i = np.array([doc.features[self.name].featureDict[key] for doc in docList])
            chi_i = (val_i - self.featureDict[key] )**2
            self.chi2[key] = sum(1.0 * chi_i / self.featureDict[key]);     
               
    def getFeatureVector(self, globalFeature, n):
        topFeatures     = dict(Counter(globalFeature.chi2).most_common(n))
        
        print [key for key in topFeatures.keys()]
        return np.array([self.featureDict[key] for key in topFeatures.keys()])
        
        
        
authors = list();
authors.append(author('1st'));
authors.append(author('2nd'));
#authors.append(author('3rd'));

#authors[0].setDocs(['1.female.ENFJ.Dutch.OV.txt']);
#authors[1].setDocs(['2.female.ENFJ.Dutch.L.txt']);

authors[0].setDocs(['ttext1.txt']);
authors[1].setDocs(['ttext2.txt']);
#authors[2].setDocs(['ttext3.txt']);

docs = getAllDocuments(authors);

globalFeatures = dict.fromkeys((docs[0].rawFeatures.keys()));

for key in globalFeatures:
    globalFeatures[key] = feature(key);
    globalFeatures[key].makeGlobalFeature(docs);
    globalFeatures[key].chiSquared(docs);
    
x = globalFeatures['lex1']
y = docs[0].features['lex1']
    

#f.makeGlobalFeatures(a);
#f.setAllDocumentFeatures(a);
#f.chiSquared(getAllDocuments(a))
#



















