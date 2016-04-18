import nltk


def increment_key(dict_obj, key):
    if key in dict_obj:
        dict_obj[key] += 1
    else:
        dict_obj[key] = 1


def get_feature_values(all_sentences):

    all_tag_sequence = []
    all_word_sequence = []
    all_feature_list = []
    dict_word = {}

    for sentence in all_sentences:
        sentence = 'start/start %s' % sentence
        words = sentence.split()
        tag_list = []
        word_list = []
        for entry in words:
            word, tag = entry.rsplit('/', 1)
            tag_list.append(tag)
            if word not in ['start']:
                word_list.append(word)
                increment_key(dict_word, word)

        all_tag_sequence.append(tag_list)
        all_word_sequence.append(word_list)

    # all_tag_sequence now has a list of tags corresponding to different sentences

    bigram_pos_list = []
    trigram_pos_list = []
    for tag_seq in all_tag_sequence:
        bigram_pos_list.extend(list(nltk.bigrams(tag_seq)))
        trigram_pos_list.extend(list(nltk.trigrams(tag_seq)))

    dict_pos_bigram = {}
    dict_pos_trigram = {}

    for entry in bigram_pos_list:
        increment_key(dict_pos_bigram, entry)

    for entry in trigram_pos_list:
        increment_key(dict_pos_trigram, entry)

    for key, value in dict_pos_trigram.iteritems():
        prob_val = float(value)/dict_pos_bigram[(key[0], key[1])]
        key_str = '_'.join(key)
        dict_temp = {'pos_trigram': key_str}
        all_feature_list.append((dict_temp, prob_val))

    # calculate word bigrams now
    bigram_word_list = []
    for word_seq in all_word_sequence:
        bigram_word_list.extend(list(nltk.bigrams(word_seq)))

    dict_word_bigram = {}
    for entry in bigram_word_list:
        increment_key(dict_word_bigram, entry)

    #for key, value in dict_word_bigram.iteritems():
    #    prob_val = float(value)/dict_word[key[0]]
    #    key_str = '_'.join(key)
    #    dict_temp ={'word_bigram': key_str}
    #    all_feature_list.append((dict_temp, prob_val))

    return all_feature_list


def get_features(word_seq):
    word_seq = 'start/start %s'%(word_seq)
    words = word_seq.split()
    all_features = []
    tag_list = []
    word_list = []
    for entry in words:
        word, tag = entry.rsplit('/', 1)
        tag_list.append(tag)
        word_list.append(word)

    trigram_list = list(nltk.trigrams(tag_list))
    for entry in trigram_list:
        key_str = '_'.join(entry)
        dict_temp = {'pos_trigram': key_str}
        all_features.append(dict_temp)

    #bigram_list = list(nltk.bigrams(tag_list))
    #for entry in bigram_list:
    #    key_str = '_'.join(entry)
    #    dict_temp = {'word_bigram': key_str}
    #    all_features.append(dict_temp)


    return all_features
