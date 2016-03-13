
rules = {'I1': lambda data: min(max(data['keyword']['VH'], data['keyword']['H']), max(data['title_word']['H'], data['title_word']['M']), data['cue_phrase']['H'], data['nonessential']['L'], max(data['proper_noun']['H'], data['proper_noun']['M']), max(data['numerical_data']['H'], data['numerical_data']['M']), data['sentence_location']['H'], max(data['sentence_length']['L'], data['sentence_length']['M'], data['sentence_length']['H'], data['sentence_length']['VH'])),
         'L2': lambda data: min(max(data['nonessential']['H'],data['nonessential']['M']), data['sentence_location']['L']),
         'I2': lambda data: min(max(data['keyword']['VH'], data['keyword']['H'], data['keyword']['M'], data['keyword']['L']), max(data['cue_phrase']['H'], data['cue_phrase']['M'], data['proper_noun']['H'], data['numerical_data']['H']), max(data['sentence_length']['VL'], data['sentence_length']['L'], data['sentence_length']['M'], data['sentence_length']['H'])),
         'L3': lambda data: min(max(data['keyword']['VL'],data['keyword']['L']),data['proper_noun']['L'],data['numerical_data']['L'],data['sentence_location']['L']),
         'I3': lambda data: min(max(data['keyword']['M'], data['keyword']['H'], data['keyword']['VH']), data['sentence_location']['H']),
         'M1': lambda data: min(max(data['keyword']['L'],data['keyword']['M']),max(data['proper_noun']['M'],data['numerical_data']['M'])),
         'M2': lambda data: min(max(data['keyword']['L'],data['keyword']['M'],data['keyword']['H']),data['sentence_location']['L'],data['sentence_length']['VH'],data['numerical_data']['L'], data['proper_noun']['L']),
         'L1': lambda data: min(max(data['keyword']['VL'],data['keyword']['L']),data['proper_noun']['L'],data['numerical_data']['L'],max(data['sentence_length']['VL'],data['sentence_length']['VH'])),
         'L4': lambda data: min(max(data['keyword']['VL'], data['keyword']['L']), max(data['proper_noun']['L'], data['numerical_data']['L'], data['sentence_location']['L'])),
         'I4': lambda data: min(max(data['keyword']['VH'], data['keyword']['H']), max(data['sentence_length']['H'], data['sentence_length']['VH']), max(data['numerical_data']['M'], data['numerical_data']['H']), max(data['proper_noun']['M'], data['proper_noun']['H']))}


def calculate_all_rules(sentence):
    result = {}
    for rule_key in rules:
        result[rule_key] = calculate_rule(sentence, rules[rule_key])

    return result

def calculate_rule(sentence, rule):
    return rule(sentence)

def do_inference(sentences):
    for sentence in sentences:
        nista = 0

def print_rules_results(sentence):
    
    for key in rules:
        print("\t" + "%3s" % key + ": " + str(calculate_rule(sentence, rules[key])))
