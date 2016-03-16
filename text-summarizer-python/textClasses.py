class Word:
    def __init__(self, stem, part_of_speech, synonym_list):
        self.stem = stem
        self.abs_frequency = 1
        self.part_of_speech = part_of_speech
        self.synonym_list = synonym_list

    @property
    def term_weight(self):
        return self.__term_weight if self.__term_weight else 0
    
    @term_weight.setter
    def term_weight(self, val):
        self.__term_weight = val

    def increment_abs_frequency(self):
        self.abs_frequency += 1

class Sentence:
    def __init__(self, original, position, bag_of_words, stemmed_bag_of_words, ending_char):
        self.original = original
        self.position = position
        self.rank = 0
        self.bag_of_words = bag_of_words
        self.stemmed_bag_of_words = stemmed_bag_of_words
        self.ending_char = ending_char

    @property
    def rank(self):
        return self.__rank if self.__rank else 0
    
    @rank.setter
    def rank(self, val):
        self.__rank = val

class Title:
    def __init__(self, original, bag_of_words):
        self.original = original
        self.bag_of_words = bag_of_words