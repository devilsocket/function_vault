from flair.models import SequenceTagger
from flair.data import Sentence
from pprint import pprint
import re

def nerUrduName(txt):
	def spl(i):
		return i.split()[-1]
	data = {"tags" : []}
	sentence = Sentence(txt)
	model = SequenceTagger.load('/media/zeus/AREA_51/MY_WORKS/API/mods/checkpoint.pt')
	model.predict(sentence)
	data["tagged_string"] = sentence.to_tagged_string()
	for entity in sentence.get_spans('ner'):
		temp = entity.__dict__
		for item in temp["tokens"]:
			temp = item.__dict__
			temp1 = temp["tags"]["ner"].__dict__
			d = {
				"text" : temp["text"],
				"start_pos" : temp["start_pos"],
				"end_pos" : temp["end_pos"],
				"ner" : temp1["_value"],
				"confidence" : temp1["_score"]
			}
			data["tags"].append(d)
	return data

def nerEnglish(txt):
	data = {
		'content' : txt,
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
	try:
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
		sentence = Sentence(txt)
		emails = find_emails(txt)
		mobiles = mob_num_extractor(txt)
		model = SequenceTagger.load('/media/zeus/AREA_51/MY_WORKS/API/mods/eng_cpu.pt')
		model.predict(sentence)
		d = sentence.to_dict(tag_type='ner')
		for item in d['entities']:
			if item["type"] == "PER":
				data["person"]["count"]+=1
				data["person"]["source"].append(item)
			elif item["type"] == "LOC":
				data["location"]["count"]+=1
				data["location"]["source"].append(item)
			elif item["type"] == "ORG":
				data["organization"]["count"]+=1
				data["organization"]["source"].append(item)
		for email in emails:
			data["emails"]["count"]+=1
			data["emails"]["source"].append(email)
		for mobile in mobiles:
			data["mobiles"]["count"]+=1
			data["mobiles"]["source"].append(mobile)
	except:pass
	return data


def nerUrdu(txt):
	data = {
		'content' : txt,
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
	try:
		def find_emails(string):
			searchforEmails = re.compile(r'[A-Za-z0-9._%*+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
			EmailList = searchforEmails.findall(string)
			return EmailList
		def mob_num_extractor(string):
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
			return mob_num_list
		sentence = Sentence(txt)
		emails = find_emails(txt)
		mobiles = mob_num_extractor(txt)
		model = SequenceTagger.load('/media/zeus/AREA_51/MY_WORKS/API/mods/urdu_ner.pt')
		model.predict(sentence)
		d = sentence.to_dict(tag_type='ner')
		for item in d['entities']:
			if item["type"] == "PER":
				data["person"]["count"]+=1
				data["person"]["source"].append(item)
			elif item["type"] == "LOC":
				data["location"]["count"]+=1
				data["location"]["source"].append(item)
			elif item["type"] == "ORG":
				data["organization"]["count"]+=1
				data["organization"]["source"].append(item)
		for email in emails:
			data["emails"]["count"]+=1
			data["emails"]["source"].append(email)
		for mobile in mobiles:
			data["mobiles"]["count"]+=1
			data["mobiles"]["source"].append(mobile)
	except:pass
	return data



#a = nerEnglish(
#"""
#sdf@gmail.com dfg@gmail.com 9439394132 9439394133. بتائیں کہ بالاکوٹ نے کس طرح ہندوستانی فوجی بحرانوں سے متعلق ہندوستانی خطوط کو تبدیل کیا 1987 کے بعد سے ہر فوجی بحران میں ، ہندوستان بہت احتیاط کے ساتھ گامزن ہوا جبکہ ایسا لگتا ہے کہ پاکستان اس کے برخلاف کام کرتا ہے۔ بھارت کے تازہ ترین ردعمل کے اشارے وہ سیکیورٹی سی سی ایس پر کابینہ کی کمیٹی کے اجلاس کے دوران بات چیت کرنے کے لئے وزیر دفاع نریندر مودی ، مرکزی وزیر داخلہ راجناتھ سنگھ ، وزیر برائے امور خارجہ سشما سوراج ، وزیر دفاع نرملا سیتارامن اور وزیر خزانہ ارون جیٹلی کے خلاف بات چیت کرنے کے لئے تیار ہیں۔ نئی دہلی میں پلوامہ دہشت گرد حملے کے بعد پیدا ہونے والی صورتحال۔ پی ٹی آئی فوٹو شروع میں ، ہندوستان اور پاکستان کے مابین سنہ 48 48 ، 19 19 1965 اور in 1971 in traditional میں روایتی جنگیں ہوئیں۔ گذشتہ تین دہائیوں کے دوران ، ہم نے 1987 ، 1990 ، 1999 ، 2001 ، 02 اور 2008 میں کئی فوجی بحرانوں کا سامنا کرنا پڑا۔ کچھ لوگوں نے باقاعدہ جنگ میں اڑانے کی دھمکی دی ، لیکن ایسا نہیں ہوا۔ گذشتہ ماہ سی آر پی ایف کے 40 جوانوں کو ہلاک کرنے والے کشمیر میں ہونے والے دہشت گردی کے واقعے نے ایک نئے فوجی بحران کی منزلیں طے کیں جس میں واقف طرز پر عمل کرنے کا وعدہ کیا گیا تھا۔ لیکن نئی دہلی نے اس سے مختلف ردعمل کا انتخاب کیا اس بار خیبر پختون خوا کے بالاکوٹ میں دہشت گردوں کے کیمپ پر ہندوستانی لڑاکا طیارے نے بم گرائے اور 1971 کے بعد پہلی بار پاک فضائیہ کو فضائی لڑائی میں مصروف کردیا۔
#"""
#)
#pprint(a)