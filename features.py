def title_word_feature(title, processed_text):
	title_word_feature_values = []
	title.bag_of_words
	processed_text
	word_intersection = [set(filter(lambda title_word: title_word in title.bag_of_words, sublist)) for sublist in [sentence.bag_of_words for sentence in processed_text]]
	print(word_intersection)
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
		sentence_location_feature_values.append(10/sentences(sentence))
	return sentence_location_feature_values
	
def keyword_feature(sentences):
	total_number_of_sentences = len(sentences)
	