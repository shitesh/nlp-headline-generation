# -*- coding: utf-8 -*-
import codecs
import sys
import os
# define all the feature functions here
import math

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
wordcount=0
current_count= 0
firstRange=0
secondRange=0
dict_feature={}
break_count=0
totaltags=[]
def get_outcome(word, heading):
    """Returns if the word is present in heading or not.

    """
    return word in heading

def get_feature_dict(line, index=2):
    """Returns the feature dictionary of POS tagged list of words(5 words are passed in the list).

    """
    word_tag_list=line.split(" ")
    global dict_feature
    global firstRange ,secondRange,current_count,break_count
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

    return dict_feature

def cal_totalwords(file):
    f1= codecs.open(file, 'r', encoding='utf-8')
    wordlist=[]
    dict_probs={}
    for line in f1:
        val = line.strip()
        if val =='<text>':
            val =next(f1)
            while val.strip()!="</text>":
                wordtags= val.split(" ")
                for entry in wordtags:
                    word,tag = entry.rsplit('/',1)
                    wordlist.append(word)
                #call functions
                val =next(f1)
    totallen=len(wordlist)
    first_range=math.floor((0.1)*totallen)
    second_range=math.floor((0.9)*totallen)
    dict_probs['total_len']=totallen
    dict_probs['first_range']=first_range
    dict_probs['second_range']=second_range
    return dict_probs
#caluclate the word range for the file this ca

def word_range(file):
    """Return the dict contain the the postion of all the words and their current position in thier sentence 
    """
    fop= codecs.open(file, 'r', encoding='utf-8')
    position_parameters={}
    global current_count,total_length
    #if the first sentence is encountered add lead postion value to one for that particular word
    firstSentence=1
    for line in fop:
        val = line.strip()
        if val =='<text>':
            val =next(fop)
            while val.strip()!="</text>":
                if firstSentence==1:
                    line = val.strip()
                    wordtags= line.split(" ")
                    for entry in wordtags:
                        current_count+=1
                        word,tag = entry.rsplit('/',1)
                        if word not in position_parameters:
                            position_parameters[word] = {}
                            position_parameters[word]['range']=[]
                            position_parameters[word]['leadsentence']=1
                            position_parameters[word]['firstoccurance']=current_count
                         # Added the word postion for each token and also added the word rage for given word
                        rangeArray=[]
                        if(current_count<=total_length['first_range']):
                            if word in position_parameters:
                                position_parameters[word]['range'].append('1_10')
                            else:
                                position_parameters[word]['range'].append('1_10')
                        elif current_count<=total_length['total_len'] and current_count>=total_length['second_range']:
                            if word in position_parameters:
                                position_parameters[word]['range'].append('90_100')
                            else:
                                position_parameters[word]['range'].append('90_100')
                        else:
                            if word in position_parameters:
                                position_parameters[word]['range'].append('10_90')
                            else:
                                position_parameters[word]['range'].append('10_90')
                        #returns the word position for each word,word lindex is associated with current count
                    firstSentence=0
                else:
                    line = line.strip()
                    wordtags= line.split(" ")
                    for entry in wordtags:
                        current_count+=1
                        word,tag = entry.rsplit('/',1)
                        if word not in position_parameters:
                            position_parameters[word]={}
                            position_parameters[word]['range']=[]
                            position_parameters[word]['leadsentence']=0
                            position_parameters[word]['firstoccurance']=current_count
                         # Added the word postion for each token and also added the word rage for given word
                        rangeArray=[]
                        if(current_count<=total_length['first_range']):
                            if word in position_parameters:
                                position_parameters[word]['range'].append('1_10')
                            else:
                                position_parameters[word]['range'].append('1_10')
                        elif current_count<=total_length['total_len'] and current_count>=total_length['second_range']:
                            if word in position_parameters:
                                position_parameters[word]['range'].append('90_100')
                            else:
                                position_parameters[word]['range'].append('90_100')
                        else:
                            if word in position_parameters:
                                position_parameters[word]['range'].append('10_90')
                            else:
                                position_parameters[word]['range'].append('10_90')

                val =next(fop)

    return position_parameters

if __name__=="__main__":
#    path="C:/Users/Sumukh/Documents/Masters/2ndsem/subjects/NLP/project"
    path = sys.argv[1]
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            datafile = os.path.join(root, name)
            total_length={}
            position_parameters={}
            total_length=cal_totalwords(datafile)
            position_parameters=word_range(datafile)