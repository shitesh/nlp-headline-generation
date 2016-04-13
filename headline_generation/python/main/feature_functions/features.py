# define all the feature functions here
"""List of features used:
1. Current Story Word
2. Word Bi-gram Context - both sides -1 and +1
3. POS of Current Story Word
4. POS Bi-gram of Current Word - both sides -1 and +1
5. POS Tri-gram of Current Word - both sides -1, -2 and +1, +2
6. Word Position in Lead sentence
7. Word Position
8. First Word Occurrence Position
9. Word TF-IDF Range

"""


def get_outcome(word, heading):
    """Returns if the word is present in heading or not.

    """
    return word in heading

def get_feature_dict(word_tag_list, index=2):
    """Returns the feature dictionary of POS tagged list of words(5 words are passed in the list).

    """
    dict_feature = {}
    word_list = []
    tag_list = []

    for entry in word_tag_list:
        word, tag = entry.rsplit('/', 1)
        word_list.append(word)
        tag_list.append(tag)

    dict_feature['1_w'] = word_list[index]
    dict_feature['2_w_w-1'] = '%s,%s' %(word_list[index-1], word_list[index])
    dict_feature['3_t'] = tag_list[index]
    dict_feature['4_t_t-1'] = '%s,%s' %(tag_list[index], tag_list[index])
    dict_feature['5_t_t-1_t-2'] = '%s,%s,%s' %(tag_list[index], tag_list[index-1], tag_list[index-2])

    if index < len(word_list)-1:
        dict_feature['6_w_w+1'] = '%s,%s' %(word_list[index], word_list[index+1])
        dict_feature['7_t_t+1'] = '%s,%s' %(tag_list[index], tag_list[index])

    if index < len(word_list)-2:
        dict_feature['8_tt_+1_t+2'] = '%s,%s,%s' %(tag_list[index], tag_list[index+1], tag_list[index+2])

    # todo: add for word position in lead sentence, word position, first word occurence position and tfidf and stop words

    return dict_feature
