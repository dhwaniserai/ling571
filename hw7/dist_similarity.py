import sys
import nltk
import scipy
from scipy.spatial import distance
import re
import pandas as pd
import math
import numpy as np

window=int(sys.argv[1]) #sliding window size
weighting=sys.argv[2] #'FREQ' or 'PMI'
judgment_filename=sys.argv[3] 
output_filename=sys.argv[4]

def preprocess(word_list):
    mod = []
    for i in range(len(word_list)):
        word = word_list[i]
        #print(word)
        word = re.sub("\W", '',  word)
        word = word.lower()
        if word !='':
            mod.append(word)
    #mod = [word for word in word_list if word !='']
    return mod

def create_cooccurrence_matrix(word_list, window_size):
    vocabulary = {}
    data = []
    row = []
    col = []

    for pos, token in enumerate(word_list):
        i = vocabulary.setdefault(token, len(vocabulary))
        start = max(0, pos-window_size)
        end = min(len(word_list), pos+window_size+1)
        for pos2 in range(start, end):
            if pos2 == pos: #the main word element
                continue
            j = vocabulary.setdefault(word_list[pos2], len(vocabulary))
            data.append(1)
            row.append(i)
            col.append(j)
    M=len(vocabulary) #shape = (MxM)
    cooccurrence_matrix_sparse = scipy.sparse.coo_matrix(arg1=(data, (row, col)))
    return vocabulary, cooccurrence_matrix_sparse

def pmi(df, positive=True):
    col_total = df.sum(axis=0)
    total = col_total.sum()
    row_total = df.sum(axis=1)
    expected = np.outer(row_total, col_total) / total
    df = df / expected
    with np.errstate(divide='ignore'): #removing warnings for log(0)
        df = np.log(df)
    df[np.isinf(df)] = 0.0  # log(0) = 0
    if positive:
        df[df < 0] = 0.0
    return df


def get_largest10(df_co_occ):
    dfs = []
    for word in df_co_occ:
        top=df_co_occ[word].nlargest(n=10)
        dfs.append(pd.DataFrame({word: top}).reset_index(drop=True))
        #print(word,end=' ')
    df_max_co_occ = pd.concat(dfs,axis=1)
    return df_max_co_occ

def op_maxn_features(word,word_features,num):
    op_str=''
    top=word_features.nlargest(n=num)
    op_str+= word + ' '
    for feature in top.keys():
        op_str += feature+':'+str(word_features[feature])+' '
    return op_str


brown_words = nltk.corpus.brown.words()

mod_brown = preprocess(brown_words)
df_co_occ = pd.DataFrame()
if weighting =='FREQ':
    vocabs, co_occ = create_cooccurrence_matrix(mod_brown,window)
    df_co_occ  = pd.DataFrame(co_occ.todense(),
                            index=vocabs.keys(),
                            columns = vocabs.keys())

elif weighting=='PMI':
    vocabs, co_occ = create_cooccurrence_matrix(mod_brown,window)
    df_occ  = pd.DataFrame(co_occ.todense(),
                            index=vocabs.keys(),
                            columns = vocabs.keys())
    df_co_occ = pmi(df_occ, positive=True)


judgements = []
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
        near = distance.cosine(df_co_occ[wd1],df_co_occ[wd2])
        csim = 1-near
        c_similarity.append(csim)
        f.write(op_maxn_features(wd1,df_co_occ[wd1],10)+'\n')
        f.write(op_maxn_features(wd2,df_co_occ[wd2],10)+'\n')
        f.write(wd1+','+wd2+':'+str(csim)+'\n')
corr=scipy.stats.spearmanr(h_similarity,c_similarity)[0]
f.write('Correlation:'+str(corr))

f.close()




