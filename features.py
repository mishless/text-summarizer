import math
import textClasses

def title_word_feature(title, processed_text):
	""" List of values from 0 to 1 rating the number title words that appear in the sentence"""
	title_word_feature_values = []
	word_intersection = [set(filter(lambda title_word: title_word in title.bag_of_words, sublist)) for sublist in [sentence.bag_of_words for sentence in processed_text]]
	for word_list in word_intersection:
		title_word_feature_values.append(len(word_list) / len(title.bag_of_words))
	return title_word_feature_values

def sentence_length_feature(sentences):
	sentence_length_feature_values = []
	max_length_sentence = len(sentences[0].original.split(" "))
	for sentence in sentences[1:]:
		if(len(sentence.original.split(" ")) > max_length_sentence):
			max_length_sentence = len(sentence.original.split(" "))
	
	for sentence in sentences:
		sentence_length_feature_values.append(len(sentence.original.split(" "))/max_length_sentence)
		
	return sentence_length_feature_values
		

def sentence_location_feature(sentences):
	sentence_location_feature_values = []
	for sentence in sentences:
		sentence_location_feature_values.append(1/sentence.position)
	return sentence_location_feature_values
	
def keyword_feature(sentences, words):
	keyword_feature_values = []
	total_number_of_sentences = len(sentences)
	for word in words:
		number_of_sentences = 0
		for sentence in sentences:
			if word in sentence.bag_of_words:
				number_of_sentences += 1
		number_of_sentences = 1 if (number_of_sentences == 0) else number_of_sentences  
		words[word].term_weight = words[word].abs_frequency * math.log10(total_number_of_sentences/number_of_sentences)
	for sentence in sentences:
		sum_of_term_weights = 0
		for word in sentence.bag_of_words:
			sum_of_term_weights += words[word].term_weight
		keyword_feature_values.append(sum_of_term_weights)
	
	#map(lambda x: x/max(keyword_feature_values), keyword_feature_values)
	maximum_keyword_feature = max(keyword_feature_values)
	a=0
	while a < len(keyword_feature_values):
		keyword_feature_values[a]/=maximum_keyword_feature
		a+=1
	return keyword_feature_values 
	#return maximum_keyword_feature

def pos_tag_feature(sentences, words, pos_tag):
	""" List of values from 0 to 1 rating the number of words with a certain part of speech tag that appear in the sentence"""
	pos_tag_words_count_list = []
	for sentence in sentences:
		pos_tag_words_count_list.append(len([word for word in sentence.bag_of_words if words[word].part_of_speech[1] == pos_tag]))
	return [pos_tag_words_sentence/max(pos_tag_words_count_list) for pos_tag_words_sentence in pos_tag_words_count_list] if max(pos_tag_words_count_list)!=0 else [0]*len(pos_tag_words_count_list)

def phrase_feature(sentences, phrase_list):
	""" List of values from 0 to 1 rating the number of phrases that appear in the sentence from a list """
	total_number_words = 0
	phrase_frequency = []
	for sentence in sentences:
		total_number_words += len(sentence.bag_of_words)
		count_phrase_per_sentence = 0
		for phrase in phrase_list:
			if phrase in sentence.original:
				count_phrase_per_sentence += 1
		phrase_frequency.append(count_phrase_per_sentence)
	return [frequency/total_number_words for frequency in phrase_frequency]
