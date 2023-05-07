import sys
import nltk
from nltk.tree import Tree
from nltk.grammar import Production, Nonterminal, CFG, PCFG
import os
import re
# now need to use PCFG to do PCKY

class PCKY:
	def __init__(self,gr):
		self.grammar = gr
		self.rhs_map = {}

	
	def rhs_to_lhs_mapping(self): #returns a dictionary
		self.rhs_map = {}
		for prod in self.grammar.productions():
			element = prod.rhs()
			if element in self.rhs_map.keys() and ([prod.lhs(),prod.prob()] not in self.rhs_map[element]):
				self.rhs_map[element].append([prod.lhs(),prod.prob()])
				
			else:
				self.rhs_map[element]=[[prod.lhs(),prod.prob()]]
		#print(self.rhs_map)
		return self.rhs_map


	def fill_leaf_nodes(self,table,words):
		for i in range(len(words)):	#just diagonal needed so only one loop
			if (words[i],) in self.rhs_map.keys():
				for ele in self.rhs_map[(words[i],)]:	#possible pos tags for a terminal
					#print(ele)
					table[i][i].append(Tree(ele,[words[i]]))
			else: #here unk is just like a placeholder
				ele = [Nonterminal('<UNK>'),0]
				table[i][i] = [Tree(ele,[words[i]])]
		return table

	

	def pcky_parse(self,table, words): # returns parse table
		size = len(words)
		for j in range(1,size):
			for i in range(j-1,-1,-1):
				for k in range(i,j):

					left_opt = table[i][k]
					right_opt = table[k+1][j]
					for ele1 in left_opt:
						for ele2 in right_opt:
							#print(ele1)
							#print()
							#print(ele2)
							if (ele1.label()[0], ele2.label()[0]) in self.rhs_map.keys():
								possible_prods = self.rhs_map[(ele1.label()[0],ele2.label()[0])]
								for ele in possible_prods: #for ex Nom & NP both have the same rhs
									ele_p = ele[1] * ele1.label()[1] * ele2.label()[1]
									table[i][j].append(Tree(ele, [ele1,ele2]))	#tree with left and right child node
		return table
	
if __name__ == "__main__":
	gr1 = nltk.data.load("file:///"+os.path.abspath(sys.argv[1]), 'text')
	gr1 = PCFG.fromstring(gr1)
	#map from rhs to lhs needed? yes
	obj = PCKY(gr1)
	obj.rhs_map = obj.rhs_to_lhs_mapping()
	#print("rhs map")
	#print(obj.rhs_map)

	f=open(sys.argv[2],"r")
	sentences = f.readlines()
	f.close()

	f=open(sys.argv[3],"w+")

	for sent in sentences:
		#f.write(sent)
		words = nltk.word_tokenize(sent.strip())
		size = len(words)
		table = [ [ [] for i in range(size)] for j in range(size)]
		table = obj.fill_leaf_nodes(table,words)
		#print(table)
		table = obj.pcky_parse(table,words)
		#print(table)
		#last_ele = table[0][size-1]
		#og_parse = str(last_ele)
		#new_parse = re.sub(", (([0-9]*[.])?[0-9]+)*\]", "",og_parse)

		parses = table[0][size-1]

		valid_parses = []
		for parse in parses:
			if parse.label()[0] == gr1.start():
				valid_parses.append(parse)
		if len(valid_parses) != 0:
			high_prob_parse = valid_parses[0]
			for parse in valid_parses:
				if parse.label()[1] > high_prob_parse.label()[1]:
					high_prob_parse = parse
			
			og_parse = str(high_prob_parse)
			new_parse = re.sub(", ([0-9]*[.])?[0-9]+(e-)?[0-9]*", "",og_parse)
			new_parse = re.sub("\[|\]","",new_parse)
			new_parse = re.sub("\n","",new_parse)
			new_parse = re.sub('\s{2,}', ' ',new_parse)
			new_parse = re.sub(" \)",")",new_parse)
			f.write(new_parse+"\n")
			
		else:
			f.write("\n")

	f.close()
	
