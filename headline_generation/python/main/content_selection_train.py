import codecs
import os
import pickle
import nltk
import sys
import math
from feature_functions.features import get_feature_dict, get_outcome
from feature_functions.file_level_features import get_word_range
from feature_functions.tfidf_training import tokenise
from nltk import MaxentClassifier

feature_set = []
classifier = None
tfidf_dict = {}
stop_word_list = []

STOP_WORD_FILE_LOCATION = 'feature_functions/hindi_stopwords.txt'
TFIDF_LOCATION = 'model/tfidf.pickle'

nltk.config_megam('MEGAM/megam-64.opt')


def get_start_end_indices(index, length):
    """Returns the start and end indices given the current index.

    For any word, the model is dependent on previous two words, previous two POS tags, next two words and next two POS
     tags. This function helps in managing the corner cases near the beginning and end indices.
    """
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
    """Initialises the globally declared variables.

    These variables are used throughout the file.
    """
    global tfidf_dict, stop_word_list

    file = codecs.open(STOP_WORD_FILE_LOCATION, 'r', encoding='utf-8')
    lines = file.readlines()
    stop_word_list = [word.strip() for word in lines]
    file.close()

    file = codecs.open(TFIDF_LOCATION, 'r', encoding='utf-8')
    for line in file:
        parts = line.strip().split('\x01')
        tfidf_dict[parts[0]] = float(parts[1])


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


def get_file_level_details(file_path):
    """Returns file level feature functions details.

    These are used as a part of the feature functions for querying the models.
    """
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


def process_sentence(sentence, headline, file_level_dict, word_dict):
    """For the sentence passed, generates the feature sets for all the words present in the sentence.

    The generated feature set is used to train the model.
    """
    global feature_set, stop_word_list

    if not sentence:
        return
    words = sentence.split()

    for index in xrange(0, len(words)):
        start_index, end_index = get_start_end_indices(index, len(words))
        outcome = get_outcome(words[index], headline)
        feature_dict = get_feature_dict(words[start_index: end_index], index-start_index)

        # additional fields
        word = words[index].rsplit('/', 1)[0]
        feature_dict['tfidf'] = word_dict.get(word, '90_100')

        feature_dict['lead_sentence'] = file_level_dict[word]['lead_sentence']
        feature_dict['first_occurance'] = file_level_dict[word]['first_occurance']
        feature_dict['range'] = ','.join(str(x) for x in file_level_dict[word]['range'])

        feature_dict['stop_word'] = 1 if word in stop_word_list else 0
        # add this to set of all features
        feature_set.append((feature_dict, outcome))


def process_input_directory(directory):
    """Processes the entire directory passed as input to generate the feature values.

    """
    count = 0
    error = open('error.txt', 'w')
    for file_name in os.listdir(directory):
        count += 1
        print count, file_name
        try:
            file_path = os.path.join(directory, file_name)
            file_level_dict, word_dict = get_file_level_details(file_path)

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
                    process_sentence(sentence, headline, file_level_dict, word_dict)
        except:
            error.write('filename : %s\n' % file_name)
            import traceback
            error.write(traceback.format_exc())
            error.write('\n')
            continue
    error.close()


def train_model():
    """Trains the model using the feature set generated above.

    """
    global classifier, feature_set
    classifier = MaxentClassifier.train(feature_set, "megam")


def save_classifier():
    """Saves the model so that it can be used without re-running the training part again.

    """
    global classifier
    out_file = open('model/content_selection.pickle', 'wb')
    pickle.dump(classifier, out_file)
    out_file.close()


if __name__ == '__main__':
    initialise()
    process_input_directory(sys.argv[1])
    train_model()
    save_classifier()
