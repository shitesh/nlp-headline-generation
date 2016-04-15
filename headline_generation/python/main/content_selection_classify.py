import codecs
import pickle
import sys
from feature_functions.features import get_feature_dict
from content_selection_train import get_start_end_indices
from feature_functions.tfidf_training import tokenise

classifier = None
tfidf = None


def initialise():
    global classifier, tfidf
    file = open('model/content_selection.pickle')
    classifier = pickle.load(file)
    file.close()

    file = open('model/tfidf.pickle')
    tfidf = pickle.load(file)
    file.close()


def get_tfidf_score(word):
    global tfidf
    response = tfidf.transform([word])
    feature_names = tfidf.get_feature_names()
    for col in response.nonzero()[1]:
            return response[0, col]
    return 0


def process_sentence(sentence):
    global classifier
    words = sentence.split()

    headline_words = []
    for index in xrange(0, len(words)):
        start_index, end_index = get_start_end_indices(index, len(words))
        feature_dict = get_feature_dict(words[start_index: end_index], index-start_index)
        feature_dict['tfidf'] = get_tfidf_score(words[index])
        output = classifier.prob_classify(feature_dict)
        if output.prob(1) >= output.prob(0) :
            headline_words.append((words[index], output.prob(1)))

    return headline_words

def classify(file_location):
    global classifier
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
            headline_words = process_sentence(sentence)
            if headline_words:
                all_potention_headline_words.extend(headline_words)

    return actual_headline, all_potention_headline_words

if __name__ == '__main__':
    initialise()
    classify(sys.argv[1])
