import os
import nltk
import csv
import re
import string
import random
from graph import Graph, Vertex
from sentiment import chorus_checker,analysis_sentiment,find_num
import pprint
from nltk import FreqDist
from verse_eval import bleu_eval, nist_eval, meteor_eval
from chorus_eval import pos_check, evaluate

import warnings
warnings.filterwarnings('ignore')

# oepn csv file
def open_csv(path, singer):
    with open(path, newline='',encoding='UTF8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        lyric_col = header.index('Cleaned Lyric')
        name_col = header.index('ARTIST_NAME')
        lyrics = []
        for row in reader:
            if row[name_col] == singer:
                lyrics.append(row[lyric_col])
        return lyrics
    

def make_graph(words):
    g = Graph()
    prev_word = None
    # for each word
    for word in words:
        # check that word is in graph, and if not then add it
        word_vertex = g.get_vertex(word)

        # if there was a previous word, then add an edge if does not exist
        # if exists, increment weight by 1
        if prev_word:  # prev word should be a Vertex
            # check if edge exists from previous word to current word
            prev_word.increment_edge(word_vertex)

        prev_word = word_vertex

    g.generate_probability_mappings()
    
    return g

def compose(g, words, length=50, min_nwords_in_sent=6, start_word=None, verse=False):
    composition = []
    if start_word:
        word = g.get_vertex(start_word)
    else:
        word = g.get_vertex(random.choice(words))
    nwords_in_sent = 0
    nword_generated = 0
    # for _ in range(length): 
    while nword_generated < length :
        # print(word.value, nwords_in_sent) ###
        composition.append(word.value)
        nwords_in_sent += 1
        next_word = g.get_next_word(word)
        if next_word.value == '.' and nwords_in_sent >= min_nwords_in_sent:
            # print('EOS') ###
            composition.append(next_word.value)
            word = g.get_next_word(next_word)
            nwords_in_sent = 0
        else:
            while next_word.value == '.' and nwords_in_sent < min_nwords_in_sent:
                # print('still random') ###
                if len(word.adjacent.keys()) == 1: # in case we can choose only '\.' 
                    composition.append(next_word.value)
                    next_word = g.get_next_word(next_word)
                    nwords_in_sent = 0
                    break
                else:
                    next_word = g.get_next_word(word)
            word = next_word
        nword_generated += 1
        if verse:
            if nword_generated == length and nwords_in_sent != 0:
                nword_generated -= 1

    # print(f'Number of words = {len(composition)}')
    return composition #list
            

def main():
    name = input("Enter the artist name (lowercase): ")
    lyrics = open_csv('csv_azlyrics/azlyrics_lyrics_' + name[0] + '.csv', name)
    
    sents_ref_nist = []
    sents_ref_meteor = [] # for verse evaluation
    words = []
    chorus_words=[]

    num_chorus_freq,chorus_word=chorus_checker(lyrics) #num of sentence to use 
    num_chorus_sent=num_chorus_freq.most_common(10)

    
    posi_word, neut_word, nega_word,posi_num_word,neut_num_word,nega_num_word,total_word_num=analysis_sentiment(lyrics,'word')

    chorus_freq_pos=pos_check(chorus_word)
    posi_freq_word=nltk.FreqDist(posi_word)
    nega_freq_word=nltk.FreqDist(nega_word) 

    for i in chorus_word:
        a = nltk.word_tokenize(i)
        chorus_words += a

    # print(lyrics)

    for lyric in lyrics:
        lyric_words = nltk.word_tokenize(lyric)
        lyric_sents = nltk.sent_tokenize(lyric)
        words += lyric_words
        sents_ref_nist += [nltk.word_tokenize(s)[:-1] for s in lyric_sents]
        sents_ref_meteor.append([s[:-1] for s in lyric_sents])
    
    g = make_graph(words)
    h = make_graph(chorus_words)

    chorus_score=0
    for i in range(100):
        composition_chorus1=compose(h,chorus_words,50,6,'i')
        generated_chorus1=' '.join(composition_chorus1)
        a=re.sub(r'\.', '\n', generated_chorus1)
        
        score1=evaluate(a,posi_word,nega_word,chorus_freq_pos,posi_freq_word,nega_freq_word)

        if score1>chorus_score:
            chorus_score=score1
            chorus=a


    # verse
    composition = compose(g, words, 300, 10, 'you', True)
    generated_lyric = ' '.join(composition)

    print("-------------------- this is the verse part --------------------")
    print(re.sub(r'\.', '\n', generated_lyric)) 

    print("-------------------- this is the chorus part --------------------")
    print(chorus)

    print("-------------------- Verse Evaluation --------------------")
    bleu_score = bleu_eval(sents_ref_nist, generated_lyric)
    nist_score = nist_eval(sents_ref_nist, generated_lyric)
    meteor_score = meteor_eval(sents_ref_meteor, generated_lyric)

    print(f'BLEU score = {bleu_score}')
    print(f'NIST score = {nist_score}')
    print(f'METEOR score = {meteor_score}')

if __name__ == '__main__':
    main()