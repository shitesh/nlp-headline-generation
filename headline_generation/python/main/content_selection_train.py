import codecs
import os
import pickle
import sys
from feature_functions.features import get_feature_dict, get_outcome
from feature_functions.tfidf_training import tokenise
from nltk import MaxentClassifier

feature_set = []
classifier = None
tfidf = None

def get_start_end_indices(index, length):
    start_index, end_index = index, index+1
    if index - 2 >= 0:
        start_index = index - 2
    elif index - 1 >= 0:
        start_index = index - 1

    if index + 2 <= length - 1:
        end_index = index+3
    elif index+1 <= length - 1:
        end_index = index+2

    return start_index, end_index


def initialise():
    global tfidf
    file = open('model/tfidf.pickle')
    tfidf = pickle.load(file)
    file.close()


def get_tfidf_score(word_list):
    global tfidf
    tfidf_dict = {}
    response = tfidf.transform(word_list)

    feature_names = tfidf.get_feature_names()
    for col in response.nonzero()[1]:
        tfidf_dict[feature_names[col]] = response[0, col]

    return tfidf_dict

def process_sentence(sentence, headline):
    global feature_set
    if not sentence:
        return
    words = sentence.split()
    original_words = [word.rsplit('/',1)[0] for word in words]
    tfidf_dict = get_tfidf_score(original_words)

    for index in xrange(0, len(words)):
        start_index, end_index = get_start_end_indices(index, len(words))
        outcome = get_outcome(words[index], headline)
        feature_dict = get_feature_dict(words[start_index: end_index], index-start_index)
        feature_dict['tfidf'] = tfidf_dict.get(words[index], 0)
        feature_set.append((feature_dict, outcome))


def process_input_directory(directory):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        file = codecs.open(file_path, 'r', encoding='utf-8')
        line = file.readline() # <Headline>
        headline = file.readline()

        for line in file:
            line = line.strip()
            if line in ['</Headline>', '<text>']:
                continue
            if line in ['</text>']:
                break
            sentences = line.split('\x01')
            for sentence in sentences:
                process_sentence(sentence, headline)


def train_model():
    global classifier, feature_set
    classifier = MaxentClassifier.train(feature_set)


def save_classifier():
    global classifier
    out_file = open('model/content_selection.pickle', 'wb')
    pickle.dump(classifier, out_file)
    out_file.close()


if __name__ == '__main__':
    initialise()
    process_input_directory(sys.argv[1])
    train_model()
    save_classifier()
