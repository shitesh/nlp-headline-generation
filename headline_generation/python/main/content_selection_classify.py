import codecs
import pickle
import sys
import nltk
import os
import math
import operator
from feature_functions.features import get_feature_dict
from content_selection_train import get_start_end_indices
from feature_functions.file_level_features import get_word_range
from feature_functions.tfidf_training import tokenise


classifier = None
tfidf_dict = {}
stop_word_list = []

STOP_WORD_FILE_LOCATION = 'feature_functions/hindi_stopwords.txt'
# use megam to make the learning process faster
nltk.config_megam('MEGAM/megam-64.opt')
TFIDF_LOCATION = 'model/tfidf.pickle'


def initialise():
    """Initialises the globally declared variables.

    These variables are used throughout the file.
    """
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
    """For an entire file text, returns a dictionary mapping word to range of tf-idf values it belongs to.

    This information is used as a part of feature function.
    """
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


def get_file_level_details(file_path, headers_present=True):
    """Returns file level feature functions details.

    These are used as a part of the feature functions for querying the models.
    """
    global file_level_dict
    file = codecs.open(file_path, 'r', encoding='utf-8')
    if headers_present:
        line = file.readline()
        while line.strip() != '<text>':
            line = file.readline()

    all_lines = []
    for line in file:
        line = line.strip()
        if line == '</text>':
            break
        parts = line.split('\x01')
        if parts:
            parts = [part for part in parts if parts]
            all_lines.extend(parts)

    file_level_dict = get_word_range(all_lines)
    word_dict = get_tfidf_score(all_lines)
    return file_level_dict, word_dict


def process_sentence(sentence, file_level_dict, word_dict):
    """For the sentence passed, returns the words along with the probabilities of each word to be present in headline.

    Uses the content generation model trained before to get the probability.
    """
    global classifier
    words = sentence.split()

    headline_words = {}

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

        if output.prob(1) > 0.0:
            headline_words[words[index]] = max(output.prob(1), headline_words.get(words[index], 0))

    return headline_words


def classify_dev_file(file_location):
    """For given file path, returns a dictionary of all the words along with the probability value.

    This function is called by headline synthesis process during training and so return value consists of all the words.
    """
    global classifier
    file_level_dict, word_dict = get_file_level_details(file_location)
    file = codecs.open(file_location, 'r', encoding='utf-8')
    line = file.readline() # <headline>

    actual_headline = file.readline()

    all_potention_headline_words = {}
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
                for key, value in headline_words.iteritems():
                    all_potention_headline_words[key] = max(value, all_potention_headline_words.get(key, 0))

    return actual_headline.replace('\x01', ''), all_potention_headline_words


def classify_new_file(file_path):
    """This function is called by decoding algorithm.

    For given input file, it returns a dictionary of 20 words along with their associated probability which are most
    suitable to be included in the headline.
    """
    file_level_dict, word_dict = get_file_level_details(file_path, False)
    all_potention_headline_words = {}

    file = codecs.open(file_path, 'r', encoding='utf-8')
    for line in file:
        line = line.strip()
        sentences = line.split('\x01')
        for sentence in sentences:
            headline_words = process_sentence(sentence, file_level_dict, word_dict)
            if headline_words:
                for key, value in headline_words.iteritems():
                    all_potention_headline_words[key] = max(value, all_potention_headline_words.get(key, 0))

    dict_unique_words = {}
    sorted_headline_words = sorted(all_potention_headline_words.items(), key=operator.itemgetter(1), reverse=True)
    top_20_words= {}
    for entry in sorted_headline_words:
        word_with_tag, value = entry
        word = word_with_tag.rsplit('/', 1)[0]
        if word not in dict_unique_words:
            dict_unique_words[word] = 1
        top_20_words[word_with_tag] = value
        if len(dict_unique_words) > 20:
            break

    return top_20_words
