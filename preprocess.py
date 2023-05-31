import pandas as pd
import re
import nltk
import glob
from nltk import word_tokenize
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm

def clean(text):
# Removes all special characters and numericals leaving the alphabets
    text = re.sub('[^A-Za-z,]+', ' ', text)
    text = re.sub(',', '.', text)
    return text

# POS tagger dictionary
pos_dict = {'J':wordnet.ADJ, 'V':wordnet.VERB, 'N':wordnet.NOUN, 'R':wordnet.ADV}
def token_stop_pos(text):
    tags = nltk.pos_tag(word_tokenize(text))
    newlist = []
    for word, tag in tags:
        if word.lower() not in set(stopwords.words('english')):
            newlist.append(tuple([word, pos_dict.get(tag[0])]))
    return newlist

wordnet_lemmatizer = WordNetLemmatizer()
def lemmatize(pos_data):
    lemma_rew = " "
    for word, pos in pos_data:
        if not pos:
            lemma = word
            lemma_rew = lemma_rew + " " + lemma
        else:
            lemma = wordnet_lemmatizer.lemmatize(word, pos=pos)
            lemma_rew = lemma_rew + " " + lemma
    return lemma_rew

def main():
    for path in tqdm(glob.glob('azlyrics-scraper/*.csv')):
        # csv_name = re.sub(r'[\b.*/|.csv\b]', '', path)
        df = pd.read_csv(path, usecols=range(5))

        # drop na lyrics
        df = df.dropna(subset=['LYRICS'])

        df['Cleaned Lyric'] = df['LYRICS'].apply(clean)
        df['POS tagged'] = df['Cleaned Lyric'].apply(token_stop_pos)
        df['Lemma'] = df['POS tagged'].apply(lemmatize)

        df.to_csv('csv_azlyrics/' + path.split('/')[1])

if __name__ == '__main__':
    main()