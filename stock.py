# NSE TICKER
from urllib.request import build_opener, HTTPCookieProcessor, Request, urlopen
from urllib.parse import urlencode
from http.cookiejar import CookieJar
import six
import re
import json



def nseTicker(ticker):
	default = {}
	header= {
		'Accept': '*/*',
		'Accept-Language': 'en-US,en;q=0.5',
		'Host': 'nseindia.com',
		'Referer': "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=INFY&illiquid=0&smeFlag=0&itpFlag=0",
	    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
	    'X-Requested-With': 'XMLHttpRequest'
	}
	def clean_server_response(resp_dict):
	    d = {}
	    for key, value in resp_dict.items():
	        d[str(key)] = value
	    resp_dict = d
	    for key, value in resp_dict.items():
	        if type(value) is str or isinstance(value, six.string_types):
	            if re.match('-', value):
	                try:
	                    if float(value) or int(value):
	                        dataType = True
	                except ValueError:
	                    resp_dict[key] = None
	            elif re.search(r'^[0-9,.]+$', value):
	                # replace , to '', and type cast to int
	                resp_dict[key] = float(re.sub(',', '', value))
	            else:
	                resp_dict[key] = str(value)
	    return resp_dict
	try:
		code = ticker
		get_quote_url = 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?'
		encoded_args = urlencode([('symbol', code), ('illiquid', '0'), ('smeFlag', '0'), ('itpFlag', '0')])
		url_args = get_quote_url + encoded_args
		#print(url_args)
		req = Request(url_args, None, header)
		cj = CookieJar()
		res = build_opener(HTTPCookieProcessor(cj)).open(req)
		#print(res)
		strings = res.read().decode('latin-1')
		res = six.StringIO(strings)
		res = res.read()
		match = re.search(r'<div\s+id="responseDiv"\s+style="display:none">(.*?)</div>',res, re.S)
		buffer = match.group(1).strip()
		default = clean_server_response(json.loads(buffer)['data'][0])
	except:pass 
	return default