from nltk.translate.bleu_score import bleu
import math


def get_bleu_score(candidate_seq, full_text, N=3):
    
    all_words = []
    for line in full_text:
        parts = line.split('\x01')
        for part in parts:
            words = part.split()
            all_words.extend(words)

    weight = 1.0/N
    blue_score = 0.0
    for index in xrange(len(candidate_seq)-3):
        blue_score += bleu([all_words], candidate_seq[index: index+3], weight)

    return math.log(blue_score)