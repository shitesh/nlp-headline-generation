import codecs
import sys
import os
import pickle
from content_selection_classify import *
from feature_functions.BLEU_comparison import get_bleu_score
from nltk import MaxentClassifier

headline_feature_set = []
headline_classifier = None

def get_bleu_score_probability(file_location):
    file = codecs.open(file_location, 'r', encoding='utf-8')
    line = file.readline() # <headline>
    actual_headline = file.readline()
    while line.strip() != '<text>':
        line = file.readline()
    all_lines = file.read()

    bleu_score = get_bleu_score(actual_headline, all_lines)
    return bleu_score


def process_directory(input_directory):
    all_headlines = []
    dict_content_score = {}
    dict_bleu = {}
    for file_name in os.listdir(input_directory):
        file_path = os.path.join(input_directory, file_name)
        headline, word_dict = classify_dev_file(file_path)

        content_score = {}
        for word in headline.replace('\x01', '').split():
            content_score += word_dict[word]

        if content_score in dict_content_score:
            dict_content_score[content_score] += 1
        else:
            dict_content_score[content_score] = 1

        # get bleu score
        bleu_score = get_bleu_score_probability(file_path)
        if bleu_score in dict_bleu:
            dict_bleu[bleu_score] += 1
        else:
            dict_bleu[bleu_score] = 1

        all_headlines.append((headline, word_dict))


    for score, count in dict_content_score.iteritems():
        output_dict = {'content_score':  score}
        outcome = float(count)/len(dict_content_score)

    for score, count in dict_bleu.iteritems():
        output_dict = {'content_score': score}
        outcome = float(count)/len(dict_content_score)


def train():
    global headline_classifier, headline_feature_set
    classifier = MaxentClassifier.train(headline_feature_set, "megam")


def save():
    global headline_classifier
    out_file = open('model/headline_synthesis.pickle', 'wb')
    pickle.dump(classifier, out_file)
    out_file.close()


if __name__ == '__main__':
    initialise()
    print 'processing directory'
    process_directory(sys.argv[1])
    print 'training'
    train()
    print 'saving'
    save()