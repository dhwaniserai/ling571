##ling571 hw3 readme
# Author: Dhwani Serai (dserai)
# CKY parser implementation

#After loading the grammar from the file as a CFG I have created another dictionary to map the rhs to lhs instead of lhs->rhs to make the lookup process easier
#this is done in the rhs_to_lhs_mapping function

#for the cky parsing I have divided the parsing in two parts
1. Diagonal filling which is basically creating a list of pos tags for every token in the sentence. Since these will be leaf nodes in the parse trees with no children I have seperated it out. (filling_leaf_nodes function)

2. filling up the rest of the nodes in the table using the cky parsing algorithm and keeping track of the backpointers by using the tree data structure as the left and right child nodes.

## In the end checking for valid parses by using the nonterminals of the last element in the 0th row to see which ones match the start of the grammar. Printing the valid parses to the file using the tree formed at that nonterminal

#some issue with running the check_hw3.sh on my tar file. The files are there but patas says that it may be corrupted. I was able to unzip it in a different directory and it worked fine
#sorry for the trouble