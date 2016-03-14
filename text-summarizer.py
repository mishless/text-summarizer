import sys
import os
import collections
import nltk.data
import string
import math
import features
import traceback
import time
import argparse
import nltk.corpus
import nltk.stem.porter

import textClasses as tc 
import cluster
import fuzzy
import rules

CUE_PHRASE_FILE = 'bonus_words'
STIGMA_WORDS_FILE = 'stigma_words'

def pre_process_text(text):
    text = text.split('\n', 1)
    title = tc.Title(text[0], [])
    text = text[1].replace(u"\u2018", '\'').replace(u"\u2019", '\'').replace(u"\u201c",'"').replace(u"\u201d", '"')
    words = dict()
    sentences = []
    
    sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    detected_sentences = sentence_detector.tokenize(text.strip())
    stopwords_list = nltk.corpus.stopwords.words('english')
    stemmer = nltk.stem.porter.PorterStemmer()
    
    #Pre-process title
    tokens = nltk.word_tokenize(title.original)
    tokens = [token for token in tokens if token not in stopwords_list]
    part_of_speech = nltk.pos_tag(tokens)
    for (token, word_pos) in zip(tokens, part_of_speech):
        token = token.lower()
        if (token not in words) and (token not in list(string.punctuation) and (token not in stopwords_list)):
                words[token] = tc.Word(stemmer.stem(token), word_pos, [(lemma, stemmer.stem(lemma)) for synset in nltk.corpus.wordnet.synsets(token) for lemma in synset.lemma_names()])
        title.bag_of_words.append(token)

    #Pre-process text
    for detected_sentence in detected_sentences:
        
        tokens = nltk.word_tokenize(detected_sentence)
        tokens = [token for token in tokens if token not in stopwords_list]
        if tokens:
            sentences.append(tc.Sentence(detected_sentence, len(sentences) + 1, [], [], None))
            part_of_speech = nltk.pos_tag(tokens)
            for (token, word_pos) in zip(tokens, part_of_speech):
                token = token.lower()
                if (token not in list(string.punctuation) and (token not in stopwords_list)):
                    if (token not in words):
                        words[token] = tc.Word(stemmer.stem(token), word_pos, [(lemma, stemmer.stem(lemma)) for synset in nltk.corpus.wordnet.synsets(token) for lemma in synset.lemma_names()])
                    elif token in words:
                        words[token].increment_abs_frequency()
                    sentences[-1].bag_of_words.append(token)
                    sentences[-1].stemmed_bag_of_words.append(stemmer.stem(token))
    return [title, sentences, words]

def process_input(argv=None):
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--text-file", dest="text_file", help="the file containing the text tom be summarized", required=True)
    parser.add_argument("-p", "--percent", dest="percentage", help="the compression rate as percentage", required=True)
    parser.add_argument("-t", "--threads", dest="threads", help="the number of threads", required=True)
    
    # Process arguments
    args = parser.parse_args()

    threads = args.threads
    percentage = args.percentage
    text_file = args.text_file
    with open(text_file, 'r') as f:
        text = f.read()
    f.closed

    return {"text": text, "percentage": percentage, "threads": threads}

def resource_loader():
    resources = dict()
    path = './resources'
    resource_files = [file.split()[0] for file in os.listdir(path)]
    for resource_file_name in resource_files:
        with open(path + "/"+resource_file_name, 'r') as f:
            text = f.read()
        f.closed
        resources[resource_file_name.split('.')[0]] = set(list(text.split('\n')))
    return resources

def print_stuff(sentences, sentences_features):

    data = sentences_features

    for i in range(0, len(data)):
        print("******************************")

        print("Sentence: ", end="")        
        print(sentences[i].original)

        print_sentence_info(data[i])

        print("Rules: ")
        rules.print_rules_results(data[i])

def filter_using_clusters(sentences, percentage, clusters):
    number_sentences = math.floor(percentage * len(sentences))
    sentences = sorted(sentences, key=lambda x: x.rank, reverse=True)
    clusters_counter = [0] * len(clusters)
    sentence_counter = 0;
    chosen_sentences = []
    while len(chosen_sentences) < number_sentences:
        sentence_counter = 0
        for i in range(0, len(clusters)):
            for j in range(0, len(sentences)):
                if (clusters_counter[i] == min(clusters_counter) and clusters[i].count(sentences[j].position) == 1):
                    chosen_sentences.append(sentences[j])
                    clusters[i].remove(sentences[j].position)
                    if (len(clusters[i]) == 0):
                        clusters_counter[i] = sys.maxsize
                    else:
                        clusters_counter[i] += 1
                    break;
            if (len(chosen_sentences) >= number_sentences):
                break;
    chosen_sentences = sorted(chosen_sentences, key=lambda x: x.position)
    for sentence in chosen_sentences:
        print(sentence.original)
    return chosen_sentences

def print_based_on_fuzzy(angels_objects, p):
    print("***** RESULTS BASED ONLY ON FUZZY *****")
    number_sentences = math.floor(p * len(angels_objects))
    sorted_by_rank = [element for element in sorted(angels_objects, 
        key=lambda x: x.rank, reverse=True)][0:number_sentences]
    vukans_list = sorted(sorted_by_rank, key=lambda x: x.position, reverse=False)
    for sentence in vukans_list:
        print(sentence.original)
        print("")

def main():
    try:
        start_time = time.time()

        processed_input = process_input()
        text = processed_input['text']
        percentage = processed_input['percentage']
        threads = int(processed_input['threads'])
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
        k_means_result = cluster.k_means(preprocessed_text[1], preprocessed_text[2], percentage, threads)
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
        fuzzy.print_everything(preprocessed_text[1], sentences_feature_list)
        #fuzzied = fuzzy.fuzzify_sentences(sentences_feature_list)
        #print_stuff(preprocessed_text[1], sentences_feature_list)
        fuzzy.set_fuzzy_ranks(preprocessed_text[1], sentences_feature_list)
        filter_using_clusters(preprocessed_text[1], float(percentage)/100, k_means_result[1])
        # for obj in preprocessed_text[1]:
        #     print("***************************")
        #     print("Sentence: " + obj.original)
        #     print("Rank: " + str(obj.rank))
        #fuzzy_ranks = fuzzy.get_fuzzy_ranks(sentences_feature_list)
        #print(fuzzy_ranks)
        #fuzzy.print_everything(preprocessed_text[1], sentences_feature_list)
        print_based_on_fuzzy(preprocessed_text[1], float(percentage)/100)
        print("Total time: {} seconds.".format(time.time()- start_time))
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