def ngram(s, n):
    ''' returns the n-gram of a string s as a list '''
    return [s[idn:idn+n] for idn in xrange(len(s)-n+1)];
    
def ngram_list(ulist, n):
    ''' returns all n-grams of a unicode list ulist as a list'''
    nlist = [u''];
    for x in ulist:
        nlist += ngram(x,n)
    return nlist 
    

def lFrequency(plist, wdict):
    freq = np.zeros(len(wdict))
    for w in xrange(len(wdict)):
        freq[w] = plist.count(wdict[w])
    return freq
    
    
"""
def wFrequency(ngramList):
    ''' Calculates the frequency of each str in the list ngramList, and returns
    a sorted list of the names with their respective frequencies
    '''
    counts          = Counter(ngramList);
    ngramNames, ni  = zip(*counts.items()); # ungs: unique ngrams
    sortID          = np.argsort(ni)[::-1]
    ngramNames      = np.array(ngramNames)[sortID];
    ni              = np.array(ni)[sortID];     
    ngramFreq       = ni/(1.*len(ngramList));  
    return ngramNames, ngramFreq

def fHist(ngramNames, ngramFreq, nmax):
    ''' Shows the frequency histogram of words w '''
    labels = ngramNames[:nmax+1];
    values = ngramFreq[:nmax+1];
    index  = np.arange(len(labels));
    plt.bar(index, values);
    plt.xticks(index, labels);
    plt.xlabel('n-gram');
    plt.ylabel('frequency in counts per # of words');
    plt.show(0);
    


#def chi2(feat_author, feat_all, feat_all_freq):
#    for f in feat_all:
        
''' Test Section '''

### 1 load all texts/add them to authors
a = list();
a.append(author('1st'));
a.append(author('2nd'));
a[0].setDocs(['ttext1.txt']);
a[1].setDocs(['ttext2.txt']);

f = features(a);
#gDictionary = globalDict(a);
    
# extract all features

fName    = [];
fName.append('ttext1.txt');
fName.append('ttext2.txt');

lex_all = []; # terrible style, please redo: !!1
pos_all = []; # !!1
lex_aut = [];
pos_aut = [];
nmax    = 3;
for f in fName:
    l, p = parserExtraction(textReader(f));
    lex_aut.append(l);
    pos_aut.append(p);
    lex_all += l; # !!1
    pos_all += p; # !!1    
    
lex  = np.arange(nmax, dtype=object);
pos  = np.arange(nmax, dtype=object);
fwd  = Counter(lex_all);

for n in xrange(1,nmax+1):
    lex[n-1] = Counter(ngram(lex_all, n));
    pos[n-1] = Counter(ngram(pos_all, n));
    
lex  = np.arange(len(fName), dtype=object);
pos  = np.arange(len(fName), dtype=object);  
fwd  = np.arange(len(fName), dtype=object);  


    
fwd  = Counter(lex_all);
lex  = np.arange(3, dtype=object);
pos  = np.arange(3, dtype=object);
flex  = np.arange(3, dtype=object);
fpos  = np.arange(3, dtype=object);
fwd  = np.zeros(len(fName));

for n in xrange(1,4):
    lex[n-1]  = Counter(ngram_list(lex_all, n));
    pos[n-1]  = Counter(ngram_list(pos_all, n));
    flex[n-1] = np.zeros([len(fName), len(lex[n-1])])
    fpos[n-1] = np.zeros([len(fName), len(lex[n-1])])
    # convert author features
    for a in xrange(len(fName)):
        for idk in xrange(len(lex[n-1].keys())):
            flex[n-1][a][idk] = ngram_list(lex_aut[a], n).count(lex[n-1].keys()[idk]);
            
        for idk in xrange(len(pos[n-1].keys())):
            fpos[n-1][a][idk] = ngram_list(pos_aut[a], n).count(pos[n-1].keys()[idk]);

lex, pos = featureExtraction(text);

nlex = ngram_list(lex, 2);
npos = ngram_list(pos, 2);
nnl, nfl = wFrequency(nlex);
nnp, nfp = wFrequency(npos);


'''
