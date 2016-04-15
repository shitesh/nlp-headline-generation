# -*- coding: utf-8 -*-
import codecs
import sys
import os
# define all the feature functions here

import math


def cal_totalwords(lines):
    word_list = []
    dict_probs = {}

    for line in lines:
        val = line.strip()
        if val == '</text>':
            break
        wordtags = val.split()
        for entry in wordtags:
            word, tag = entry.rsplit('/', 1)
            word_list.append(word)


    total_len=len(word_list)
    first_range=math.floor((0.1)*total_len)
    second_range=math.floor((0.9)*total_len)

    dict_probs['total_len'] = total_len
    dict_probs['first_range'] = first_range
    dict_probs['second_range'] = second_range
    return dict_probs
#caluclate the word range for the file this ca


def get_word_range(lines):
    """Return the dict contain the lead postion of the words in the file i.e if the word is present in the first sentence or not
    """
    position_parameters = {}
    total_length = cal_totalwords(lines)
    #if the first sentence is encountered add lead postion value to one for that particular word
    firstSentence = 1
    current_count = 0

    for line in lines:
        line = line.strip()
        if line == "</text>":
            break
        if firstSentence==1:
            wordtags = line.split()

            for entry in wordtags:
                current_count += 1
                word, tag = entry.rsplit('/',1)
                if word not in position_parameters:
                    position_parameters[word] = {}
                    position_parameters[word]['range'] = []
                    position_parameters[word]['lead_sentence'] = 1
                    position_parameters[word]['first_occurance'] = current_count
                 # Added the word postion for each token and also added the word rage for given word

                if current_count <= total_length['first_range']:
                    position_parameters[word]['range'].append('1_10')
                elif total_length['total_len'] >= current_count >= total_length['second_range']:
                    position_parameters[word]['range'].append('90_100')
                else:
                    position_parameters[word]['range'].append('10_90')
                #returns the word position for each word,word lindex is associated with current count
            firstSentence=0

        else:
            wordtags= line.split()
            for entry in wordtags:
                current_count += 1
                word,tag = entry.rsplit('/', 1)
                if word not in position_parameters:
                    position_parameters[word] = {}
                    position_parameters[word]['range'] = []
                    position_parameters[word]['lead_sentence'] = 0
                    position_parameters[word]['first_occurance'] = current_count
                 # Added the word postion for each token and also added the word rage for given word
                if current_count<=total_length['first_range']:
                    position_parameters[word]['range'].append('1_10')
                elif total_length['total_len'] >= current_count >= total_length['second_range']:
                    position_parameters[word]['range'].append('90_100')
                else:
                    position_parameters[word]['range'].append('10_90')

    return position_parameters
