import sys
import nltk
from nltk.tree import Tree
from nltk.grammar import Production, Nonterminal
import os

def rhs_to_lhs_mapping(grammar): #returns a dictionary
	rhs_map = {}
	for prod in grammar.productions():
		element = prod.rhs()
		if element in rhs_map.keys() and (prod.lhs() not in rhs_map[element]):
			rhs_map[element].append(prod.lhs())
			
		else:
			rhs_map[element]=[prod.lhs()]
	return rhs_map

def fill_leaf_nodes(table,grammar,words,rhs_map):
	for i in range(len(words)):	#just diagonal needed so only one loop
		for ele in rhs_map[(words[i],)]:	#possible pos tags for a terminal
			table[i][i].append(Tree(ele,[words[i]]))
	return table

def cky_parse(table, grammar, words, rhs_map): # returns parse table
	size = len(words)
	for j in range(1,size):
		for i in range(j-1,-1,-1):
			for k in range(i,j):

				left_opt = table[i][k]
				right_opt = table[k+1][j]
				for ele1 in left_opt:
					for ele2 in right_opt:
						if (ele1.label(), ele2.label()) in rhs_map.keys():
							possible_prods = rhs_map[(ele1.label(),ele2.label())]
							for lhs in possible_prods: #for ex Nom & NP both have the same rhs
								table[i][j].append(Tree(lhs, [ele1,ele2]))	#tree with left and right child node
	return table

gr1 = nltk.data.load("file://"+sys.argv[1], 'text')
gr1 = nltk.grammar.CFG.fromstring(gr1)
#map from rhs to lhs needed? yes
rhs_mapping = rhs_to_lhs_mapping(gr1)

f=open(sys.argv[2],"r")
sentences = f.readlines()
f.close()

f=open(sys.argv[3],"w+")

for sent in sentences:
	f.write(sent)
	words = nltk.word_tokenize(sent.strip())
	size = len(words)
	table = [ [ [] for i in range(size)] for j in range(size)]
	table = fill_leaf_nodes(table,gr1,words,rhs_mapping)
	table=cky_parse(table,gr1,words,rhs_mapping)
	valid_parses = []
	for ele in table[0][size-1]:
		if str(ele.label()) == str(gr1.start()):
			valid_parses.append(ele)
			f.write(str(ele)+"\n")
	f.write("Number of parses: "+str(len(valid_parses))+"\n\n")

f.close()
	
