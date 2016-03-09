import sys
import os
import collections
import nltk.data
import string
import math
import features

from argparse import ArgumentParser
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.corpus import wordnet as wn
from functools import reduce

import cluster

def pre_process_text(text):
	text = text.split('\n', 1)
	title = Title(text[0], [])
	text = text[1]
	words = dict()
	sentences = []
	
	sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	detected_sentences = sentence_detector.tokenize(text.strip())
	stopwords_list = stopwords.words('english')
	stemmer = PorterStemmer()
	
	#Pre-process title
	tokens = nltk.word_tokenize(title.original)
	tokens = [token for token in tokens if token not in stopwords_list]
	part_of_speech = nltk.pos_tag(tokens)
	for (token, word_pos) in zip(tokens, part_of_speech):
		token = token.lower()
		if (token not in words) and (token not in list(string.punctuation)):
				words[token] = Word(stemmer.stem(token), 0, 0, word_pos, [lemma for synset in wn.synsets(token) for lemma in synset.lemma_names()])
		title.bag_of_words.append(token)

	#Pre-process text
	for detected_sentence in detected_sentences:
		sentences.append(Sentence(detected_sentence, len(sentences) + 1, 0, [], None))
		tokens = nltk.word_tokenize(sentences[-1].original)
		tokens = [token for token in tokens if token not in stopwords_list]
		part_of_speech = nltk.pos_tag(tokens)
		for (token, word_pos) in zip(tokens, part_of_speech):
			token = token.lower()
			if (token not in list(string.punctuation)):
				if (token not in words):
					words[token] = Word(stemmer.stem(token), 1, 0, word_pos, [lemma for synset in wn.synsets(token) for lemma in synset.lemma_names()])
				elif token in words:
					words[token] =  Word(stemmer.stem(token), words[token].abs_frequency + 1, 0, word_pos, [lemma for synset in wn.synsets(token) for lemma in synset.lemma_names()])
				sentences[-1].bag_of_words.append(token)
	return [title, sentences, words]

def process_input(argv=None):
	if argv is None:
		argv = sys.argv
	else:
		sys.argv.extend(argv)
	parser = ArgumentParser()
	parser.add_argument("-t", "--text-file", dest="text_file", help="the file containing the text tom be summarized", required=True)

	# Process arguments
	args = parser.parse_args()

	text_file = args.text_file
	with open(text_file, 'r') as f:
		text = f.read()
	f.closed
	return text

def main():
	try:
		text = process_input()
		preprocessed_text = pre_process_text(text)
		similarities = cluster.calculate_cosine_similarity(preprocessed_text[1], preprocessed_text[2])
		proper_noun_feature_value = features.pos_tag_feature(preprocessed_text[1], preprocessed_text[2], 'NNP')
		numerical_data_feature_value = features.pos_tag_feature(preprocessed_text[1], preprocessed_text[2], 'CD')
		title_word_feature_value = features.title_word_feature(preprocessed_text[0], preprocessed_text[1])
		return 0
	except KeyboardInterrupt:
		### handle keyboard interrupt ###
		return 0
	except Exception as e:
		sys.stderr.write(repr(e))
		return 2

if __name__ == "__main__":
	Word = collections.namedtuple("Word", ["stem", "abs_frequency", "term_weight", "part_of_speech", "synonym_list"])
	Sentence = collections.namedtuple("Sentence", ["original", "position", "rank", "bag_of_words", "ending_char"])
	Title = collections.namedtuple("Title", ["original", "bag_of_words"])
	sys.exit(main())