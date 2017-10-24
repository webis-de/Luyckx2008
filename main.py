from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import MBSP
import math
        
class document(object):
    def __init__(self, author, filename):
        self.author     = author;
        self.fileName   = filename;
        self.readText();
        
    def textReader(self, filename):
        """ Simple Text Reader """
        f   = open(filename, "r")
        txt = f.read();
        return txt;
        
    def readText(self):
        self.text = self.textReader(self.fileName);
        
    def parserExtraction(self, text):
        """ Uses the MBSP parser on text 
        Parameters
        ----------
        text : string
            input text
        
        Returns
        ------
        list lex
            List of lexical features
        list pos
            List of Parts-of-Speech tags
        """
        p = MBSP.parse(text);
        s = MBSP.split(p);
        lex = [u''];
        pos = [u''];
        for sentence in s:
            lex += [w.string for w in sentence.word]
            pos += sentence.parts_of_speech
        return lex, pos
        
    def parseText(self):
        self.lex, self.pos = self.parserExtraction(self.text);
      
    def setFeatures(self, features):
        self.features = features; 
    
class author(object):
    def __init__(self, name):
        self.name = name;
    def setDocs(self, documentFiles):
        self.docFiles = documentFiles;
        self.docs = list();
        for docName in self.docFiles:
            temp_doc = document(self.name, docName);
            temp_doc.readText();
            temp_doc.parseText();
            self.docs.append(temp_doc);   
              
        
class features(object):
    """ 
    Feature Class: In this class, all features (dictionaries) shall be stored.
    Each feature type is denoted by an attribute of the class (e.g. featires.lex)
    Since most of the time n-grams are used, these features classes can be multi
    dimensonal, where in n = i-1th features.feature[i]. 
    """
    def __init__(self):
        global nmax;
        nmax      = 3;
        self.lex  = np.arange(nmax, dtype=object);
        self.pos  = np.arange(nmax, dtype=object);
        
    def makeGlobalFeatures(self, authorList):
        # needs to be adjusted for using lists of documents
        """ Takes an authorlist and makes the current object the total feature 
            dictionary.
            
            Arguments
            ---------
            authorlist : list
                list containing author objects        
        """
        self.globalFeature = 1;
        for idn in xrange(0, nmax):
            self.lex[idn] = Counter();
            self.pos[idn] = Counter();
            
        for authors in authorList:
            for docs in authors.docs:
                for n in xrange(1, nmax+1):
                    self.lex[n-1] = self.lex[n-1] + Counter(self.ngram(docs.lex,n));
                    self.pos[n-1] = self.pos[n-1] + Counter(self.ngram(docs.pos,n));
                    
        for idn in xrange(0, nmax):
            self.lex[idn] = self.convert2Frequency(dict(self.lex[idn]))
            self.pos[idn] = self.convert2Frequency(dict(self.pos[idn]))
            

     
        
    def ngram(self, flist, n):    
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
        
    def convert2Frequency(self, featureDict):
        invTotalNumber = 1.0 / sum(featureDict.values());
        featureDict.update((k, invTotalNumber*v) for k,v in featureDict.items());
        return featureDict

    def setDocumentFeatures(self, globalFeature, doc):        
        docFeatures = features();
        
        for n in xrange(1, nmax+1):
            docFeatures.lex[n-1] = dict.fromkeys(globalFeature.lex[n-1].keys(), []);
            docFeatures.pos[n-1] = dict.fromkeys(globalFeature.pos[n-1].keys(), []);
            
            lex_in = dict(Counter(self.ngram(doc.lex, n)));
            for key in self.lex[n-1].keys():
                if lex_in.has_key(key):
                    docFeatures.lex[n-1][key] = lex_in[key];
                else:
                    docFeatures.lex[n-1][key] = 0;
                    
            pos_in = dict(Counter(self.ngram(doc.pos, n)));
            for key in self.pos[n-1].keys():
                if pos_in.has_key(key):
                    docFeatures.pos[n-1][key] = pos_in[key]
                else:
                    docFeatures.pos[n-1][key] = 0;   
            docFeatures.lex[n-1] = docFeatures.convert2Frequency(docFeatures.lex[n-1]);   
            docFeatures.pos[n-1] = docFeatures.convert2Frequency(docFeatures.pos[n-1]);   
        doc.setFeatures(docFeatures);
        
    def setAllDocumentFeatures(self, authorlist):
        if hasattr(self, 'globalFeature'):
            for authors in authorlist:
                for docs in authors.docs:
                    self.setDocumentFeatures(self, docs)
        else:
            raise Exception('features have to be global')

    def chiSquared(self, doclist):
        if hasattr(self, 'globalFeature'):
            self.chi_lex  = np.arange(nmax, dtype=object);
            self.chi_pos  = np.arange(nmax, dtype=object);
            for n in xrange(1, nmax+1):
                self.chi_lex[n-1] = dict.fromkeys(self.lex[n-1].keys(), 0);
                self.chi_pos[n-1] = dict.fromkeys(self.pos[n-1].keys(), 0);
                for keys in self.chi_lex[n-1].keys():
                    val_i = np.array([doc.features.lex[n-1][keys] for doc in doclist])
                    chi_i = (val_i - self.lex[n-1][keys] )**2
                    self.chi_lex[n-1][keys] = sum(1.0 * chi_i / self.lex[n-1][keys]);
                    
                for keys in self.chi_pos[n-1].keys():
                    val_i = np.array([doc.features.pos[n-1][keys] for doc in doclist])
                    chi_i = (val_i - self.pos[n-1][keys] )**2
                    self.chi_pos[n-1][keys] = sum(1.0 * chi_i / self.pos[n-1][keys]);          
        else:
            raise Exception('features have to be global')

def getAllDocuments(authorlist):
    documentlist = [];
    for authors in authorlist:
        [documentlist.append(doc) for doc in authors.docs];
    return documentlist;
    
a = list();
a.append(author('1st'));
a.append(author('2nd'));
a[0].setDocs(['ttext1.txt']);
a[1].setDocs(['ttext2.txt']);

f = features();
f.makeGlobalFeatures(a);
f.setAllDocumentFeatures(a);
f.chiSquared(getAllDocuments(a))

















