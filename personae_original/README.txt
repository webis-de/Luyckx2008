------------------------------------------------------------------------------------------
Personae Corpus
------------------------------------------------------------------------------------------

Creator(s):
	CLiPS Research Center, University of Antwerp
	Kim Luyckx, Walter Daelemans
	http://www.clips.uantwerpen.be
    
Version: 2013-11-26
Language: Dutch

This dataset is available at http://www.clips.uantwerpen.be/datasets

License:
	The dataset is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 
	3.0 Unported License. Please read the terms of use carefully.
	http://creativecommons.org/licenses/by-nc-sa/3.0
	(Full legal code enclosed: License.txt)
	For commercial and other uses, please contact Walter Daelemans (walter.daelemans@uantwerpen.be)

Description:
	The Personae corpus was collected for experiments in Authorship Attribution and 
	Personality Prediction. It consists of 145 Dutch-language essays, written by 145 
	different students (BA in Linguistics and Literature at the University of Antwerp, 
	Belgium). Each student also took an online MBTI personality test, allowing personality 
	prediction experiments. The corpus was controlled for topic, register, genre, age, 
	and education level. 
	We make available the original texts, a syntactically annotated version of the texts, 
	and the metadata.

If you use this dataset in your research, make sure to cite the following paper:

	Kim Luyckx and Walter Daelemans (2008). Personae, a Corpus for Author and Personality 
	Prediction from Text. In Proceedings of the Sixth International Conference on Language 
	Resources and Evaluation (LREC 2008), Marrakech, Morocco.
	(Full paper at http://www.clips.uantwerpen.be/bibliography/personae-a-corpus-for-author-and-personality-prediction-from-text)

Acknowledgement:
	The construction of the corpus was made possible by a grant from the Flemish Research 
	Foundation (FWO) for the 'Computational Techniques for Stylometry for Dutch' project.

------------------------------------------------------------------------------------------

Corpus
------
data/ contains the original texts (tokenized)
mbsp/ contains a syntactically annotated version of the texts
Both file types are in UTF-8 encoding
Metadata are in the filenames (see: File Naming Conventions)

Syntactic Annotation (MBSP)
---------------------------
We use the Memory-Based Shallow Parser (MBSP) (demo: http://www.cnts.ua.ac.be/cgi-bin/jmeyhi/MBSP-instant-webdemo.cgi), which performs tokenization, POS-tagging, chunking, relation finding, and NER.

Daelemans, W. and van den Bosch, A. (2005) Memory-Based Language Processing. Studies in Natural Language Processing. Cambridge: Cambridge University Press.

File Naming Conventions
-----------------------
<author_number>.<gender>.<MBTI_profile>.<mother_tongue>.<region>.txt
e.g. 1.female.ENFJ.Dutch.OV.txt

MBTI Profile
------------
Based on C.G. Jung's personality typology which characterizes a person according to four preferences:
- Introverted / Extraverted
- iNtuition / Sensing
- Feeling / Thinking
- Judging / Perceiving

Region
------
A = Antwerpen (capital is Antwerpen)
B = Vlaams-Brabant (capital is Leuven)
L = Limburg (capital is Hasselt)
OV = Oost-Vlaanderen (Eastern Flanders; capital is Gent)
WV = West-Vlaanderen (Western Flanders; capital is Brugge)
Other
