from LuyckxFeatures import *
from os import listdir
from os.path import isfile, join, splitext

def arange(personae_data_path):
    personae_data_path = 'personae_original/';
    files = [f for f in listdir(personae_data_path) if isfile(join(personae_data_path, f))]
    

    for idf, fileName in enumerate(files):
        fileHandle = open(personae_data_path + fileName, "r");
        fullText   = fileHandle.read();
        fileHandle.close();
        splitText  = fullText.split();
        nWords     = len(splitText);
        nPart      = int(round(nWords/10));
        
        for idp in range(0,10):
            outHandle = open('personae/' + str(idf) + '-' + str(idp) + '.txt', 'w');
            outHandle.write(' '.join(splitText[idp*nPart:(idp+1)*nPart]))
            outHandle.close();
            
        outHandle = open('personae/' + str(idf) + '-9.txt', 'w');
        outHandle.write(' '.join(splitText[9*nPart:]))
        outHandle.close();    
          
def getAuthorFileList(nAuthors):
    authorDict = dict();
    fileList   = list()
    for ida in range(0,nAuthors):
        authorDict['a'+str(ida+1)] = ['personae/'+str(ida)+'-'+str(idf)+'.txt' for idf in range(0,10)]
        [fileList.append(f) for f in authorDict['a'+str(ida+1)]]
    return authorDict, fileList
    
def getFeaturedAuthors(nAuthors, parseBool):
    authorDict, fileList = getAuthorFileList(nAuthors);
    if parseBool: parseCorpus(fileList)
    authors    = list();
    for idak, authorKey in enumerate(authorDict.keys()):
        authors.append(author(authorKey))
        for fName in authorDict[authorKey]:
            pName = splitext(fName)[0] + '.mbsp'
            authors[idak].addDoc(fName, pName)
    return authors
