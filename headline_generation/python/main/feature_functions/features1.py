#!/usr/bin/python
# -*- coding: utf-8 -*
# define all the feature functions here
"""List of features used:
1. Word Translation Model
things to do for this feature:
a) get possible synonyms of verb words from hindi_wordnet
b) check occurrence of the synonyms in the article part.
c) formula:
pWT = (number of times wi occurs in headline and wj occurs in news story in the training data)/(number of times wj is observed in the news stories in the training
data)

d) finally update the content selection scoreS:
we just multiply the content selection probability of word wj with the
probabilistic weight with which another word wi can be substituted for it.

"""

def get_word_translation(word_tag_list):
    """Returns the feature dictionary for word translation of verb words in news article
    """
    verb_word_list_headline = []
    verb_word_list_article = []

    for entry in word_tag_list:
        word, tag = entry.rsplit('/', 1)

        #word_list.append(word)
        #tag_list.append(tag)
    #return a dictionary as in the main doc ie dict[word][ subWords] = probablity




import os
import sys
print sys.getdefaultencoding()
from sys import argv

script, input = argv

Files_in_Directory = []
verb_word_list_headline = {}
verb_word_list_article = {}
    



def get_files_in_folder():
    '''
Loops over the directory to get available files  	
'''    	 	
    for dirName, subdirList, fileList in os.walk(input):
            for fname in fileList:
                if fname.endswith(".txt"):
                    fn = os.path.join(dirName,fname)
                    Files_in_Directory.append(fn)

#prints any given dictionary
def PrintDictionary(d):
    i=0
    for key,val in d.items():
         print str(i)+")"+key, "=>", val
         i= i+1


def count_verbs():
    '''
	get count of verb in articles and verb in articles 
    '''
    global verb_word_list_headline,verb_word_list_article
    
    for fname in Files_in_Directory:
       with open(fname, 'r') as filename:
	startFlag = 0		
	print "###########################################################################################"
        print "Current File:"+fname
       	for line in filename:
		line = line.strip()
            	WordOfLine = line.split()
            	for entry in WordOfLine:
        		word, tag = entry.rsplit('/', 1)
    			
				
			if (word == "<Headline>") or (tag == "<Headline>"):
				#print "found headline $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
				startFlag = 1
		        elif (word == "</Headline>") or (tag == "</Headline>"):
				#print "found headline end $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
				startFlag = 0
			else:
				#print "word:"+word
				#dd other kinds of verb tags too!!
				if tag == "VM":				
					
					if startFlag==1:
						#print "word:"+word+"tag:"+tag+"flag:"+str(startFlag)
						if word in verb_word_list_headline:
							verb_word_list_headline[word]+=1
						else:
							verb_word_list_headline[word]=1
					else:
						#print "word:"+word+"tag:"+tag+"flag:"+str(startFlag)	
						if word in verb_word_list_article:
							verb_word_list_article[word]+=1
						else:
							verb_word_list_article[word]=1
	print "###########################################################################################"
get_files_in_folder()
count_verbs()
print "verb headline dictionary"
PrintDictionary(verb_word_list_headline)
print "verb article dictionary"
PrintDictionary(verb_word_list_article)
