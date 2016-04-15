# -*- coding: utf-8 -*-
# tfidf with hindi stopwords
import nltk
import codecs
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = None

def tokenise(text):
    x = nltk.word_tokenize(text)
    return_list = []
    for i in x:
        i = i.replace(',', '').replace('.', '').replace(u'।', '')
        if not i:
            continue
        return_list.append(i) # can use stemmer here
    return return_list

def generate_tfidf_values(all_text):
    global tfidf
    file = codecs.open('hindi_stopwords.txt', 'r', encoding='utf-8')
    stop_words = file.readlines()
    stop_words = [word.strip() for word in stop_words]
    tfidf = TfidfVectorizer(tokenizer=tokenise, stop_words=stop_words)
    tfidf.fit_transform(all_text)


def read_file(file_location):
    file = codecs.open(file_location, 'r', encoding='utf-8')
    file_contents = []
    for line in file:
        file_contents.append(line.strip())
    return ' '.join(file_contents)

all_text = []
all_text.append(read_file('hindi_train1.txt'))
all_text.append(read_file('hindi_train2.txt'))

generate_tfidf_values(all_text)

check = u"सुबहas"
response = tfidf.transform([check])
print response
print response.nonzero()[1]
feature_names = tfidf.get_feature_names()
for col in response.nonzero()[1]:
    print feature_names[col], ' - ', response[0, col]
