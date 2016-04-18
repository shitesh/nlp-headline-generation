# -*- coding: utf-8 -*-
import numpy as np


#A = "हाल ही में राज्य"
#B = "हाल ही में "

#print A.decode("utf-8")


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
    for word in A:
        index = words[word]
        a[index] += 1

    for word in B:
        index = words[word]
        b[index] += 1


    # use numpy's dot product to calculate the cosine similarity
    sim = np.dot(a, b) / np.sqrt(np.dot(a, a) * np.dot(b, b))
    print "cosine value is "+str(sim)
    return sim

#print evaluation(A,B)