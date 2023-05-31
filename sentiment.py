import csv
import nltk
from nltk import FreqDist
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tag import pos_tag

   
# analysis sentimental score

def analysis_sentiment(lyric,state):
    check=SentimentIntensityAnalyzer()
    important_tag=['VB','VBD','VBG','VBP','VBZ']
    positive=[]
    negative=[]
    neutral=[]
    total_word_num=[]

    num_posi=0
    num_nega=0
    num_neut=0

    for song in lyric:
        total_num=0
        if state=='word':
            tokens= nltk.word_tokenize(song)
            for token in tokens:
                total_num=total_num+1
                score=check.polarity_scores(token)
                if score['compound']>0.5:
                    positive.append(token)
                    num_posi=num_posi+1
                elif score['compound']>-0.5 and score['compound']<0.5:
                    neutral.append(token)
                    num_neut=num_neut+1
                else:
                    negative.append(token)
                    num_nega=num_nega+1
            total_word_num.append(total_num)
        else:
            tokens=song.split(".")
            for token in tokens:
                total_num=total_num+1
                check_list=[]
                for word in nltk.word_tokenize(token):
                    score=check.polarity_scores(word)
                    if score['compound']>0.5 or score['compound']<-0.5:
                        check_list.append(word)
                if check_list!=[]:
                    score=check.polarity_scores(check_list[-1])
                else:
                    score=check.polarity_scores(token)
                    
                if score['compound']>0.5:
                    positive.append(token)
                    num_posi=num_posi+1
                elif score['compound']>-0.5 and score['compound']<0.5:
                    neutral.append(token)
                    num_neut=num_neut+1
                else:
                    negative.append(token)
                    num_nega=num_nega+1
            total_word_num.append(total_num)
        
 
    return positive, neutral, negative, num_posi,num_neut,num_nega, total_word_num

def find_num(posi_num,neut_num,nega_num,total_word_num):
    total_emotion_num=posi_num+neut_num+nega_num

    posi_percent=posi_num/total_emotion_num
    nega_percent=nega_num/total_emotion_num
    neut_percent=neut_num/total_emotion_num

    # count average word of song 
    total_num_freq=FreqDist(total_word_num)
    a=0
    b=0

    for (i,j) in total_num_freq.most_common(len(total_num_freq)):
        a=a+j
        b=b+i*j

    num_average_word=b/a

    posi_num=int(num_average_word*posi_percent)
    nega_num=int(num_average_word*nega_percent)
    neut_num=int(num_average_word*neut_percent)

    return posi_num, nega_num, neut_num

def chorus_checker(song): # check sentence num to use 
    result=[]
    sentence=[]
    result_sentence=[]
    for s in song:
        for i in s.split('.'):
            sentence.append(i)
        result_freq=FreqDist(sentence)
        for i,j in result_freq.most_common(len(result_freq)):
            for a,b in result_freq.most_common(len(result_freq)):
                if len(i)>10 and i!='' and i!=a and j>2 and b>2:
                    if i in a:
                        result_sentence.append(i+'.')
                        result.append(j+b)


    
    return FreqDist(result),result_sentence #check chorus num to use in result_num_freq and num of sentence in song
