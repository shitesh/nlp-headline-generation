import codecs
import pickle
import sys
from feature_functions.features import get_feature_dict
from content_selection_train import get_start_end_indices
from feature_functions.file_level_features import get_word_range
from feature_functions.tfidf_training import tokenise

import nltk
import os
import math

classifier = None
tfidf_dict = {}
stop_word_list = []

STOP_WORD_FILE_LOCATION = 'feature_functions/hindi_stopwords.txt'
nltk.config_megam('MEGAM/megam-64.opt')
TFIDF_LOCATION = 'model/tfidf.pickle'


def initialise():
    global classifier, tfidf_dict, stop_word_list
    file = open('model/content_selection.pickle')
    classifier = pickle.load(file)
    file.close()

    file = codecs.open(TFIDF_LOCATION, 'r', encoding='utf-8')
    for line in file:
        parts = line.strip().split('\x01')
        tfidf_dict[parts[0]] = float(parts[1])
    file.close()

    file = codecs.open(STOP_WORD_FILE_LOCATION, 'r', encoding='utf-8')
    lines = file.readlines()
    stop_word_list = [word.strip() for word in lines]
    file.close()


def get_tfidf_score(all_lines):
    global tfidf_dict

    word_dict = {}

    for line in all_lines:
        word_list = line.split()
        for word in word_list:
            word = word.rsplit('/', 1)[0]
            if word in tfidf_dict:
                word_dict[word] = tfidf_dict.get(word)

    all_values = word_dict.values()
    all_values.sort()

    length = len(all_values) - 1
    first_range_boundary = all_values[int(math.floor(0.9*length))]
    second_range_boundary = all_values[int(math.floor(0.1*length))]

    for key, value in word_dict.iteritems():
        if value >= first_range_boundary:
            word_dict[key] = '1_10'
        elif value >= second_range_boundary:
            word_dict[key] = '10_90'
        else:
            word_dict[key] = '90_100'

    return word_dict


def get_file_level_details(file_path):
    global file_level_dict
    file = codecs.open(file_path, 'r', encoding='utf-8')
    line = file.readline()
    while line.strip() != '<text>':
        line = file.readline()

    all_lines = []
    for line in file:
        parts = line.split('\x01')
        if parts:
            all_lines.extend(parts)

    file_level_dict = get_word_range(all_lines)
    word_dict = get_tfidf_score(all_lines)
    return file_level_dict, word_dict


def process_sentence(sentence, file_level_dict, word_dict):
    global classifier
    words = sentence.split()

    headline_words = []

    for index in xrange(0, len(words)):
        start_index, end_index = get_start_end_indices(index, len(words))
        feature_dict = get_feature_dict(words[start_index: end_index], index-start_index)

        word = words[index].rsplit('/', 1)[0]
        feature_dict['tfidf'] = word_dict.get(word, '90_100')

        feature_dict['lead_sentence'] = file_level_dict[word]['lead_sentence']
        feature_dict['first_occurance'] = file_level_dict[word]['first_occurance']
        feature_dict['range'] = ','.join(str(x) for x in file_level_dict[word]['range'])

        feature_dict['stop_word'] = 1 if word in stop_word_list else 0

        output = classifier.prob_classify(feature_dict)

        if output.prob(1) > 0.4:
            headline_words.append((words[index], output.prob(1)))

    return headline_words

def classify(file_location):
    global classifier
    file_level_dict, word_dict = get_file_level_details(file_location)

    file = codecs.open(file_location, 'r', encoding='utf-8')
    line = file.readline() # <headline>

    actual_headline = file.readline()

    all_potention_headline_words = []
    for line in file:
        line = line.strip()
        if line in ['</Headline>','<text>']:
            continue
        if line in ['</text>']:
            break
        sentences = line.split('\x01')
        for sentence in sentences:
            headline_words = process_sentence(sentence, file_level_dict, word_dict)
            if headline_words:
                all_potention_headline_words.extend(headline_words)

    return actual_headline, set(all_potention_headline_words)

if __name__ == '__main__':
    print 'starting'
    initialise()
    out_file = codecs.open(sys.argv[2], 'w', encoding='utf-8')
    for file_name in os.listdir(sys.argv[1]):
        file_path = os.path.join(sys.argv[1], file_name)
        x, y = classify(file_path)
        out_file.write('%s\n' % file_name)
        out_file.write('%s\n\n' % x)
        for i in y:
            out_file.write('%s,  %s\n' % (i[0], i[1]))
    out_file.close()
