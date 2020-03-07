from polyglot.transliteration import Transliterator
trans = Transliterator(source_lang="en", target_lang="ur")

def transliterationAnalyzerUrduOne(txt):
	default = {}
	default["result"]=' '.join(list(map(trans.transliterate,txt.split())))
	return default