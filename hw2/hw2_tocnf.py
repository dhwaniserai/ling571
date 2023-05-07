import nltk
import sys
from nltk.grammar import *
import os
# nltk grammar data structure

#gr1 = nltk.data.load("grammars/large_grammars/atis.cfg")
#print(sys.argv[1])
gr1 = nltk.data.load("file://"+sys.argv[1])
#print(gr1.productions())
#print(gr1.productions()[0].lhs())
#print(gr1.productions()[0].rhs())
#print(gr1.productions()[-1])
#print(gr1.productions()[-1].lhs())
#print(gr1.productions()[-1].rhs())
#print(gr1.is_chomsky_normal_form())

def remove_hybrid(grammar): ##no hybrid for atis??
	new_rules=[]
	for prod in grammar.productions():
		if (len(prod.rhs())>1) and nltk.grammar.is_terminal(prod.rhs()[0]):
			new_term = str(prod.rhs()[0]).replace(" ","_")
			new_term = new_term.replace("'","")
			new_rule = Production(Nonterminal(new_term),[prod.rhs()[0]])
			new_rhs = [Nonterminal(new_term),prod.rhs()[1]]
			print("rhs",prod.rhs())
			mod_rule = Production(prod.lhs(),new_rhs)
			new_rules.append(mod_rule)
			new_rules.append(new_rule)
		else:
			new_rules.append(prod)
	return nltk.grammar.CFG(grammar.start(),new_rules)		
	#print("Hybrid",prod)

def remove_unitprods(grammar):
	unit_prods = []
	leftover = []
	new_grammar = []
	for prod in grammar.productions():
		if len(prod.rhs())==1 and prod.is_nonlexical():
			unit_prods.append(prod)
		else:
			leftover.append(prod)
	for un in unit_prods:
		un_lhs = str(un.lhs())
		un_rhs = str(un.rhs()[0])
		for i in range(len(leftover)):
			#check for lexicons
			rule = str(leftover[i]).split()
			if un_lhs in rule:
				rule[rule.index(un_lhs)] = un_rhs
			if un_lhs in rule:
                                rule[rule.index(un_lhs)] = un_rhs
			leftover[i]=" ".join(rule)
	new_grammar=nltk.CFG.fromstring('\n'.join(leftover))

			
	return new_grammar

def remove_longprods(grammar):
	long_prods = []
	leftover = []
	new_grammar = []
	for prod in grammar.productions():
		if len(prod.rhs()) > 2 :
			long_prods.append(prod)
		else:
			leftover.append(prod)
	for prod in long_prods: #for more than 3 non-terminals??
		prod_lhs = str(prod.lhs())
		prod_rhs = str(prod.rhs())
		pivot = prod.rhs()[1]
		str_pivot = str(pivot)
		#print("lhs",prod_lhs,"rhs",prod_rhs,"pivot",pivot)
		pivot_n = Nonterminal((str_pivot+str_pivot[-1]).upper()) #new notation by repeating last letter
		#print("newp",pivot_n)
		new_rule = Production(pivot_n,prod.rhs()[1:])
		mod_prod_rhs = Production(prod.lhs(),[prod.rhs()[0], pivot_n])
		#print(mod_prod_rhs)
		#print(new_rule)
		leftover.extend([mod_prod_rhs,new_rule])
	return nltk.CFG(grammar.start(),leftover)

new_gr1=remove_unitprods(gr1)
new_gr2=remove_longprods(new_gr1)
#print(new_gr2)
new_gr3 = remove_hybrid(new_gr2)
#with open(sys.argv[2],"w") as f:
#	prods = new_gr3.productions()
#	str_prods = [str(prod) for prod in prods]
#	f.write("\n".join(str_prods))
with open(sys.argv[2], 'w+') as f:
	f.write('{0}start {1}\n'.format('%', str(new_gr3.start())))
	for prod in new_gr3.productions():
		f.write(str(prod) + '\n')

print(new_gr3.is_chomsky_normal_form())

