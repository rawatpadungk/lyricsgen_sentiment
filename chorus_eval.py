import nltk

def pos_check(word):
    result=[]
    for i in word:
        pre_result=[]
        for j in nltk.word_tokenize(i):
            tag_word=nltk.pos_tag([j])
            pre_result.append(tag_word[0][1])
        result.append(tuple(pre_result))
    return nltk.FreqDist(result)


def evaluate(a,c,d,pos_freq,posi_freq,nega_freq):
    score=0
    a_word=[]
    
    for sentence in nltk.sent_tokenize(a):
        for i in nltk.word_tokenize(sentence):
            a_word.append(i)
            if i in c:
                score=score+posi_freq[i]
            if i in d:
                score=score+nega_freq[i]
    a_freq=nltk.FreqDist(a_word)

    pos_result=[]

    for sentence in nltk.sent_tokenize(a):
        for i in nltk.word_tokenize(sentence):
            tag_word=nltk.pos_tag([i])
            pos_result.append(tag_word[0][1])
            score=score+a_freq[i]

    if tuple(pos_result) in pos_freq:
        score=score+pos_freq[tuple(pos_result)]
    
    return score