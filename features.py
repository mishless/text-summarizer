def title_word_feature(title, processed_text):
	""" List of values from 0 to 1 rating the number title words that appear in the sentence"""
	title_word_feature_values = []
	word_intersection = [set(filter(lambda title_word: title_word in title.bag_of_words, sublist)) for sublist in [sentence.bag_of_words for sentence in processed_text]]
	for word_list in word_intersection:
		title_word_feature_values.append(len(word_list) / len(title.bag_of_words))
	return title_word_feature_values

def sentence_length_feature(sentences):
	sentence_length_feature_values = []
	max_length_sentence = len(sentences[0].split(" "))
	for sentence in sentences[1:]:
		if(len(sentence.split(" ")) > max_length_sentence):
			max_length_sentence = len(sentence.split(" "))
	
	for sentence in sentences:
		sentence_length_feature_values.append(len(sentence.split(" "))/max_length_sentence)
		
	return sentence_length_feature_values
		

def sentence_location_feature(sentences):
	sentence_location_feature_values = []
	for sentence in sentences:
		sentence_location_feature_values.append(10/sentence.pos)
	return sentence_location_feature_values
	
def keyword_feature(sentences):
	total_number_of_sentences = len(sentences)

def pos_tag_feature(sentences, words, pos_tag):
	""" List of values from 0 to 1 rating the number of words with a certain part of speech tag that appear in the sentence"""
	pos_tag_words_count_list = []
	for sentence in sentences:
		pos_tag_words_count_list.append(len([word for word in sentence.bag_of_words if words[word].part_of_speech[1] == pos_tag]))
	return [pos_tag_words_sentence/max(pos_tag_words_count_list) for pos_tag_words_sentence in pos_tag_words_count_list] if max(pos_tag_words_count_list)!=0 else [0]*len(pos_tag_words_count_list)    


