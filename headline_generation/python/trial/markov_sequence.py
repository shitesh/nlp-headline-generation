import copy
import codecs
import json
import operator
import random

dict_bigram_third = {}


def initialise():
    global dict_bigram_third
    file = codecs.open('../main/model/pos_trigrams.txt', 'r', encoding='utf-8')
    line = file.readline()
    dict_temp = json.loads(line)
    for key, value in dict_temp.iteritems():
        key_tuple = tuple(key.split('\x01'))
        dict_bigram_third[key_tuple] = value


def generate_sequence(word_dict):
    global dict_bigram_third

    dict_tag_word = {}
    for wordtag, probability in word_dict.iteritems():
        word, tag = wordtag.rsplit('/', 1)
        if tag not in dict_tag_word:
            dict_tag_word[tag] = {}
        dict_tag_word[tag][word] = probability


    for tag, value in dict_tag_word.iteritems():
        value = sorted(value.items(), key=operator.itemgetter(1))
        value = [entry[0] for entry in value]
        dict_tag_word[tag] = value

    print dict_tag_word
    pos_tag_seq = []
    word_tag_seq = []
    # start the initialisation
    for tag, word_list in dict_tag_word.iteritems():
        pos_tag_seq.append(('start', tag))
        word_tag_seq.append([word_list[0]])

    print pos_tag_seq
    print word_tag_seq

    count = 0
    all_sentences = []
    while len(all_sentences) < 4:
        current_seq = pos_tag_seq.pop(0)
        current_word_seq = word_tag_seq.pop(0)
        print current_seq

        if current_seq in dict_bigram_third:
            value_list = dict_bigram_third[current_seq]
            for value in value_list:
                if value in dict_tag_word:
                    new_word_seq = copy.deepcopy(current_word_seq)
                    new_seq = (current_seq[1], value)

                    added = False
                    for word in dict_tag_word[value]:
                        if word not in current_word_seq:
                            print 'added', word
                            new_word_seq.append(word)
                            added = True

                    if added:
                        print 'new', new_seq
                        pos_tag_seq.append(new_seq)
                        word_tag_seq.append(new_word_seq)
                    else:
                        # no word present to be added
                        all_sentences.append(' '.join(current_word_seq))
                    break
            count += 1

    for word in word_tag_seq:
        print ' '.join(word)

    for sentence in all_sentences:
        print sentence


initialise()
file = codecs.open('/tmp/dict_word.txt', 'r', encoding='utf-8')
word_dict = json.loads(file.readline())
generate_sequence(word_dict)
