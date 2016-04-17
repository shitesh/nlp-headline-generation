"""This files contains functions for getting the result from headline synthesis model.

"""
import pickle
from feature_functions.BLEU_comparison import get_bleu_score
from feature_functions.headline_model_features import get_classification_dictionary

headline_synthesis_classifier = None


def headline_synthesis_initialise():
    """Loads the classifier object with the contents of stored model file.

    """
    global headline_synthesis_classifier

    file = open('model/headline_synthesis.pickle')
    headline_synthesis_classifier = pickle.load(file)
    file.close()


def get_headline_synthesis_score(headline_seq, dict_content_score, file_text):
    """For a headline sequence given the entire file text, returns the probability of that sequence to be the headline.

    Uses the trained headline synthesis model to find out the probability.
    """
    global headline_synthesis_classifier
    dict_features = {}
    content_score = 0
    headline_words = headline_seq.split()

    bleu_score = get_bleu_score(headline_seq, file_text)
    for word in headline_words:
        content_score += dict_content_score.get(word, 0)

    dict_features['content_score']= content_score

    if bleu_score:
        dict_features['bleu_score'] = bleu_score

    temp_dict = get_classification_dictionary(headline_seq)
    for key, value in temp_dict.iteritems():
        if key == 'headline_len':
            continue
        dict_features[key] = value

    probability = headline_synthesis_classifier.classify(dict_features)
    return probability






