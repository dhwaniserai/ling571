import json
import codecs
import sys
import nltk
import numpy as np
from sklearn import svm
from sklearn.metrics import f1_score
import pandas as pd

glove_file=sys.argv[1]
relation_train=sys.argv[2]
relation_test=sys.argv[3]
training_vec=sys.argv[4]
testing_vec=sys.argv[5]
output=sys.argv[6]

def load_glove_model(glove_file):
    f = codecs.open(glove_file, 'r', encoding='utf-8')
    model = {}
    embedding = np.array([])
    for line in f:
        split_line = line.split()
        word = split_line[0]
        embedding = np.array([float(val) for val in split_line[1:]])
        model[word] = embedding
    shape = embedding.shape
    return model, shape

def load_conll_relations(connl_file): #json file
    pdtb_file = codecs.open(connl_file, encoding='utf8')
    relations = [json.loads(x) for x in pdtb_file]
    return relations

def average_relation_vector(relations, embeddings, embed_shape):
    #relation has two arguments and we have to take average of the embedding vectors individually
    average = []
    for i in range(len(relations)):
        line = relations[i]['Arg1']['RawText']
        tokens = nltk.word_tokenize(line)
        vec1=get_embed_vector(tokens, embeddings, embed_shape)
        avg1 = np.mean(vec1, axis=0)
        

        line = relations[i]['Arg2']['RawText']
        tokens = nltk.word_tokenize(line)
        vec2=get_embed_vector(tokens, embeddings, embed_shape)
        avg2 = np.mean(vec2, axis=0)

        average.append(np.concatenate((avg1,avg2), axis=None))
       
    avg_df = pd.DataFrame(average)
    return avg_df

def get_embed_vector(token_list, embeddings, embed_shape):
    zero_emb = np.zeros(shape=embed_shape,dtype=float)
    token_embed = [zero_emb for i in range(100)]
    min_len = min(100, len(token_list))
    for i in range(min_len):
        if token_list[i] in embeddings.keys():
            
            token_embed[i]=embeddings[token_list[i]]
    embed_vector = token_embed
    
    return embed_vector

def train_svm(train_X, train_Y):
    clf = svm.SVC(kernel='linear', random_state=5)
    clf.fit(train_X, train_Y)
    return clf

def test_svm(model, test_X, test_Y, f): # f is output file
    
    Y_true = test_Y
    Y_pred = model.predict(test_X)
    score = f1_score(Y_true, Y_pred, average=None)
    write_output(Y_true, Y_pred, score, f)
    return score

def write_output(Y_true, Y_pred, score, f):
    f.write("F1 score "+str(score)+'\n')
    for i in range(len(Y_true)):
        f.write(str(Y_true[i])+'\t'+str(Y_pred[i])+'\n')


glove_emb, glove_shape = load_glove_model(glove_file)
conll_train = load_conll_relations(relation_train)
conll_test = load_conll_relations(relation_test)

train_X = average_relation_vector(conll_train, glove_emb, glove_shape)
train_Y = [rel['Sense'][0].split('.')[0] for rel in conll_train]

train_X['Sense'] = train_Y #for printing as csv

print(train_X['Sense'].value_counts())
train_X.to_csv(training_vec, index=None, header=None)
train_X = train_X.drop('Sense', axis=1)


svm_model = train_svm(train_X, train_Y)


test_X = average_relation_vector(conll_test, glove_emb, glove_shape)
test_Y = [rel['Sense'][0].split('.')[0] for rel in conll_test]

test_X['Sense'] = test_Y #for output purposes
test_X.to_csv(testing_vec, index=None, header=None)
print("test")
print(test_X['Sense'].value_counts())
test_X = test_X.drop('Sense', axis=1)

f=open(output, 'w+')
score = test_svm(svm_model, test_X, test_Y, f)
f.close()