from flair.models import SequenceTagger
from flair.data import Sentence
from pprint import pprint
import re
import re
import spacy
from spacy.matcher import Matcher
nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)

def nname(resume_text):
    nlp_text = nlp(resume_text)
    
    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    
    matcher.add('NAME', None, [*pattern])
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text



def extract_name(resume_text):
	def namePos(subs,string):
		data = []
		for sub in subs:
			for m in re.finditer(sub,string):
				data.append(
					{
						"text" : sub,
						"start_pos" : m.start(),
						"end_pos" : m.end(),
						"type" : "mobile",
						"confidence" : 100.0
					}
				)
				break
		return data
	name = nname(resume_text)
	names = namePos([name],resume_text)
	return names
def mob_num_extractor(string):
	data = []
	def mobilePos(subs,string):
		data = []
		for sub in subs:
			for m in re.finditer(sub,string):
				data.append(
					{
						"text" : sub,
						"start_pos" : m.start(),
						"end_pos" : m.end(),
						"type" : "mobile",
						"confidence" : 100.0
					}
				)
		return data
	string = string.strip(' ')
	mob_num_format = re.compile(r'[-0-9+]{10,14}')
	mob_num_list = mob_num_format.findall(string)
	not_number = []
	for count in range(len(mob_num_list)):
		if len(mob_num_list[count])  > 10:
			if '+91' in mob_num_list[count]:
				mob_num_list[count] = mob_num_list[count].replace('+91','')
				if '-' in mob_num_list[count]:
					mob_num_list[count] = mob_num_list[count].replace('-','')
				if len(mob_num_list[count]) != 10:
					not_number.append(mob_num_list[count])
			else:
				not_number.append(mob_num_list[count])
		elif len(mob_num_list[count]) < 10:
			not_number.append(mob_num_list[count])
	
	for del_me in not_number:
		if del_me in mob_num_list:
			mob_num_list.remove(del_me)
	del not_number
	data = mobilePos(list(set(mob_num_list)),string)
	return data
def find_emails(string):
	data = []
	def emailPos(subs,string):
		data = []
		for sub in subs:
			for m in re.finditer(sub,string):
				data.append(
					{
						"text" : sub,
						"start_pos" : m.start(),
						"end_pos" : m.end(),
						"type" : "email",
						"confidence" : 100.0
					}
				)
		return data
	searchforEmails = re.compile(r'[A-Za-z0-9._%*+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
	EmailList = searchforEmails.findall(string)

	data = emailPos(list(set(EmailList)),string)
	return data


def Resume(text):
	text = ' '.join([line.replace('\t', ' ') for line in text.split('\n') if line])
	data = {
		'content' : text,
		'person'  : {
			'count' : 0,
			'source' : [],
		},
		'location' : {
			'count' : 0,
			'source' : []
		},
		'organization' : {
			'count' : 0,
			'source' : []
		},
		'emails' : {
			'count' : 0,
			'source' : []
		},
		'mobiles' : {
			'count' : 0,
			'source' : []
		}
	}
	
	emails = find_emails(text)
	mobiles = mob_num_extractor(text)
	persons = extract_name(text)
	#print(persons)
	for email in emails:
			data["emails"]["count"]+=1
			data["emails"]["source"].append(email)
	for mobile in mobiles:
		data["mobiles"]["count"]+=1
		data["mobiles"]["source"].append(mobile)
	for person in persons:
		data["person"]["count"]+=1
		data["person"]["source"].append(person)

	sentence = Sentence(text)
	model = SequenceTagger.load('/media/zeus/AREA_51/MY_WORKS/API/mods/eng_cpu.pt')
	model.predict(sentence)
	d = sentence.to_dict(tag_type='ner')
	for item in d['entities']:
		if item["type"] == "PER" and item['confidence']>0.70:
			data["person"]["count"]+=1
			data["person"]["source"].append(item)
		elif item["type"] == "LOC" and item['confidence']>0.60:
			data["location"]["count"]+=1
			data["location"]["source"].append(item)
		elif item["type"] == "ORG" and item['confidence']>0.95:
			data["organization"]["count"]+=1
			data["organization"]["source"].append(item)
	return data