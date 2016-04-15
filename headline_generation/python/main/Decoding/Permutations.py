import Queue
from itertools import *
import sys
import os

q = Queue.PriorityQueue()

print 'Stop at 5:'
arr=['ABCD','HI',"how","are","u"]
words=[]

def permutations(file):
    """ Caluclation of the permutations in the words"""
    f= open(file,'r')
    for line in f:
        val = line.strip()
        if val =='<text>':
            val =next(f)
            while val.strip()!="</text>":
                wordtags= val.split(" ")
                for entry in wordtags:
                    word,tag = entry.rsplit('/',1)
                    words.append(word)
                #call functions
                val =next(f)
    for i in permutations(word,4):
        print i




if __name__=="__main__":
    path="C:/Users/Sumukh/Documents/Masters/2ndsem/subjects/NLP/project"
#    path = sys.argv[1]
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            datafile = os.path.join(root, name)
            permutations(datafile)