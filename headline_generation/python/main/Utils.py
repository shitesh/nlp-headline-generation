"""Contains all the common functions that are used in different scripts.

"""


def remove_tags_from_line(words):
    """Removes the trailing /POStag from each word and returns the sentence.

    """
    words = [word.rsplit('/', 1)[0] for word in words]
    return ' '.join(words)


def get_start_end_indices(index, length):
    """Returns the start and end indices given the current index.

    For any word, the model is dependent on previous two words, previous two POS tags, next two words and next two POS
     tags. This function helps in managing the corner cases near the beginning and end indices.
    """
    start_index, end_index = index, index+1
    if index - 2 >= 0:
        start_index = index - 2
    elif index - 1 >= 0:
        start_index = index - 1

    if index + 2 <= length - 1:
        end_index = index+3
    elif index+1 <= length - 1:
        end_index = index+2

    return start_index, end_index
