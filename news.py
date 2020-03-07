B=dict
import urllib.request
from urllib.parse import urlencode as D
import xmltodict as E
def newsGoogle(txt):
	N='source';M='guid';C=[]
	try:
		F=D([('q',txt),('safe','strict'),('hl','en-US'),('gl','US'),('ceid','US:en')]);G='https://news.google.com/rss/search?';H=G+F;I=urllib.request.Request(H);J=urllib.request.urlopen(I);K=E.parse(J)['rss']['channel']['item']
		for L in K:A=B(L);A[M]=B(A[M]);A[N]=B(A[N]);C.append(A)
	except:pass
	return C

def newsYahooFinance():
	data = []
	try:
		res = urllib.request.urlopen("https://finance.yahoo.com/news/rss")
		d2 = E.parse(res.read())
		for v in d2['rss']['channel']['item']:
			del v['guid'], v['media:content'], v['media:text'], v['media:credit']
			v['source'] = B(v['source'])
			data.append(v)
	except:pass
	return data

def newsYahooFinanceTicker(ticker):
	data = []
	try:
		res = urllib.request.urlopen("https://feeds.finance.yahoo.com/rss/2.0/headline?"+D([('s',ticker)]))
		d1 = E.parse(res.read())
		for item in d1["rss"]["channel"]["item"]:
			del item['guid']
			data.append(B(item))
	except:pass
	return data