import sys
import nltk
f=open(sys.argv[1],"r")
cfg = nltk.data.load("file:"+sys.argv[1])
ec_parser = nltk.parse.EarleyChartParser(cfg)
f.close()
f=open(sys.argv[2],"r")
sentences = f.read().strip().split('\n')
n_sent, n_parse = len(sentences), 0.0
f.close()
f=open(sys.argv[3],"w")
for sent in sentences:
	f.write(sent+"\n")
	sent = nltk.word_tokenize(sent)
	n_sent_parse = 0.0
	try:
		for tree in ec_parser.parse_all(sent):
			f.write(str(tree)+"\n")
			n_sent_parse += 1.0
		n_parse += n_sent_parse
	except:
		f.write("\n")
	f.write("Number of parses: "+str(n_sent_parse)+"\n\n")

f.write("Average number of parses per sentence: "+str(n_parse/n_sent))
