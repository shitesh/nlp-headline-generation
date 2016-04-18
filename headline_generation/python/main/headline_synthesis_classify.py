"""This files contains functions for getting the result from headline synthesis model.

"""
import pickle
from feature_functions.BLEU_comparison import get_bleu_score
from feature_functions.headline_model_features import get_classification_dictionary
from feature_functions.generate_language_model_features import get_features

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

    headline_words = headline_seq.split()
    feature_list = get_features(headline_seq)

    # handle the case of start tag for trigram
    start_feature = feature_list.pop(0)
    start_feature['content_score'] = dict_content_score[headline_words[0]] + dict_content_score[headline_words[1]]
    start_feature['bleu_score'] = 0.0

    probability = headline_synthesis_classifier.classify(start_feature)
    if probability == 1.0:
        probability = 0

    for index in xrange(0, len(headline_words)-2):
        headline_seq = ' '.join(headline_words[index: index+3])
        bleu_score = get_bleu_score(headline_seq, file_text)

        content_score = 0
        for word in headline_words[index: index+3]:
            content_score += dict_content_score[word]

        feature_dict = feature_list.pop(0)
        feature_dict['content_score'] = content_score
        feature_dict['bleu_score'] = bleu_score
        temp = headline_synthesis_classifier.classify(feature_dict)
        if temp == 1.0:
            temp = 0
        probability += temp

    return probability






