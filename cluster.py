#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import random

from nltk.stem.porter import *
from functools import reduce

def calculate_similarities(sentences, words):
    similarities = dict()
    max_words_in_common = 1
    max_synonyms_in_common = 1
    for first_sentence in sentences:
        if first_sentence.position not in similarities:
            similarities[first_sentence.position] = dict()
            for second_sentence in sentences:
                if second_sentence.position \
                    not in similarities[first_sentence.position]:
                    similarities[first_sentence.position][second_sentence.position] = \
                        None
                    if first_sentence.position \
                        != second_sentence.position:
                        words_in_common = 0
                        synonyms_in_common = 0
                        for word in first_sentence.bag_of_words:
                            for second_word in \
                                second_sentence.bag_of_words:
                                if words[word].stem \
                                    == words[second_word].stem:
                                    words_in_common += 1
                                if word != second_word:
                                    if word \
    in words[second_word].synonym_list:
                                        synonyms_in_common += 1
                                    if second_word \
    in words[word].synonym_list:
                                        synonyms_in_common += 1
                        similarities[first_sentence.position][second_sentence.position] = \
                            [words_in_common, synonyms_in_common]
                        if words_in_common > max_words_in_common:
                            max_words_in_common = words_in_common
                        if synonyms_in_common > max_synonyms_in_common:
                            max_synonyms_in_common = synonyms_in_common
    for first_sentence in sentences:
        for second_sentence in sentences:
            if first_sentence.position != second_sentence.position:
                similarities[first_sentence.position][second_sentence.position] = \
                    similarities[first_sentence.position][second_sentence.position][0] \
                    / max_words_in_common \
                    + similarities[first_sentence.position][second_sentence.position][1] \
                    / max_synonyms_in_common
    return similarities

'''
Method to calculate the cosine similarity between all pairs of sentences 
in the documents. 
It calculates the cosine of the angle that is between the two vectors. 
The two vectors are constructed as follows: 
1. A list-union of words is created containing the words from both sentneces 
without repetitions.
2. Every word of the list is substituted by an array of the word plus all of 
its synonyms.
3. Every sentence is then represented as a vector with the same number of 
components as the length of the union of words from 1.
4. Every component is equal to the number of times the current word 
occurs in the sentence (or its synonym). 
5. After that the popular formuila for cosine is used:
cos(a, b) = sum(a*b)/sqrt(sum(a^2))*sqrt(sum(b^2))
6. Similarities are saved in a 2d array
''' 
def calculate_cosine_similarity(sentences, words):
    stemmer = PorterStemmer()
    similarities = {}
    # For every pair of sentences initialize the similarity to None
    for first_sentence in sentences:
        if first_sentence.position not in similarities:
            similarities[first_sentence.position] = {}
            for second_sentence in sentences:
                if second_sentence.position \
                    not in similarities[first_sentence.position]:
                    similarities[first_sentence.position][second_sentence.position] = None
                    if first_sentence.position \
                        != second_sentence.position:
                        # Union of the bag of words of the two sentences
                        bag_of_words = \
                            list(set(first_sentence.bag_of_words)
                                 | set(second_sentence.bag_of_words))
                        # Substitute each word with an array of it plus all its synonyms 
                        bag_of_words = \
                            [list(set(words[word].synonym_list
                             + [word])) for word in bag_of_words]
                        # Calculate the vector for the first sentences by 
                        # counting occurances of every word plus its synonyms 
                        # from the bag of words in the sentence after stemming it
                        first_sentence_vector = [reduce(lambda x, y: x \
                                + y, [[stemmer.stem(sentence_word)
                                for sentence_word in
                                first_sentence.bag_of_words].count(stemmer.stem(word))
                                for word in synonyms]) for synonyms in
                                bag_of_words]
                        # Calculate the vector for the second sentences by
                        # counting occurances of every word plus its synonyms
                        # from the bag of words in the sentence after stemming it
                        second_sentence_vector = [reduce(lambda x, y: x \
                                + y, [[stemmer.stem(sentence_word)
                                for sentence_word in
                                second_sentence.bag_of_words].count(stemmer.stem(word))
                                for word in synonyms]) for synonyms in
                                bag_of_words]
                        # Calculate denominator according to the formula
                        denominator = math.sqrt(reduce(lambda x, y: x \
                                + y, map(lambda x: x * x,
                                first_sentence_vector))) \
                            * math.sqrt(reduce(lambda x, y: x + y,
                                map(lambda x: x * x,
                                second_sentence_vector)))
                        # Calculate similarity between the two sentneces
                        similarities[first_sentence.position][second_sentence.position] = \
                            reduce(lambda x, y: x + y, [first * second
                                   for (first, second) in
                                   zip(first_sentence_vector,
                                   second_sentence_vector)]) \
                            / denominator
    return similarities

def calculate_number_of_clusters(sentences, words):
    accumulates_len_of_sentences = reduce(lambda x, y: x + y,
            [len(sentence.bag_of_words) for sentence in sentences])
    return len(words) / accumulates_len_of_sentences

def calculate_number_of_clusters_based_on_ratio(sentences, percentage):
    return int(percentage) * 0.01 * len(sentences)

'''
Implementation of K-means algorithm using Lloyd's iterative approach:
1. Randomly assign center sentences to the specified numnber of clusters
2. Assign every sentence to a cluster based on the similarity measure
3. Re-calculate thenew center of the clusters based on the accumulated
similarity - the sentnence with the lowest accumulated similarity gets to be the center
4. Repeat 2 and 3 until there is no change between two consecutive iterations
'''

def k_means(sentences, words, percentage):
    similarities = calculate_cosine_similarity(sentences, words)
    number_of_clusters = \
        calculate_number_of_clusters_based_on_ratio(sentences,
            percentage)
    sentence_positions = list(range(1, len(sentences) + 1))
    centers = random.sample(sentence_positions, int(number_of_clusters))
    old_centers = []
    while set(centers) != set(old_centers):
        old_center = centers

        # Put every sentence in the correct cluster

        clusters = {}
        for sentence in sentences:
            best_cluster_center = max([(center[0],
                    similarities[sentence.position][center[0] + 1])
                    for center in enumerate(centers) if center[0] + 1
                    != sentence.position], key=lambda x: x[1])[0]
            if best_cluster_center in clusters:
                clusters[best_cluster_center].append(sentence.position)
            elif best_cluster_center not in clusters:
                clusters[best_cluster_center] = [sentence.position]

        # Re-evaluate the new centers of the clusters

        accumulative_similarities = {}
        old_centers = centers
        centers = []
        keys = sorted(clusters.keys())
        for cluster_index in keys:
            accumulative_similarities[cluster_index] = {}
            for first_sentence in clusters[cluster_index]:
                accumulative_similarities[cluster_index][first_sentence] = \
                    0
                for second_sentence in clusters[cluster_index]:
                    if first_sentence != second_sentence:
                        accumulative_similarities[cluster_index][first_sentence] += \
                            similarities[first_sentence][second_sentence]
            centers.append(max([(sentence_positon,
                           accumulative_similarities[cluster_index][sentence_positon])
                           for sentence_positon in
                           clusters[cluster_index]], key=lambda x: \
                           x[1])[0])
    return [centers, clusters]

def cluster_based_summary(sentences, centers, clusters):
    output = []
    output.extend([sentence for sentence in sentences if sentence.position in centers])
    output.sort(key=lambda sentence: sentence.position)
    return output