import random
import nltk

from nltk.corpus import names
from nltk import MaxentClassifier

nltk.config_megam('/home/shitesh/repos/nlp-headline-generation/headline_generation/python/main/MEGAM/megam-64.opt')

all_names = [(name, 'male') for name in names.words('male.txt')]
female_names = [(name, 'female') for name in names.words('female.txt')]

all_names.extend(female_names)
random.shuffle(all_names) # shuffle names

def gender_features(word):
    # returns a dictionary of feature sets
    word = word.lower()
    feature_dict = {'last_letter': word[-1]}
    feature_dict['first_letter'] = word[0]
    feature_dict['fw'] = word[:2]
    feature_dict['lw'] = word[-2:]

    return feature_dict


feature_sets = [(gender_features(name), gender) for (name, gender) in all_names]

train_set, test_set = feature_sets[100:], feature_sets[:100]

classifier = MaxentClassifier.train(train_set, "megam")

print classifier.classify(gender_features('Gary'))