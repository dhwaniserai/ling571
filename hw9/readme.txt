Ling 571 HW 9
Author: Dhwani Serai (dserai)

for this discourse parsing assignment we have used Glove embeddings for making the vector representaation of a given argument in a relation.
Glove is basically a lookup table which gives a embedding vector for one sense of a word.
1. Getting embeddings for a relation
First, I get the raw_text of the argument, tokenize it and then use glove for embeddings of individual words in the text(size 100). If the token is not in glove then I add a zero embedding vector.
I get the mean vector along axis=0 to get mean values for all features in the embeddings of all words.
I repeat the same for the raw text of Arg2, then concatenate those individual vectors.
This is the X part of training a classifier
For getting the Y part I use the first part of the first Sense as the label.
In the future I could maybe try using the same embeddings for different Senses of the relation to see if there is any improvement. I don't think that it would improve by a lot because if the sense is different then the embedding vector of the relation should also be different. If the embeddings were context based then I guess using different senses would improve the model.

2. Training a classifier:
I have trained on SVM classifier which is trained on the above embedding vector and Sense value as the prediction.

3. Interpretation:
Interestingly, the label which has the lowest number of examples in the training data(Contingency) has the maximum f1_score in the SVM model (0.57). The label with second least training examples(~2700) has the second best f1_score(Temporal;0.47). The label with the maximum examples in training has the third best f1_score(0.42) (for Expansion).
Comparison has the lowest f1_score(0.14) despite having 4000 examples in the training data.

Yay! done with the last homework of the course