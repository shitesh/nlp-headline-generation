import copy
from content_selection_classify import *
from headline_synthesis_classify import *
from heapq import heappush, heappop
from Utils import remove_tags_from_line

logger = None
LOG_FILE_LOCATION = 'parse_log.log'

def initialise_all():
    """Initialise the content selection and headline synthesis models

    """
    global logger
    initialise()
    headline_synthesis_initialise()
    logger = codecs.open(LOG_FILE_LOCATION, 'w', encoding='utf-8')


def get_file_headings(file_path, headline_length=8):
    """Creates the actual headings by parsing the passed file and generating sequences.

    """
    global logger
    top_sentence_list = []
    file = codecs.open(file_path, encoding='utf-8')
    text = file.read()
    file.close()

    top_20_words = classify_new_file(file_path)

    heap, next_heap = [], []
    for word in top_20_words:
        heappush(heap, (0, [word]))

    index = 0
    max_length = 20
    while index < max_length:
        if index < 1:
            max_range = 21
        elif index < 3:
            max_range = 3
        else:
            max_range = 2

        index2 = 1
        probability_list = []
        while heap and index2 < max_range:
            prob, word = heappop(heap)
            if prob not in probability_list:
                probability_list.append(prob)

            index2 += 1
            for all_word in top_20_words:
                if all_word not in word:
                    word_copy = copy.deepcopy(word)
                    existing_words = [word1.rsplit('/', 1)[0] for word1 in word_copy]
                    if all_word.rsplit('/', 1)[0] in existing_words:
                        continue
                    word_copy.append(all_word)
                    word_str = ' '.join(word_copy)
                    probab_value = get_headline_synthesis_score(word_str, top_20_words, text)
                    logger.write('%s- %s\n' %(word_str, probab_value))
                    heappush(next_heap, (-1*probab_value, word_copy))
        heap = next_heap
        next_heap = heap
        index += 1
        max_length = headline_length # change headline length if needed

    count = 0
    while heap and count < 10:
        count += 1
        probab, sentence = heappop(heap)
        top_sentence_list.append(remove_tags_from_line(sentence))
    return top_sentence_list
