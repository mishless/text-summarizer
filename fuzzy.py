# Fuzzy stuff for text summarizer
# Authors: Us
# Copyright: Ask Mihaela

mem_funcs = {}

mem_funcs['keyword'] =           [{'start' :  -1, 'peak' :   0, 'end' :0.25},
                                  {'start' :   0, 'peak' :0.25, 'end' :0.50},
                                  {'start' :0.25, 'peak' :0.50, 'end' :0.75},
                                  {'start' :0.50, 'peak' :0.75, 'end' :1.00},
                                  {'start' :0.75, 'peak' :1.00, 'end' :2.00}]

mem_funcs['title_word'] =        [{'start' :  -1, 'peak' :   0, 'end' :0.25},
                                  {'start' :   0, 'peak' :0.25, 'end' :1.00},
                                  {'start' :0.25, 'peak' :1.00, 'end' :2.00}]                        

mem_funcs['sentence_location'] = [{'start' :  -1, 'peak' :   0, 'end' :   1},
                                  {'start' :   0, 'peak' :   1, 'end' :   2}] 

mem_funcs['sentence_length'] =   [{'start' :  -1, 'peak' :   0, 'end' :0.25},
                                  {'start' :   0, 'peak' :0.25, 'end' :0.50},
                                  {'start' :0.25, 'peak' :0.50, 'end' :0.75},
                                  {'start' :0.50, 'peak' :0.75, 'end' :1.00},
                                  {'start' :0.75, 'peak' :1.00, 'end' :2.00}]

mem_funcs['proper_noun'] =       [{'start' :  -1, 'peak' :   0, 'end' :0.50},
                                  {'start' :   0, 'peak' :0.50, 'end' :1.00},
                                  {'start' :0.50, 'peak' :1.00, 'end' :2.00}]                        

mem_funcs['cue_phrase'] =        [{'start' :  -1, 'peak' :   0, 'end' :0.10},
                                  {'start' :   0, 'peak' :0.10, 'end' :1.00},
                                  {'start' :0.10, 'peak' :1.00, 'end' :2.00}]          

mem_funcs['nonessential'] =      [{'start' :  -1, 'peak' :   0, 'end' :0.10},
                                  {'start' :   0, 'peak' :0.10, 'end' :1.00},
                                  {'start' :0.10, 'peak' :1.00, 'end' :2.00}]                        

mem_funcs['numerical_data'] =    [{'start' :  -1, 'peak' :   0, 'end' :0.50},
                                  {'start' :   0, 'peak' :0.50, 'end' :1.00},
                                  {'start' :0.50, 'peak' :1.00, 'end' :2.00}] 

def get_line(zero, peak):
    k = 1/(peak-zero)
    n = -k * zero

    return {'k': k, 'n' : n}

def fuzzify_feature(val, feature):
    ret_val = []

    for func in mem_funcs[feature]:

        if val < func['start'] or val > func['end']:
            res = 0

        else:
            if val < func['peak']:
                line = get_line(func['start'], func['peak'])
            else:
                line = get_line(func['end'], func['peak'])

            res = line['k'] * val + line['n'];

        ret_val.append(res)

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

def test_stuff():

    return
    print("Expected (1, 0)")
    print_line(get_line(0, 1))
    print("Expected (1, -5)")
    print_line(get_line(5, 6))
    print("Expected (-1, 2)")
    print_line(get_line(2,1))
    exit()

def print_info(info):
    for sentence in info:
        print("*******************");
        for feature in sentence:
            print(feature + ": " + str(sentence[feature]));

#MAIN:
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