# -*- coding: utf-8 -*-
from math import*
import re, math
from collections import Counter

WORD = re.compile(r'\w+')
genarated_headline=""
actual_headline=""

def jaccard(actual_headline,genarated_headline):
    """ This where juccard fucntionality will happen"""
    x = actual_headline.split(" ")
    y= genarated_headline.split(" ")
    intersection_cardinality = len(set.intersection(*[set(genarated_headline), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)

def get_cosine(actual_headline, genarated_headline):
    """ this is cosine functionality without a term frequency"""
    vec1 = text_to_vector(genarated_headline)
    vec2 = text_to_vector(actual_headline)
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

if __name__=="__main__":
    print "heelo"