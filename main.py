from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import MBSP
import math


def textReader(filename):
    f   = open(filename, "r")
    txt = f.read();
    return txt;
    
def ngram(string, n):
    return [string[idn:idn+n] for idn in xrange(len(string)-n+1)];
    
def ngramFrequency(ngramList):
    counts          = Counter(ngramList);
    ngramNames, ni  = zip(*counts.items()); # ungs: unique ngrams
    sortID          = np.argsort(ni)[::-1]
    ngramNames      = np.array(ngramNames)[sortID];
    ni              = np.array(ni)[sortID];     
    ngramFreq       = ni/(1.*len(ngramList));  
    return ngramNames, ngramFreq

def ngramFrequencyHist(ngramNames, ngramFreq, nmax):
    labels = ngramNames[:nmax+1];
    values = ngramFreq[:nmax+1];
    index  = np.arange(len(labels));
    plt.bar(index, values);
    plt.xticks(index, labels);
    plt.xlabel('n-gram');
    plt.ylabel('frequency');
    plt.show(0);
    
def lexExtraction(text, n):
    wList   = MBSP.Sentence(text, token=[MBSP.WORD]).word;
    words   = [word.string for word in wList]
    



fName   = 'testtext.txt'
text    = textReader(fName);

#n       = 3;
#ngrams  = ngram(text, 3);
#nn, nf  = ngramFrequency(ngrams);
#ngramFrequencyHist(nn, nf, 20);
