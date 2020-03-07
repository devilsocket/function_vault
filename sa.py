from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

def sentimentAnalyzerOne(txt):
	default = {}
	res = analyser.polarity_scores(txt)
	score = res["compound"]
	default["polarity"]=score
	if score>0:default["sentiment"]="Positive"
	elif score<0:default["sentiment"]="Negative";
	else:default["sentiment"]="Neutral";
	return default