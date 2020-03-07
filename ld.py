import pycld2 as pcd

def languageDetector(input_text):
	res = pcd.detect(input_text)
	return res