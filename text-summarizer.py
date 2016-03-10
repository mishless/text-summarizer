import sys
import os
import collections
import nltk.data
import string
import math
import features
import traceback
import textClasses as tc 

from argparse import ArgumentParser
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.corpus import wordnet as wn
from functools import reduce

import cluster

def pre_process_text(text):
	text = text.split('\n', 1)
	title = tc.Title(text[0], [])
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
		if (token not in words) and (token not in list(string.punctuation) and (token not in stopwords_list)):
				words[token] = tc.Word(stemmer.stem(token), 0, word_pos, [lemma for synset in wn.synsets(token) for lemma in synset.lemma_names()])
		title.bag_of_words.append(token)

	#Pre-process text
	for detected_sentence in detected_sentences:
		sentences.append(tc.Sentence(detected_sentence, len(sentences) + 1, 0, [], None))
		tokens = nltk.word_tokenize(sentences[-1].original)
		tokens = [token for token in tokens if token not in stopwords_list]
		part_of_speech = nltk.pos_tag(tokens)
		for (token, word_pos) in zip(tokens, part_of_speech):
			token = token.lower()
			if (token not in list(string.punctuation) and (token not in stopwords_list)):
				if (token not in words):
					words[token] = tc.Word(stemmer.stem(token), 0, word_pos, [lemma for synset in wn.synsets(token) for lemma in synset.lemma_names()])
				elif token in words:
					words[token].increment_abs_frequency()
				sentences[-1].bag_of_words.append(token)
	return [title, sentences, words]

def process_input(argv=None):
	if argv is None:
		argv = sys.argv
	else:
		sys.argv.extend(argv)
	parser = ArgumentParser()
	parser.add_argument("-t", "--text-file", dest="text_file", help="the file containing the text tom be summarized", required=True)
	parser.add_argument("-p", "--percent", dest="percentage", help="the compression rate as percentage", required=True)

	# Process arguments
	args = parser.parse_args()

	percentage = args.percentage
	text_file = args.text_file
	with open(text_file, 'r') as f:
		text = f.read()
	f.closed

	return {"text": text, "percentage": percentage}

def main():
	try:
		processed_input = process_input()
		text = processed_input['text']
		percentage = processed_input['percentage']
		preprocessed_text = pre_process_text(text)
		similarities = cluster.calculate_cosine_similarity(preprocessed_text[1], preprocessed_text[2])
		proper_noun_feature_value = features.pos_tag_feature(preprocessed_text[1], preprocessed_text[2], 'NNP')
		numerical_data_feature_value = features.pos_tag_feature(preprocessed_text[1], preprocessed_text[2], 'CD')
		title_word_feature_value = features.title_word_feature(preprocessed_text[0], preprocessed_text[1])
		keyword_feature_value = features.keyword_feature(preprocessed_text[1], preprocessed_text[2])
		k_means_result = cluster.k_means(preprocessed_text[1], preprocessed_text[2], percentage)
		return 0
	except KeyboardInterrupt:
		### handle keyboard interrupt ###
		return 0
	except Exception as e:
		sys.stderr.write(repr(e))
		traceback.print_tb(e.__traceback__)
		return 2

if __name__ == "__main__":
	sys.exit(main())