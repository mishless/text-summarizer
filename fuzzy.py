# Fuzzy stuff for text summarizer
# Authors: Us
# Copyright: Ask Mihaela

import rules as rl
import numpy

mem_funcs = {}

mem_funcs['keyword'] =           {'VL':
                                    {'start' :  -1, 'peak' :   0, 'end' :0.25},
                                  'L':
                                    {'start' :   0, 'peak' :0.25, 'end' :0.50},
                                  'M':
                                    {'start' :0.25, 'peak' :0.50, 'end' :0.75},
                                  'H':
                                    {'start' :0.50, 'peak' :0.75, 'end' :1.00},
                                  'VH':
                                    {'start' :0.75, 'peak' :1.00, 'end' :2.00}}

mem_funcs['title_word'] =        {'L':
                                    {'start' :  -1, 'peak' :   0, 'end' :0.25},
                                  'M':
                                    {'start' :   0, 'peak' :0.25, 'end' :1.00},
                                  'H':
                                    {'start' :0.25, 'peak' :1.00, 'end' :2.00}}

mem_funcs['sentence_location'] = {'L':
                                    {'start' :  -1, 'peak' :   0, 'end' :   1},
                                  'H':
                                    {'start' :   0, 'peak' :   1, 'end' :   2}} 

mem_funcs['sentence_length'] =   {'VL':
                                    {'start' :  -1, 'peak' :   0, 'end' :0.25},
                                  'L':
                                    {'start' :   0, 'peak' :0.25, 'end' :0.50},
                                  'M':
                                    {'start' :0.25, 'peak' :0.50, 'end' :0.75},
                                  'H':
                                    {'start' :0.50, 'peak' :0.75, 'end' :1.00},
                                  'VH':
                                    {'start' :0.75, 'peak' :1.00, 'end' :2.00}}

mem_funcs['proper_noun'] =       {'L':
                                    {'start' :  -1, 'peak' :   0, 'end' :0.50},
                                  'M':
                                    {'start' :   0, 'peak' :0.50, 'end' :1.00},
                                  'H':
                                    {'start' :0.50, 'peak' :1.00, 'end' :2.00}}

mem_funcs['cue_phrase'] =        {'L':
                                    {'start' :  -1, 'peak' :   0, 'end' :0.10},
                                  'M':
                                    {'start' :   0, 'peak' :0.10, 'end' :1.00},
                                  'H':
                                    {'start' :0.10, 'peak' :1.00, 'end' :2.00}}

mem_funcs['nonessential'] =      {'L':
                                    {'start' :  -1, 'peak' :   0, 'end' :0.05},
                                  'M':
                                    {'start' :   0, 'peak' :0.05, 'end' :1.00},
                                  'H':
                                    {'start' :0.05, 'peak' :1.00, 'end' :2.00}}

mem_funcs['numerical_data'] =    {'L':
                                    {'start' :  -1, 'peak' :   0, 'end' :0.50},
                                  'M':
                                    {'start' :   0, 'peak' :0.50, 'end' :1.00},
                                  'H':
                                    {'start' :0.50, 'peak' :1.00, 'end' :2.00}}

output_funcs =                   {'L':
                                    {'start' :-0.5, 'peak' :   0, 'end' :0.50},
                                  'M':
                                    {'start' :   0, 'peak' :0.50, 'end' :1.00},
                                  'I':
                                    {'start' :0.50, 'peak' :1.00, 'end' :1.50}}

def get_line(zero, peak):
    k = 1/(peak-zero)
    n = -k * zero

    return {'k': k, 'n' : n}

def fuzzify_feature(val, feature):
    ret_val = {}

    for key in mem_funcs[feature]:
        func = mem_funcs[feature][key]
        if val < func['start'] or val > func['end']:
            res = 0

        else:
            if val < func['peak']:
                line = get_line(func['start'], func['peak'])
            else:
                line = get_line(func['end'], func['peak'])

            res = line['k'] * val + line['n'];

        ret_val[key] = res

    return ret_val

def fuzzify_sentence(s):
    ret_val = {}

    for feature in s:
        ret_val[feature] = fuzzify_feature(s[feature], feature)    

    return ret_val


def fuzzify_sentences(sentences):
    fuzzified = []

    for sentence in sentences:
        fuzzified.append(fuzzify_sentence(sentence))       

    return fuzzified


def print_line(line):
    print("(k, n) = (" + str(line['k']) + ", " + str(line['n']) + ")")

def print_info(info):
    for sentence in info:
        print("*******************");
        for feature in sentence:
            print(feature + ": " + str(sentence[feature]));

def get_max_rules(sentence):
    max_rules = {'I' : 0, 'M' : 0, 'L' : 0}
    
    fuzzified_sentence = fuzzify_sentence(sentence)
    rule_results = rl.calculate_all_rules(fuzzified_sentence)


    for rule_key in rule_results:
        if max_rules[rule_key[0]] < rule_results[rule_key]:            
            max_rules[rule_key[0]] = rule_results[rule_key]  

    return max_rules

def get_output_function_val(key, x):

    ofun = output_funcs[key]

    if x < ofun['start'] or x > ofun['end']:
        return 0

    else:
        if x < ofun['peak']:
            line = get_line(ofun['start'], ofun['peak'])
        else:
            line = get_line(ofun['end'], ofun['peak'])

        return line['k'] * x + line['n'];        

def get_output_val(x, key, maximum):
    return min(maximum, get_output_function_val(key,x))

def get_aggregated_value(x, max_rules):

    output_vals = []
    for key in max_rules:
        output_vals.append(get_output_val(x, key, max_rules[key]))

    return max(output_vals)

def center_of_gravity(max_rules):
    dx = 0.01
    x_vals = []
    y_vals = []

    integration_start = -0.3
    integration_end = 1.3

    x_vals = list(numpy.arange(integration_start, integration_end, dx))

    for x in x_vals:
        y_vals.append(get_aggregated_value(x, max_rules))

    summ = 0
    for i in range(0, len(y_vals)):
        summ += y_vals[i] * x_vals[i]

    return summ/sum(y_vals) 

def get_fuzzy_rank(sentence):

    max_rules = get_max_rules(sentence)

    return center_of_gravity(max_rules)


def print_everything(almost_originals, sentences):

    
    rank_results = get_fuzzy_ranks(sentences)
    something = zip(almost_originals, rank_results)
    rank_sort_results = sorted(something, key= lambda x: x[1][1], reverse=True)

    for ranked_element in rank_sort_results:
        sentence = ranked_element[1][0]

        print("******************************")
        print(ranked_element[0].original)

        print("\nFeatures:")

        fuzzified = fuzzify_sentence(sentence)
        for key in fuzzified:
            print("\t" + "%20s" % key + ": ", end = "")
            for key2 in fuzzified[key]:
                print(" %2s: " % key2 + "%.2f" % fuzzified[key][key2], end = "")
            print("")

        print("\nRules:")

        rl.print_rules_results(fuzzify_sentence(sentence))

        print("\nFinal value: " + "%.3f" % ranked_element[1][1])
        print("Rank: (%d / %d)" % (1 + rank_sort_results.index(ranked_element),
              len(rank_sort_results)))
        print("")
        
def set_fuzzy_ranks(sentence_object, sentences):

    for (sen_obj,sentence) in zip(sentence_object, sentences):
        sen_obj.rank = get_fuzzy_rank(sentence)

def get_fuzzy_ranks(sentences):

    ret_val = []
    for sentence in sentences:
        ret_val.append((sentence, get_fuzzy_rank(sentence)))

    return ret_val

# MAIN:
# test_stuff()

# sentence1 = {'keyword' : 0.1, 'title_word' : 0.2,
#              'sentence_location': 0.3, 'sentence_length' : 0.4,
#              'proper_noun' : 0.5, 'cue_phrase' : 0.6,
#              'nonessential' : 0.7, 'numerical_data' : 0.8}

# sentence2 = {'keyword' : 0.8, 'title_word' : 0.7,
#              'sentence_location': 0.6, 'sentence_length' : 0.5,
#              'proper_noun' : 0.4, 'cue_phrase' : 0.3,
#              'nonessential' : 0.2, 'numerical_data' : 0.1}

# sentences = [sentence1, sentence2]
# output = fuzzify_sentences(sentences)
# print_info(output)