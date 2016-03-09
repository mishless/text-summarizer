import math

from nltk.stem.porter import *
from functools import reduce

def calculate_similarities(sentences, words):
	similarities = dict()
	max_words_in_common = 1
	max_synonyms_in_common = 1
	for first_senetence in sentences:
		if (first_senetence.position not in similarities):
			similarities[first_senetence.position] = dict()
			for second_sentence in sentences:
				if (second_sentence.position not in similarities[first_senetence.position]):
					similarities[first_senetence.position][second_sentence.position] = None;
					if (first_senetence.position != second_sentence.position):
						words_in_common = 0
						synonyms_in_common = 0
						for word in first_senetence.bag_of_words:
							for second_word in second_sentence.bag_of_words:
								if (words[word].stem == words[second_word].stem):
									words_in_common += 1
								if (word != second_word):
									if (word in words[second_word].synonym_list):
										synonyms_in_common += 1
									if (second_word in words[word].synonym_list):
										synonyms_in_common += 1
						similarities[first_senetence.position][second_sentence.position] = [words_in_common, synonyms_in_common]
						if (words_in_common > max_words_in_common):
							max_words_in_common = words_in_common
						if (synonyms_in_common > max_synonyms_in_common):
							max_synonyms_in_common = synonyms_in_common
	for first_senetence in sentences:
		for second_sentence in sentences:
			if (first_senetence.position != second_sentence.position):
				similarities[first_senetence.position][second_sentence.position] = similarities[first_senetence.position][second_sentence.position][0]/max_words_in_common + similarities[first_senetence.position][second_sentence.position][1]/max_synonyms_in_common
	return similarities

def calculate_cosine_similarity(sentences, words):
	stemmer = PorterStemmer()
	similarities = dict()
	for first_senetence in sentences:
		if (first_senetence.position not in similarities):
			similarities[first_senetence.position] = dict()
			for second_sentence in sentences:
				if (second_sentence.position not in similarities[first_senetence.position]):
					similarities[first_senetence.position][second_sentence.position] = None;
					if (first_senetence.position != second_sentence.position):
						bag_of_words = list(set(first_senetence.bag_of_words) | set(second_sentence.bag_of_words))
						bag_of_words = [list(set(words[word].synonym_list + [word])) for word in bag_of_words]
						first_sentence_vector = [reduce(lambda x, y: x + y, [[stemmer.stem(sentence_word) for sentence_word in first_senetence.bag_of_words].count(stemmer.stem(word)) for word in synonyms]) for synonyms in bag_of_words]
						second_sentence_vector = [reduce(lambda x, y: x + y, [[stemmer.stem(sentence_word) for sentence_word in second_sentence.bag_of_words].count(stemmer.stem(word)) for word in synonyms]) for synonyms in bag_of_words]
						denominator = math.sqrt(reduce(lambda x, y: x + y, map(lambda x: x * x, first_sentence_vector)))*math.sqrt(reduce(lambda x, y: x + y, map(lambda x: x * x, second_sentence_vector)))
						similarities[first_senetence.position][second_sentence.position] = reduce(lambda x, y: x + y, [first*second for first, second in zip(first_sentence_vector, second_sentence_vector)])/denominator
	return similarities

def calculate_number_of_clusters(sentences, words):
	accumulates_len_of_sentences = reduce(lambda x, y: x + y, [len(sentence.bag_of_words) for sentence in sentences])
	return len(words) / accumulates_len_of_sentences