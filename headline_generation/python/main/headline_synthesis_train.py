import codecs
import sys
import nltk
import os
import pickle
from content_selection_classify import *
from feature_functions.BLEU_comparison import get_bleu_score
from feature_functions.headline_model_features import get_headline_synthesis_features
from nltk import MaxentClassifier

headline_feature_set = []
headline_classifier = None
nltk.config_megam('MEGAM/megam-64.opt')


def get_bleu_score_probability(file_location):
    """For the passed input file, returns the bleu score of the headline with reference to the text.

    """
    file = codecs.open(file_location, 'r', encoding='utf-8')
    line = file.readline() # <headline>
    actual_headline = file.readline()
    while line.strip() != '<text>':
        line = file.readline()
    all_lines = file.read()

    bleu_score = get_bleu_score(actual_headline, all_lines)
    return bleu_score


def process_directory(input_directory):
    """Processes the entire directory passed as input to generate the feature values.

    """
    global headline_feature_set
    all_headlines = []
    dict_content_score = {}
    dict_bleu = {}
    for file_name in os.listdir(input_directory):
        print file_name
        file_path = os.path.join(input_directory, file_name)
        headline, word_dict = classify_dev_file(file_path)

        content_score = 0
        for word in headline.replace('\x01', '').split():
            # todo: recheck this, what if word is present in headline but not in text?
            content_score += word_dict.get(word, 0)

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

        all_headlines.append(headline)

    headline_feature_set = get_headline_synthesis_features(all_headlines)

    for score, count in dict_content_score.iteritems():
        output_dict = {'content_score':  score}
        outcome = float(count)/len(dict_content_score)
        headline_feature_set.append((output_dict, outcome))

    for score, count in dict_bleu.iteritems():
        output_dict = {'content_score': score}
        outcome = float(count)/len(dict_content_score)
        headline_feature_set.append((output_dict, outcome))


def train():
    """Trains the model using the feature set generated above.

    """
    global headline_classifier, headline_feature_set
    headline_classifier = MaxentClassifier.train(headline_feature_set, "megam")


def save():
    """Saves the model so that it can be used without re-running the training part again.

    """
    global headline_classifier
    out_file = open('model/headline_synthesis.pickle', 'wb')
    pickle.dump(headline_classifier, out_file)
    out_file.close()


if __name__ == '__main__':
    initialise()
    process_directory(sys.argv[1])
    train()
    save()
