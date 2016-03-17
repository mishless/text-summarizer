# Briefly

## What is Briefly?
Briefly is a text-summarization tool developed for the Intelligent Systems Master Course at MdH (Sweden) by:
* K. Dobrovoljski
* A. Paredes
* M. Stoycheva
* V. Turkulov

### Characteristics

- Core: Python 3.5.1
- Web-server: Node.js
- Front-End: Bootstrap, CSS3 & jQuery + Jade

Briefly create [extraction base summaries](https://en.wikipedia.org/wiki/Automatic_summarization#Extraction-based_summarization) using Fuzzy Logic + Clustering techniques.

The features selected to evaluate and rank the sentences are:

1. Keyword
2. Sentence Lenght
3. Sentence Position
4. Title Words
5. Proper Nouns
6. Numerical Data
7. Cue Phrases
8. Stigma Words

## Install

### Python

To run the python code we need to install the following libraries:

```
pip install pexpect unidecode jsonrpclib pexpect numpy cycler
```

Then in CMD:

```
python
nltk.download()
``` 

And download all the packages

### Node.js

In the folder text-summarizer-server we install the packages throught the package manager:

```
npm install
```
Packages info:

* body-parser ~1.13.2
* cookie-parser ~1.3.5
* debug ~2.2.0
* ejs ~2.4.1
* morgan ~1.6.1
* serve-favicon 
* dateformat ~1.0.12
* python-shell ~0.4.0
* jade


