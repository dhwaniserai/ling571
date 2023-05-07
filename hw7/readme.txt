Ling 571 hw7
@Author Dhwani Serai

Brown corpus reading format:
I have used brown corpus words(brown.words()) format as my dataset which does not distinguish between individual sentences in the dataset and it is a continuous sliding window over the whole dataset

Preprocessing: I have lowercased all words and removed punctuations(even from within the words)

Part 1:
For creating a cooccurence matrix I have used the coordinate format in scipy. Whenever a word is encountered as a cooccurence it is added as a entry in the matrix. Then using that I convert it to a sparse matrix and later into a dense form which will be of shape vocab x vocab.

Output analysis:
For freq weights the top10 most similar words were mostly 'the' 'has' 'an' which do not necessarily give proper context

For PMI weight form there were more meaningful words in the top10 most similar words.

For window_size: As we increase the window_size the number of relevant words in the top10 values increases. Like in PMI calculation for sliding window 2 the word 'stove' still has some random context words in it's top 10 values like 'republicans' but for sliding window 10 all the words in top 10 are very relevant to the word stove

For quality of model:
Word2vec performs better than both freq and pmi based counts because for the given judgements 'car' and 'automobile' or 'magic' and 'wizard' have a much higher similarity score than freq or pmi. So, it gives a better prediction about contextually relevant words.
