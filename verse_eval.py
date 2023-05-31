import csv
import nltk

from nltk.translate import bleu_score, nist_score, meteor_score

def bleu_eval(reference, genlyric):
    """
    return the average BLEU score

    PARAMETERS:
    reference: list(list(str))
    genlyric: str
    """
    total_bleu_score = 0
    lines = genlyric.split(' . ')
    for line in lines: 
        line_score = bleu_score.sentence_bleu(reference, nltk.word_tokenize(line))
        total_bleu_score += line_score
    avg_bleu_score = total_bleu_score / len(lines)
    return avg_bleu_score

def nist_eval(reference, genlyric):
    """
    return the average NIST score

    PARAMETERS:
    reference: list(list(str))
    genlyric: str
    """
    total_nist_score = 0
    lines = genlyric.split(' . ')
    for line in lines: 
        try:
            line_score = nist_score.sentence_nist(reference, nltk.word_tokenize(line))
        except ZeroDivisionError:
            line_score = 0
        # print(line_score)
        total_nist_score += line_score
    # print('end')
    avg_nist_score = total_nist_score / len(lines)
    return avg_nist_score

def meteor_eval(reference, genlyric):
    """
    return the average METEOR score

    PARAMETERS:
    reference: list(list(str))
    genlyric: str
    """
    total_meteor_score = 0
    lines = genlyric.split(' . ')
    for line in lines: 
        line_score = meteor_score.meteor_score(reference, line.split(' . '))
        total_meteor_score += line_score
    avg_meteor_score = total_meteor_score / len(lines)
    return avg_meteor_score

