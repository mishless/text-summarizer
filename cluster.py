#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import random
import time
import threading

from nltk.stem.porter import *
from functools import reduce

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
def cosine_similarity_thread_run(number_of_thread, number_of_sentences, sentences, words, stemmer, results):
    similarities = {}
    start_sentence_position = number_of_thread * number_of_sentences
    end_sentence_position = (number_of_thread + 1) * number_of_sentences
    if end_sentence_position > len(sentences):
        end_sentence_position = len(sentences)
    #print("Number of thread: {} Start_position: {} End Position: {}".format(number_of_thread, 
    #                           start_sentence_position, end_sentence_position))
    for sentence_position in range(start_sentence_position, end_sentence_position):
        if sentences[sentence_position].position not in similarities:
            similarities[sentences[sentence_position].position] = {}
            for sentence in sentences:
                if sentence.position not in similarities[sentences[sentence_position].position]:
                    similarities[sentences[sentence_position].position][sentence.position] = None
                    if sentences[sentence_position].position != sentence.position:
                        # Union of the bag of words of the two sentences
                        bag_of_words = \
                            list(set(sentences[sentence_position].bag_of_words)
                                 | set(sentence.bag_of_words))
                        # Substitute each word with an array of it plus all its synonyms 
                        bag_of_words = \
                            [list(set([synonym[1] for synonym in words[word].synonym_list]
                             + [stemmer.stem(word)])) for word in bag_of_words]
                        # Calculate the vector for the first sentences by 
                        # counting occurances of every word plus its synonyms 
                        # from the bag of words in the sentence after stemming it
                        first_sentence_vector = [reduce(lambda x, y: x \
                                + y, [sentences[sentence_position].stemmed_bag_of_words.count(word)
                                for word in synonyms]) for synonyms in
                                bag_of_words]
                        # Calculate the vector for the second sentences by
                        # counting occurances of every word plus its synonyms
                        # from the bag of words in the sentence after stemming it
                        second_sentence_vector = [reduce(lambda x, y: x \
                                + y, [sentence.stemmed_bag_of_words.count(word)
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
                        similarities[sentences[sentence_position].position][sentence.position] = \
                            reduce(lambda x, y: x + y, [first * second
                                   for (first, second) in
                                   zip(first_sentence_vector,
                                   second_sentence_vector)]) \
                            / denominator
    results[number_of_thread] = similarities

def calculate_cosine_similarity(sentences, words, number_of_threads):
    stemmer = PorterStemmer()
    similarities = {}
    # Create the specified number of threads, run them and join result
    threads = []
    results = [None] * number_of_threads
    number_of_sentences = math.ceil(len(sentences)/number_of_threads)
    for number_of_thread in range(0, number_of_threads):
        threads.append(threading.Thread(name='Thread#{}'.format(number_of_thread),
        target=cosine_similarity_thread_run,args=(number_of_thread,
                                                  number_of_sentences,
                                                  sentences,
                                                  words,
                                                  stemmer,
                                                  results)))
    for number_of_thread in range(0, number_of_threads):
        threads[number_of_thread].start()
    for number_of_thread in range(0, number_of_threads):
        threads[number_of_thread].join()
    for number_of_thread in range(0, number_of_threads):
        similarities.update(results[number_of_thread])
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

def k_means(sentences, words, percentage, number_of_threads):
    similarities = calculate_cosine_similarity(sentences, words, number_of_threads)
    number_of_clusters = \
        calculate_number_of_clusters_based_on_ratio(sentences,
            percentage)
    sentence_positions = list(range(1, len(sentences) + 1))
    centers = random.sample(sentence_positions, int(number_of_clusters))
    old_centers = []
    while set(centers) != set(old_centers):
        old_center = centers

        # Put every sentence in the correct cluster
        start_time = time.time()
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