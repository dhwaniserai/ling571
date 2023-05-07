import sys
import os
import nltk
from nltk import grammar, parse
from nltk.tokenize import word_tokenize

grammar_file = sys.argv[1]
sentence_file = sys.argv[2]
output = sys.argv[3]


gram=''
with open(grammar_file,'r') as f:
    gram = f.read().strip()
grammar = grammar.FeatureGrammar.fromstring(gram)
parser = parse.FeatureChartParser(grammar, trace=1)

sentences = []
with open(sentence_file,'r') as f:
    txt = f.read()
    sentences = [line for line in txt.split('\n') if line.strip() != '']

f=open(output,'w+')
for sent in sentences:
    sent = sent.strip()
    tokens = sent.split(' ')
    trees = parser.parse(tokens)
    for tree in trees: 
        f.write(str(tree.label()['SEM']))
    f.write("\n")

f.close()