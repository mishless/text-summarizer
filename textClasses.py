class Word:
	def __init__(self, stem, term_weight, part_of_speech, synonym_list):
		self.stem = stem
		self.abs_frequency = 1
		self.term_weight = term_weight
		self.part_of_speech = part_of_speech
		self.synonym_list = synonym_list

	def increment_abs_frequency(self):
		self.abs_frequency+=1

	def set_term_weight(self, term_weight):
		self.term_weight = term_weight

class Sentence:
	def __init__(self, original, position, rank, bag_of_words, ending_char):
		self.original = original
		self.position = position
		self.rank = rank
		self.bag_of_words = bag_of_words
		self.ending_char = ending_char

class Title:
	def __init__(self, original, bag_of_words):
		self.original = original
		self.bag_of_words = bag_of_words