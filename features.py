def title_word_feature(title, processed_text):
	title_word_feature_values = []
	title.bag_of_words
	processed_text
	word_intersection = [set(filter(lambda title_word: title_word in title.bag_of_words, sublist)) for sublist in [sentence.bag_of_words for sentence in processed_text]]
	print(word_intersection)
	for word_list in word_intersection:
		title_word_feature_values.append(len(word_list) / len(title.bag_of_words))
	return title_word_feature_values