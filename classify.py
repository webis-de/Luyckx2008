import numpy as np
from subprocess import call
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt  

import weka.core.jvm as jvm
from weka.classifiers import Classifier
from weka.core.converters import Loader, Saver



loader = Loader(classname="weka.core.converters.ArffLoader")
cls = Classifier(classname="weka.classifiers.functions.SMO")
cls.options = ["-C", "1.0"];
jvm.start()

nAuthors = [2, 5, 10, 20, 50, 100, 145]
features = ('lex1', 'lex2', 'lex3', 
            'pos1', 'pos2', 'pos3')
            
            
accuracy = np.zeros( (len(nAuthors), len(features)) )


for idn,n in enumerate(nAuthors):
    for idk,key in enumerate(features):
        a = np.zeros(5)
        data = loader.load_file
        for N in range(0,5):
            fName = 'features/N-%.3d_%s_cv%d.arff.cv.%%' % (n, key, N+1)
            # call(['Timbl', '+%', '-t', 'cross_validate', '-f', fName[:-14:] + '_files', '-F', 'ARFF']);
            fHandle = open(fName, "r")
            a[N] = float(fHandle.readline())
            fHandle.close()
        
        accuracy[idn, idk] = 0.01 * np.mean(a);
        
fMarkers = ('d', '.', '^', 'o', '+', 'v', 'r')
for idk in range(0, len(features)):
    plt.plot(nAuthors, accuracy[:,idk], fMarkers[idk]+':');

plt.legend(features)
plt.show(0)
    
    
jvm.stop()
