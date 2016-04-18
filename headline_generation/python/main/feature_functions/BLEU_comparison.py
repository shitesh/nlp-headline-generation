# -*- coding: utf-8 -*-
from nltk.translate.bleu_score import bleu
import math


def get_bleu_score(candidate_text, full_text, N=3):

    all_words = []
    parts = full_text.split('\x01')
    for part in parts:
        words = part.split()
        for word in words:
            word = word.rsplit('/', 1)[0]
            all_words.append(word)

    weight = 1.0/N
    bleu_score = 0.0
    candidate_seq = candidate_text.split()
    candidate_seq = [word.rsplit('/', 1)[0] for word in candidate_seq]

    for index in xrange(len(candidate_seq)-2):
        bleu_score += bleu([all_words], candidate_seq[index: index+3], [weight])

    return bleu_score

