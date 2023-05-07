import sys
import os
import nltk
from nltk import grammar, parse
from nltk.tokenize import word_tokenize


#print(sys.argv)
gram=''
with open(sys.argv[1],'r') as f:
    gram = f.read().strip()
grammar = grammar.FeatureGrammar.fromstring(gram)
parser = parse.FeatureEarleyChartParser(grammar)

sentences = []
with open(sys.argv[2],'r') as f:
    sentences = f.readlines()
#print(sentences)
f=open(sys.argv[3],'w+')
for sent in sentences:
    sent = sent.strip()
    tokens = word_tokenize(sent)
    #print(tokens)
    trees = parser.parse(tokens)
    #print(trees._pformat_flat())
    for tree in trees: 
        flat_tree = tree._pformat_flat("","()",False)
        f.write(flat_tree)
    f.write("\n")
f.close()