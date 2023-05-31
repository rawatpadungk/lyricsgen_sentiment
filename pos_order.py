import csv
import nltk
from collections import defaultdict

# oepn csv file
def open_csv(path):
    with open(path, newline='',encoding='UTF8') as csvfile:
        reader = csv.reader(csvfile)
        header=next(reader)
        a = header.index('LYRICS')
        b = header.index('ARTIST_NAME')
        lyric=[]
        for row in reader:
            if row[b]=='ariana grande':
                lyric.append(row[a])
        return lyric

def pos_sents(lyrics):
    sent2pos_dict = defaultdict(list)   # dictionary for looking up the pos structure of the sentence (sentence -> POS structure)
    pos2sent_dict = defaultdict(list)   # dictionary for looking up the corresponding sentence with the certain POS structure (POS structure -> sentence)
    ordered_sents = []  # the sentences in the lyrics in order
    tagged_pos_sents = []   # the POS structures in the lyrics in order
    for lyric in lyrics:
        ordered_sent = []  # the sentences in the lyrics in order
        tagged_pos_sent = []   # the POS structures in the lyrics in order
        sents = lyric.split(",")
        for sent in sents:
            tagged_words = nltk.pos_tag(nltk.word_tokenize(sent), tagset='universal')
            k = tuple([t for _, t in tagged_words])
            v = tuple([w for w, _ in tagged_words])
            tagged_pos_sent.append(k)
            ordered_sent.append(v)
            pos2sent_dict[k].append(v)
            sent2pos_dict[v].append(k)
        ordered_sents.append(ordered_sent)
        tagged_pos_sents.append(tagged_pos_sent)
    return ordered_sents, tagged_pos_sents, sent2pos_dict, pos2sent_dict

def analyze_freq_pos_sents(taggedlist, most_n=None):
    fd = nltk.FreqDist(taggedlist)
    return fd.most_common(most_n)

def main():
    sample_songs = open_csv('csv_azlyrics/azlyrics_lyrics_a.csv')
    ordered_sents_sample, tagged_pos_sents_sample, sent2pos_dict_sample, pos2sent_dict_sample = pos_sents(sample_songs)

    # example analysis
    most_n_freq_pos_sents = analyze_freq_pos_sents(tagged_pos_sents_sample[0])
    print(most_n_freq_pos_sents)    # print the frequency distribution of sentence structures

    most_common_pos_struct = most_n_freq_pos_sents[0][0]
    print(f'\nConsider the POS structure: {most_common_pos_struct}\n')
    all_sents_most_freq_struct = pos2sent_dict_sample[most_common_pos_struct]
    print(all_sents_most_freq_struct)   # print the sentence of which the POS structure is the most common among the lyrics

main()