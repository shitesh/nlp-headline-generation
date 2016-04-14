# define all the feature functions here
"""List of features used:
1. Language model features

"""
import math


def compute_language_model_probablity(headline_word_tag_list):
    """
    computes probablity of consecutive words in the given input
    dict [word]={nextWord1: probablity,nextWord2: probablity,.....CurrentWordCount: count,others: smoothing}
    """
    prev = "start"
    cur = "start"
    LMProbablity={}
    #initialization of dictionary
    for entry in headline_word_tag_list:
        word, tag = entry.rsplit('/', 1)
        prev = cur
        cur = word
        LMProbablity[cur] = {}
        if 'CurrentWordCount' in LMProbablity[cur]:
            LMProbablity[cur]['CurrentWordCount']+=1
        else:
            LMProbablity[cur]['CurrentWordCount'] =1

        if prev in LMProbablity[cur]:
            LMProbablity[cur][prev]+=1
        else:
            LMProbablity[cur][prev] =1
    count = 1
    #update the probablity for words that don't exist and compute probablities
    prev = "start"
    cur = "start"
    for entry in headline_word_tag_list:
        word, tag = entry.rsplit('/', 1)
        LMProbablity[word]['others'] = 1/float(LMProbablity[word]['CurrentWordCount'])
        if count !=1:
            transition_prob = LMProbablity[cur][prev]
            LMProbablity[cur][prev] = transition_prob/float(LMProbablity[cur]['CurrentWordCount'])
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
    for entry in WordOfLine:
        word, tag = entry.rsplit('/', 1)
        if count != 1:
            LM_value += math.log(LMProbablity[cur][prev], 10)
        prev = cur
        cur = word
        count= count+1
    return LM_value


