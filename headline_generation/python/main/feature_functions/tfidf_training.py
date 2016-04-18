# -*- coding: utf-8 -*-
import nltk
import os
import pickle
import sys
import codecs
from sklearn.feature_extraction.text import TfidfVectorizer

TFIDF_LOCATION = '../model/tfidf.pickle'


def process_input_directory(input_directory):
    all_text = []
    dict_replacement = {'<Headline>': '', '</Headline>': '', '<text>': '', '</text>': '', ',': '', '.': '', u'।': '',  '\n': ' ', '\x01': ' '}
    for file_name in os.listdir(input_directory):
        file_path = os.path.join(input_directory, file_name)
        file = codecs.open(file_path, 'r', encoding='utf-8')

        line = file.read()
        for key, value in dict_replacement.iteritems():
            line = line.replace(key, value)
        all_text.append(line)
    return all_text


def tokenise(text):
    """Tokenises the input text for calculating tfidf value.

    """
    words = nltk.word_tokenize(text)
    return_list = []
    for word in words:
        if not word:
            continue
        word = word.rsplit('/', 1)[0]
        return_list.append(word) # todo: add a stemmer here
    return return_list


def generate_tf_idf_values(all_text):
    """Generate the tfidf values and store it in file.

    """
    global TFIDF_LOCATION
    file = codecs.open('hindi_stopwords.txt', 'r', encoding='utf-8')
    stop_word_list = file.readlines()
    stop_word_list = [word.strip() for word in stop_word_list]

    tfidf = TfidfVectorizer(tokenizer=tokenise, stop_words=stop_word_list, smooth_idf=True, encoding='utf-8')
    response = tfidf.fit_transform(all_text)
    feature_names = tfidf.get_feature_names()
    out_file = codecs.open(TFIDF_LOCATION, 'w', encoding='utf-8')
    for col in response.nonzero()[1]:
        out_file.write('%s\x01%s\n' %( feature_names[col], response[0, col]))
    out_file.close()

if __name__ == '__main__':
    all_text = process_input_directory(sys.argv[1])
    print 'got all data'
    generate_tf_idf_values(all_text)
