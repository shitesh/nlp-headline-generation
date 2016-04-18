import codecs
import json
import nltk
import operator
import os
import sys


def increment_dict(dict_obj, key):
    """Increments the value associated with a key in a dictionary.

    """
    if key in dict_obj:
        dict_obj[key] += 1
    else:
        dict_obj[key] = 1


def generate_trigram_pos(all_headlines):
    """Generates and stores a POS trigram sequence for the passed text.

    """
    all_tag_sequence = []
    for headline in all_headlines:
        headline = 'start/start %s end/end' % headline
        words = headline.split()
        tags = [word.rsplit('/', 1)[1] for word in words]
        all_tag_sequence.append(tags)

    trigram_pos_list = []
    for tag_seq in all_tag_sequence:
        trigram_pos_list.extend(list(nltk.trigrams(tag_seq)))
    #print trigram_pos_list

    dict_bigram_third = {}
    for entry in trigram_pos_list:
        if (entry[0], entry[1]) not in dict_bigram_third:
            dict_bigram_third[(entry[0], entry[1])] = {}
        increment_dict(dict_bigram_third[(entry[0], entry[1])], entry[2])

    for key, value in dict_bigram_third.iteritems():
        value = sorted(value.items(), key=operator.itemgetter(1))
        value = [entry[0] for entry in value]
        dict_bigram_third[key] = value

    dict_write = {}
    for key, value in dict_bigram_third.iteritems():
        key_str = '\x01'.join(key)
        dict_write[key_str] = value

    file = codecs.open('../main/model/pos_trigrams.txt','w', encoding='utf-8')
    file.write(json.dumps(dict_write))
    file.close()

all_headlines = []
for file_name in os.listdir(sys.argv[1]):
    file = codecs.open(os.path.join(sys.argv[1], file_name), encoding='utf-8')
    line = file.readline()
    headline = file.readline()
    headline = headline.strip().replace('\x01', '')
    all_headlines.append(headline)
    file.close()

generate_trigram_pos(all_headlines)