import math
import textClasses


def title_word_feature(title, processed_text):
    """ List of values from 0 to 1 rating the number title words that appear in the sentence"""

    title_word_feature_values = []

    # Calculate the number of common words with the title that the sentence has

    word_intersection = [set(filter(lambda title_word: title_word \
                         in title.bag_of_words, sublist))
                         for sublist in [sentence.bag_of_words
                         for sentence in processed_text]]
    for word_list in word_intersection:
        title_word_feature_values.append(len(word_list)
                / len(title.bag_of_words))
    return title_word_feature_values


def sentence_length_feature(sentences):
    """ List of values from 0 to 1 rating the length of the sentence in comparation with the longest one """

    sentence_length_feature_values = []
    max_length_sentence = len(sentences[0].original.split(' '))

    # Find the longest sentence

    for sentence in sentences[1:]:
        if len(sentence.original.split(' ')) > max_length_sentence:
            max_length_sentence = len(sentence.original.split(' '))

    # Normalize the lenght of every sentence

    for sentence in sentences:
        sentence_length_feature_values.append(len(sentence.original.split(' '
                )) / max_length_sentence)
    return sentence_length_feature_values


def sentence_location_feature(sentences):
    """ List of values from 0 to 1 rating the position of the sentence"""

    sentence_location_feature_values = []
    for sentence in sentences:
        sentence_location_feature_values.append(1 / sentence.position)
    return sentence_location_feature_values


def keyword_feature(sentences, words):
    """ List of values from 0 to 1 rating the term frequency normalized by the invert frequency of the sentences """

    keyword_feature_values = []
    total_number_of_sentences = len(sentences)

    # Calculate number of sentence where every word is

    for word in words:
        number_of_sentences = 0
        for sentence in sentences:
            if word in sentence.bag_of_words:
                number_of_sentences += 1
        number_of_sentences = (1 if number_of_sentences
                               == 0 else number_of_sentences)

        # asign term weight based on tf/isf

        words[word].term_weight = words[word].abs_frequency \
            * math.log10(total_number_of_sentences
                         / number_of_sentences)

    # Calculate the total term weight for every sentence

    for sentence in sentences:
        sum_of_term_weights = 0
        for word in sentence.bag_of_words:
            sum_of_term_weights += words[word].term_weight
        keyword_feature_values.append(sum_of_term_weights)
    return [x / max(keyword_feature_values) for x in
            keyword_feature_values]


def pos_tag_feature(sentences, words, pos_tag):
    """ List of values from 0 to 1 rating the number of words with a certain part of speech tag that appear in the sentence"""

    pos_tag_words_count_list = []

    # Create a list with the number of words with the input pos_tag appear in the phrase

    for sentence in sentences:
        pos_tag_words_count_list.append(len([word for word in
                sentence.bag_of_words if words[word].part_of_speech[1]
                == pos_tag]))

    # Return a list of values normalize by the sentence with the maximum number of pos_tag words
        
    return ([pos_tag_words_sentence / max(pos_tag_words_count_list)
            for pos_tag_words_sentence in
            pos_tag_words_count_list] if max(pos_tag_words_count_list)
            != 0 else [0] * len(pos_tag_words_count_list))


def phrase_feature(sentences, phrase_list):
    """ List of values from 0 to 1 rating the number of phrases that appear in the sentence from a list """

    total_number_words = 0
    phrase_frequency = []

    # Calculate the number of words of the text
    # Number of phrase that appear in that sentence

    for sentence in sentences:
        count_phrase_per_sentence = 0
        for phrase in phrase_list:
            if phrase in sentence.original:
                count_phrase_per_sentence += 1
        phrase_frequency.append(count_phrase_per_sentence/len(sentence.bag_of_words))

    return phrase_frequency