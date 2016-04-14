import codecs
import os
import sys
from feature_functions.features import get_feature_dict, get_outcome
from nltk import MaxentClassifier

feature_set = []
classifier = None

def process_sentence(sentence, headline):
    global feature_set
    words = sentence.split()
    for index in xrange(0, len(words)):
        start_index, end_index = index

        # handle the corner cases of index
        if index - 2 > 0:
            start_index = index - 2
        elif index - 1 > 0:
            start_index = index - 1

        if index + 2 < len(words)-1:
            end_index = index+3
        elif index+1 < len(words)-1:
            end_index = index+2

        outcome = get_outcome(words[index], headline)
        feature_dict = get_feature_dict(words[start_index: end_index])
        feature_set.append(feature_dict, outcome)


def process_input_directory(directory):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        file = codecs.open(file_path, 'r')
        line = file.readline() # <headline>
        headline = file.readline()

        for line in file:
            line = line.strip()
            if line in ['</headline>','<text>']:
                continue
            if line in ['</text>']:
                break
            sentences = line.split('\x01')
            for sentence in sentences:
                process_sentence(sentence, headline)

def train_model():
    global classifier
    classifier = MaxentClassifier.train(feature_set)



if __name__=='__main__':
    process_input_directory(sys.argv[1])

