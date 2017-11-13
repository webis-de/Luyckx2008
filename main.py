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
        return [self.featureDict[key] for key in topFeatures.keys()]
    
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
    
    data['attributes'].append(('author', list([author.name for author in authors])))
    data['data'] = list();

    for idd, doc in enumerate(docList):
        data['data'].append(doc.features[globalFeature.name].getFeatureVector(globalFeature, n))
        data['data'][idd].append(doc.author)

    data['description'] = '';
    data['relation'] = globalFeature.name;

    fHandle = open(fileName, "w");
    arff.dump(data, fHandle);
    fHandle.close();
    return(data);

authorDict = personae.getAuthorFileList(2)
authors    = list();
for idak, authorKey in enumerate(authorDict.keys()):
    authors.append(author(authorKey))
    print 'loading author documents of '+authorKey
    authors[idak].setDocs(authorDict[authorKey])
    print '.. loaded'

docs = getAllDocuments(authors);

globalFeatures = dict.fromkeys((docs[0].rawFeatures.keys()));

for key in globalFeatures:
    globalFeatures[key] = feature(key);
    globalFeatures[key].makeGlobalFeature(docs);
    globalFeatures[key].chiSquared(docs);   
    exportARFF(docs, authors, globalFeatures[key], 5, 'features/'+key+'.arff')
    
f = 'pos1'
x = globalFeatures[f]
y = docs[0].features[f]
        




