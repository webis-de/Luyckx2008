## luyckx2008 - Authorship attribution and verification with many authors and limited data
Part of the Studienstiftung Kolleg "Stylometry and Paraphrasing". This subproject 
attempts to implement the code described in [1]. 

This is a reimplementation of the approach to authorship attribution originally described in

> Kim Luyckx and Walter Daelemans. 2008. [Authorship attribution and verification with many authors and limited data](http://www.aclweb.org/anthology/C08-1065). In Proceedings of the 22nd International Conference on Computational Linguistics - Volume 1 (COLING '08), Vol. 1. Association for Computational Linguistics, Stroudsburg, PA, USA, 513-520. [[paper]](http://www.aclweb.org/anthology/C08-1065)

It was reimplemented as part of a science reproducibility study alongside [14 other authorship attribution approaches](https://github.com/search?q="Who+wrote+the+web"+user:pan-webis-de). The results of the reproducibility study can be found in

> Martin Potthast, ... UPDATE CITATION

If you use this reimplementation in your own research, please make sure to cite both of the above papers.

## Usage

To execute the software, install it and make sure all its dependencies are installed as well; then run the software using the following command:

`python luyckx2008.py <path-to-input-data> <output-path>`

## Usage

To execute the software, install it and make sure all its dependencies are installed as well; then run the software using the following command:

`python koppel11.py <path-to-input-data> <output-path>`

## Input and Output Formats

The software accepts authorship attribution datasets that are formatted according to the corresponding [PAN shared task on authorship attribution](http://pan.webis.de/tasks.html). A number of [datasets can be found there](http://pan.webis.de/data.html), and all of them are formatted as follows.

In a dataset's `TOP_DIRECTORY`, a `meta-file.json` is found which comprises

  - the language of the texts within (e.g., EN, GR, etc.),
  - the names of the subdirectories that contain texts from candidate authors,
  - the name of the subdirectory that contains texts of unknown authorship, and
  - the name of each file of unknown authorship that is to be attributed to one of the candidate authors.
  
The software accepts as input a path to an inflated dataset's `TOP_DIRECTORY` and starts the authorship attribution process from there. The output in the `OUTPUT_PATH` will be a file `answers.json` formatted as follows:

```json
{
"answers": [
	{"unknown_text": "unknown00001.txt", "author": "candidate00001", "score": 0.8},
	{"unknown_text": "unknown00002.txt", "author": "candidate00002", "score": 0.9}
	]
}
```

where `unknown_text` is the name of an unknown text as per `meta-file.json`, `author` is the name of a candidate author as per `meta-file.json`, and `score` is as real value in the range [0,1] which indicates the software's confidence in its attribution (0 means completely uncertain, 1 means completely sure).


## Dependencies

To operate the software, the following packages should be installed:
  - python 2.7
  - numpy 1.13.3 or above
  - Memory Based Sharlow Parser 1.4[MBSP](https://www.clips.uantwerpen.be/pages/MBSP)
  - Tilburg Memory Based Learner 6.15 [Timbl](https://languagemachines.github.io/timbl/)

## License

Copyright (c) 2018 Yanis Taege

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
