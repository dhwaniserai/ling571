import sys
import nltk
import scipy
from scipy.spatial import distance
import re
import pandas as pd
import math
from gensim.models import Word2Vec


window=int(sys.argv[1]) #sliding window size
judgment_filename=sys.argv[2] 
output_filename=sys.argv[3]

def preprocess(sent_list):
    slist = []
    for i in range(len(sent_list)):
        sent = sent_list[i]
        wlist = []
        #print(word)
        for word in sent:
            word = re.sub("\W", '',  word)
            word = word.lower()
            if word !='':
                wlist.append(word)
        slist.append(wlist)
    return slist

brown_sents = nltk.corpus.brown.sents()

mod_brown = preprocess(brown_sents)

model = Word2Vec(sentences=mod_brown, size=100, window=window, min_count=1, workers=1)
word_vectors = model.wv

with open(judgment_filename,'r') as f:
    judgements = f.readlines()

human_similarity = [judge.split(',') for judge in judgements]

f=open(output_filename,'w+')
h_similarity = []
c_similarity = []
for sent in human_similarity:
    if len(sent)==3:
        wd1,wd2,hsim = sent[0],sent[1],sent[2]
        h_similarity.append(hsim)
        csim = model.similarity(wd1,wd2)
        
        c_similarity.append(csim)
        
        f.write(wd1+','+wd2+':'+str(csim)+'\n')
corr=scipy.stats.spearmanr(h_similarity,c_similarity)[0]
f.write('Correlation:'+str(corr))

f.close()