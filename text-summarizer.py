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
import fuzzy as fz
import rules as rl

CUE_PHRASE_FILE = 'bonus_words'
STIGMA_WORDS_FILE = 'stigma_words'

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
                words[token] = tc.Word(stemmer.stem(token), word_pos, [lemma for synset in wn.synsets(token) for lemma in synset.lemma_names()])
        title.bag_of_words.append(token)

    #Pre-process text
    for detected_sentence in detected_sentences:
        sentences.append(tc.Sentence(detected_sentence, len(sentences) + 1, [], None))
        tokens = nltk.word_tokenize(sentences[-1].original)
        tokens = [token for token in tokens if token not in stopwords_list]
        part_of_speech = nltk.pos_tag(tokens)
        for (token, word_pos) in zip(tokens, part_of_speech):
            token = token.lower()
            if (token not in list(string.punctuation) and (token not in stopwords_list)):
                if (token not in words):
                    words[token] = tc.Word(stemmer.stem(token), word_pos, [lemma for synset in wn.synsets(token) for lemma in synset.lemma_names()])
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

def resource_loader():
    resources = dict()
    path = './resources'
    resource_files = [file.split()[0] for file in os.listdir(path)]
    for resource_file_name in resource_files:
        with open(path + "/"+resource_file_name, 'r') as f:
            text = f.read()
        f.closed
        resources[resource_file_name.split('.')[0]] = text.split('\n')
    return resources

def print_stuff(sentences, sentences_features):

    data = sentences_features

    for i in range(0, len(data)):
        print("******************************")

        print("Sentence: ", end="")        
        print(sentences[i].original)

        print_sentence_info(data[i])

        print("Rules: ")
        rl.print_rules_results(data[i])


def main():
    try:
        processed_input = process_input()
        text = processed_input['text']
        percentage = processed_input['percentage']
        resources = resource_loader()
        preprocessed_text = pre_process_text(text)
        keyword_feature_value = features.keyword_feature(preprocessed_text[1], preprocessed_text[2])
        title_word_feature_value = features.title_word_feature(preprocessed_text[0], preprocessed_text[1])
        sentence_location_feature_value = features.sentence_location_feature(preprocessed_text[1])
        sentence_length_feature_value = features.sentence_length_feature(preprocessed_text[1])
        proper_noun_feature_value = features.pos_tag_feature(preprocessed_text[1], preprocessed_text[2], 'NNP')
        cue_phrase_feature_value = features.phrase_feature(preprocessed_text[1], resources[CUE_PHRASE_FILE])
        stigma_phrase_feature_value = features.phrase_feature(preprocessed_text[1], resources[STIGMA_WORDS_FILE])
        numerical_data_feature_value = features.pos_tag_feature(preprocessed_text[1], preprocessed_text[2], 'CD')
        # similarities = cluster.calculate_cosine_similarity(preprocessed_text[1], preprocessed_text[2])
        # k_means_result = cluster.k_means(preprocessed_text[1], preprocessed_text[2], percentage)
        # summary = cluster.cluster_based_summary(preprocessed_text[1], k_means_result[0], k_means_result[1])

        sentences_feature_list = []
        for (
    keyword_value,
    title_word_value,
    sentence_location_value,
    sentence_lenght_value,
    proper_noun_value,
    cue_phase_value,
    stigma_word_value,
    numerical_data_value,
    ) in zip(
    keyword_feature_value,
    title_word_feature_value,
    sentence_location_feature_value,
    sentence_length_feature_value,
    proper_noun_feature_value,
    cue_phrase_feature_value,
    stigma_phrase_feature_value,
    numerical_data_feature_value,
    ):
            sentences_feature_list.append({
            'keyword': keyword_value,
            'title_word': title_word_value,
            'sentence_location': sentence_location_value,
            'sentence_length': sentence_lenght_value,
            'proper_noun': proper_noun_value,
            'cue_phrase': cue_phase_value,
            'nonessential': stigma_word_value,
            'numerical_data': numerical_data_value,
            })

        #fuzzied = fz.fuzzify_sentences(sentences_feature_list)
        #print_stuff(preprocessed_text[1], sentences_feature_list)
        fz.set_fuzzy_ranks(preprocessed_text[1], sentences_feature_list)
        # for obj in preprocessed_text[1]:
        #     print("***************************")
        #     print("Sentence: " + obj.original)
        #     print("Rank: " + str(obj.rank))

        #print(fuzzy_ranks)
        #fz.print_everything(preprocessed_text[1], sentences_feature_list)

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