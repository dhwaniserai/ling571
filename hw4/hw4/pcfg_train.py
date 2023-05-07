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
                count_prods[prod.lhs()] = {prod.rhs() : 1}
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
    #print(sys.argv)
    cfg_file = sys.argv[1]
    text = ''
    grammar = []
    with open(cfg_file,'r') as f:
        text = f.readlines()
    
    for parse in text:
        parse_tree = Tree.fromstring(parse)
        grammar.extend(parse_tree.productions())
    #grammar = CFG.fromstring(cfg)
    obj = PCFG_Induction(grammar)
    obj.pcfg = obj.tree_to_pcfg()
    #obj.pcfg = obj.cfg_to_pcfg()
    #print(obj.pcfg)
    pcfg_file = sys.argv[2]
    with open(pcfg_file,'w+') as f:
        f.write(obj.pcfg)
    new_pcfg = PCFG.fromstring(obj.pcfg)
    #print(new_pcfg)

