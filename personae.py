from os import listdir
from os.path import isfile, join

def arange(personae_data_path):
    personae_data_path = 'personae_original/';
    files = [f for f in listdir(personae_data_path) if isfile(join(personae_data_path, f))]

    for idf, fileName in enumerate(files):
        fileHandle = open(personae_data_path + fileName, "r");
        fullText   = fileHandle.read();
        fileHandle.close();
        splitText  = fullText.split();
        nWords     = len(splitText);
        nPart      = round(nWords/10);
        
        for idp in range(0,9):
            outHandle = open('personae/' + str(idf) + '-' + str(idp) + '.txt', 'w');
            outHandle.write(' '.join(splitText[idp*nPart:(idp+1)*nPart]))
            outHandle.close();
            
        outHandle = open('personae/' + str(idf) + '-9.txt', 'w');
        outHandle.write(' '.join(splitText[9*nPart:]))
        outHandle.close();    
          
def getAuthorFileList(nAuthors):
    aDict = dict();
    for ida in range(0,nAuthors+1):
        aDict['a'+str(ida)] = ['personae/'+str(ida)+'-'+str(idf)+'.txt' for idf in range(0,9)]
    
    return aDict
