


def title_word_feature(title, processed_text):
	""" List of values from 0 to 1 rating the number title words that appear in the sentence"""
	title_word_feature_values = []
	word_intersection = [set(filter(lambda title_word: title_word in title, sublist)) for sublist in sentences]
	print(word_intersection)
	for word_list in word_intersection:
		title_word_feature_values.append(len(word_list) / len(title.bag_of_words))
	return title_word_feature_values
	