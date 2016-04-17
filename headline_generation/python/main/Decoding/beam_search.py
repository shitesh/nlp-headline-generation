import codecs
import copy
from content_selection_classify import *
initialise()
from headline_synthesis_classify import *
headline_synthesis_initialise()

from itertools import permutations
print 'done initialising'
file = codecs.open('/tmp/trial/10469_TAGGED.txt_2', encoding='utf-8')
text = file.read()

top_20_words = classify_new_file('/tmp/trial/10486_TAGGED.txt')

top_word_list = list(top_20_words.keys())

for key, value in top_20_words.iteritems():
    print key, value

from heapq import heappush, heappop
heap = []
next_heap = []

for word in top_word_list:
    heappush(heap, (0, [word]))

from datetime import datetime
print datetime.now()
file =  codecs.open('/tmp/output.txt', 'w', encoding='utf-8')

i=0
max_length = 20
while i < max_length:
    if i <=5:
        max_range = 21
    else:
        max_range = 11

    for m in xrange(1, max_range):
        prob, word = heappop(heap)

        for all_word in top_word_list:
            if all_word not in word:
                word_copy = copy.deepcopy(word)
                word_copy.append(all_word)
                word_str = ' '.join(word_copy)
                probab_value = get_headline_synthesis_score(word_str, top_20_words, text)
                file.write('%s- %s\n' %(word_str, probab_value))
                heappush(next_heap, (probab_value, word_copy))
    heap = next_heap
    next_heap = []
    i += 1
    max_length = 6
file.close()
print datetime.now()
for i in xrange(0,30):
    x, y = heappop(heap)
    print x , ' '.join(y)