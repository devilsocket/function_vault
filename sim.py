from nltk.corpus import wordnet

def similar(inp):
	default = []
	try:default=list(set([item.lemmas()[0].name() for item in wordnet.synsets(inp)]))
	except:pass
	return default