#!/usr/bin/python
# -*- coding: utf-8 -*
import os
import sys
import codecs
from sys import argv
import numpy as np
script, input = argv
#from Evaluation.evaluate import evaluation
#from Evaluation.jaccard_cosine import jaccard


'''
Added a parser file which loops over all the files in a directory and generates similarity scores

'''
cosine_list = {}

def evaluation(s1,s2):
    '''
    returns cosine and tf idf evaluation for two given sentences
    '''

    words = {}
    i = 0
    # loop through each list, find distinct words and map them to a
    # unique number starting at zero

    for word in s1:
        if word not in words:
            words[word] = i
            i += 1

    for word in s2:
        if word not in words:
            words[word] = i
            i += 1


    # create a numpy array (vector) for each input list, filled with zeros
    word_list = list(words.keys())
    a = np.zeros(len(word_list))
    b = np.zeros(len(word_list))

    # loop through each list and create a corresponding vector for it
    # this vector counts occurrences of each word in the dictionary
    for word in s1:
        index = words[word]
        a[index] += 1

    for word in s2:
        index = words[word]
        b[index] += 1


    # use numpy's dot product to calculate the cosine similarity
    sim = np.dot(a, b) / np.sqrt(np.dot(a, a) * np.dot(b, b))
    #print "cosine value is "+str(sim)
    return sim



def jaccard(actual_headline,genarated_headline):
    """ This where jaccard fucntionality will happen"""
    x = actual_headline.split(" ")
    y= genarated_headline.split(" ")
    intersection_cardinality = len(set.intersection(*[set(genarated_headline), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)

Files_in_Directory = []


#Loops over the directory to get available files
def GetFilesInFolder():
    for dirName, subdirList, fileList in os.walk(input):
            for fname in fileList:
                if fname.endswith(".txt"):
                    fn = os.path.join(dirName,fname)
                    Files_in_Directory.append(fn)



def evaluate_headline():
    global cosine_list
    cosine  = 0.0
    max_cosine = 0.0
    global Files_in_Directory
    for fname in Files_in_Directory:
       print "current file:"+fname
       max_cosine = 0
       with codecs.open(fname, 'r', encoding='utf-8') as filename:
            count = 0
            for line in filename:

                line = line.strip()
                if count ==0:
                    actual = line
                else:
                    current =  line

                    cosine = evaluation(actual,current)

                    print "Actual Headline:"+actual.decode("utf-8")+"\nCandidate headline:"+current.decode("utf-8")+"\n  Cosine Value :"+str(cosine)

                    if(max_cosine<cosine):
                         max_cosine = cosine
                         cosine_list[fname]=max_cosine

                count+=1



#main
GetFilesInFolder()
evaluate_headline()
sorted_names = sorted(cosine_list.iteritems(), key=lambda (k, v): (-v, k))[:50]
print sorted_names
