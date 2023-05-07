import nltk
from nltk import PCFG, CFG, Tree
import sys

class PCFG_Induction:

    def __init__(self, grammar): #grammar in CFG form only
        self.grammar = grammar
        self.pcfg = ''


    def tree_to_pcfg(self):
        count_prods = {}
        for prod in self.grammar:
            if prod.lhs() in count_prods.keys():
                if prod.rhs() in count_prods[prod.lhs()].keys():
                    count_prods[prod.lhs()][prod.rhs()] += 1
                else:
                    count_prods[prod.lhs()][prod.rhs()] = 1
            else:
                #print(type(prod.rhs()))
                count_prods[prod.lhs()] = {prod.rhs() : 1}
        ###oov and removing some sparse rules
        unk_rules = []
        for lhs in count_prods.keys():
            lhs_count = sum(count_prods[lhs].values())
            for rhs in count_prods[lhs].keys():
                prob = count_prods[lhs][rhs] / lhs_count
                if prob <= 0.005 and len(rhs)==1:
                    unk_rules.append([lhs,rhs])
        # modify unk rules
        #unk_rules = unk_rules[:5]
        for rule in unk_rules:
            if ('<UNK>',) in count_prods[rule[0]].keys():
                count_prods[rule[0]][('<UNK>',)] += count_prods[rule[0]].pop(rule[1])
            else:
                count_prods[rule[0]][('<UNK>',)] = count_prods[rule[0]].pop(rule[1])#lhs
            

        pcfg_string = ""
        for lhs in count_prods.keys():
            lhs_count = sum(count_prods[lhs].values())
            for rhs in count_prods[lhs].keys():
                prob = count_prods[lhs][rhs] / lhs_count
                if len(rhs) != 1:
                    pcfg_string += str(lhs) + ' -> ' + """ """.join(map(str,rhs)) + ' [' + str(prob) + ']\n'
                else:
                    pcfg_string += str(lhs) + ' -> "' + rhs[0] + '" [' + str(prob) + "]\n"
        return pcfg_string

if __name__ == "__main__":
    
    cfg_file = sys.argv[1]
    text = ''
    grammar = []
    with open(cfg_file,'r') as f:
        text = f.readlines()
    
    for parse in text:
        parse_tree = Tree.fromstring(parse)
        grammar.extend(parse_tree.productions())
    obj = PCFG_Induction(grammar)
    obj.pcfg = obj.tree_to_pcfg()
    pcfg_file = sys.argv[2]
    with open(pcfg_file,'w+') as f:
        f.write(obj.pcfg)
    new_pcfg = PCFG.fromstring(obj.pcfg)
