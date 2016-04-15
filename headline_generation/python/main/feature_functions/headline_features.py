# define all the feature functions here
"""
List of features used:
1. Language model features
2. Headline Length feature
3. Part of Speech Language Model Feature
To add:
4. N-Gram Match feature
5. Content selection feature
"""

import math

def compute_POS_language_feature(headline_word_tag_list):
    """ Returns POS language model feature value for the headline
    """
    POSLM_feature = 0
    trigram_dict = generate_trigram_counts(headline_word_tag_list)
    bigram_dict = generate_bigram_counts(headline_word_tag_list)
    prev = "start"
    cur = "start"
    next = "start"
    count = 1

    #initialization of dictionary
    for entry in headline_word_tag_list:
        word, tag = entry.rsplit('/', 1)
        if count>2 :
            probablity = (trigram_dict[prev][cur][next])/float(bigram_dict[prev][cur])
            POSLM_feature = math.log(probablity, 10)
        prev = cur
        cur = next
        next = tag
        count = count+1
    return POSLM_feature


def generate_trigram_counts(headline_word_tag_list):
    """ Returns a dictionary with bigram score of each word pair
    """

    POS_LMProbablity={}
    count = 0
    prev = "start"
    cur = "start"
    next = "start"
    POS_LMProbablity={}
    #initialization of dictionary
    for entry in headline_word_tag_list:
        word, tag = entry.rsplit('/', 1)
        prev = cur
        cur = next
        next = tag
        POS_LMProbablity[prev] = {}

        if cur in POS_LMProbablity[prev]:
            if next in POS_LMProbablity[prev][cur]:
                POS_LMProbablity[prev][cur][next]+=1
            else:
                POS_LMProbablity[prev][cur][next] =1
        else:
            POS_LMProbablity[prev][cur][next] =1



    return POS_LMProbablity







def generate_bigram_counts(headline_word_tag_list):
    """ Returns a dictionary with bigram score of each word pair
    """

    POS_LMProbablity={}
    count = 0
    prev = "start"
    cur = "start"
    POS_LMProbablity={}
    #initialization of dictionary
    for entry in headline_word_tag_list:
        word, tag = entry.rsplit('/', 1)
        prev = cur
        cur = tag
        POS_LMProbablity[prev] = {}

        if cur in POS_LMProbablity[prev]:
            POS_LMProbablity[prev][cur]+=1
        else:
            POS_LMProbablity[prev][cur] =1

    return POS_LMProbablity

def compute_content_selection_feature(headline_word_tag_list):
    """ Returns content selection score of the given headline
    """


def compute_headline_length_feature(headline_word_tag_list):
    """
    computes the log of headline length and returns the value
    """
    Length_feature = 0
    count = 0
    tokens = headline_word_tag_list.split(" ")
    for entry in tokens:
        word, tag = entry.rsplit('/', 1)
        count = count+1
    Length_feature = math.log(count, 10)
    return Length_feature





def compute_language_model_probablity(headline_word_tag_list):
    """
    computes probablity of consecutive words in the given input
    dict [word]={nextWord1: probablity,nextWord2: probablity,.....CurrentWordCount: count,others: smoothing}
    """
    prev = "start"
    cur = "start"

    LMProbablity={}

    #initialization of dictionary
    tokens = headline_word_tag_list.split(" ")

    for entry in tokens:
        word, tag = entry.rsplit('/', 1)
        LMProbablity[word] = {}

    #calculates the word given previous word probablity
    for entry in tokens:
        word, tag = entry.rsplit('/', 1)
        prev = cur
        cur = word
        if 'CurrentWordCount' in LMProbablity[cur]:
            LMProbablity[cur]['CurrentWordCount']+=1
        else:
            LMProbablity[cur]['CurrentWordCount'] =1

        if prev in LMProbablity[cur]:
            LMProbablity[cur][prev]+=1
        else:
            LMProbablity[cur][prev] =1
    count = 1
    #update the probablity for words that don't exist and compute probabilities
    prev = "start"
    cur = "start"
    for entry in tokens:
        word, tag = entry.rsplit('/', 1)
        LMProbablity[word]['others'] = 1/float(LMProbablity[word]['CurrentWordCount'])
        if count !=1:
            transition_prob = LMProbablity[cur][prev]
            LMProbablity[cur][prev] = transition_prob/float(LMProbablity[prev]['CurrentWordCount'])
        prev = cur
        cur = word

    return LMProbablity






def get_language_model(headline):
    """Returns the language model value
    """
    LMProbablity = compute_language_model_probablity(headline)

    prev = "start"
    cur = "start"
    headline =  headline.strip()
    WordOfLine = headline.split()
    count = 1
    LM_value = 0
    tokens = headline.split(" ")
    for entry in tokens:
        word, tag = entry.rsplit('/', 1)
        if count != 1:
            if prev in LMProbablity[cur]:
                LM_value += math.log(LMProbablity[cur][prev], 10)
            #if word given previous word probablity does not exist we use others value as smoothing measure
            else:
                LM_value += math.log(LMProbablity[cur]['others'], 10)
        prev = cur
        cur = word
        count= count+1
    return LM_value


