import json
from translation import bing
import os

data_file = "/Users/brenoust/Google Drive/StageRecherche_REN/SeaCove/Web/client/data/topic_to_persons.json"
keyword_path = "/work/NII/news/topicseg/goolabs/keywords/"
trans_keyword_path = "/work/NII/news/topicseg/goolabs/keywords_translate/"
translated_dict_path = "/work/NII/news/topicseg/goolabs/keywords_translate/translated_dict.json"
old_translated_dict_path = "/work/NII/topicalAnalysis/dict/jp_en_kw.json"

output_file = "/Users/brenoust/Google Drive/StageRecherche_REN/SeaCove/Web/client/data/topic_to_persons_kw-all.json"
translated_dict_path = old_translated_dict_path
topic_to_persons = json.load(open(data_file))
day2topic = {}
topic_subset = {}

'''
min_day = "2010_08_06"
max_day = "2011_09_02"
min_day = "2001_01_01"
max_day = "2006_09_26"
query = "Naoto KAN"
query = "Shinzo ABE"
'''
query = None
translated_dict = {}

if os.path.isfile(translated_dict_path):
	translated_dict = json.load(open(translated_dict_path))


if query:
	for k in topic_to_persons.keys():
		day,topic = k.split('-Topic')
		#print topic_to_persons[k]
		if day < min_day or day > max_day:
			continue
		if query not in topic_to_persons[k]:
			continue
		topic_subset[k] = topic_to_persons[k]
		if day not in day2topic:
			day2topic[day] = []
			day2topic[day].append(topic)

else:
	for k in topic_to_persons.keys():
		day,topic = k.split('-Topic')
		'''
		if day < min_day or day > max_day:
			continue
		'''
		topic_subset[k] = topic_to_persons[k]
		if day not in day2topic:
			day2topic[day] = []
			day2topic[day].append(topic)

limit = False

topic_info  = json.load(open("/Users/brenoust/Google Drive/StageRecherche_REN/SeaCove/Web/client/data/date_to_topics.json"))
subset_topic_info = {}

for d in day2topic:
	klist = json.load(open(keyword_path+d+".kw"))
	dayinfo = topic_info[d]
	if d not in subset_topic_info:
		subset_topic_info[d] = {}

	for t in day2topic[d]:
		tinfo = dayinfo[t]
		subset_topic_info[d][t] = tinfo

		kw = sorted(klist[t], key=lambda k: klist[t][k], reverse=True)
		enkw = []
		for k in kw:
			if k not in translated_dict:
				en = bing(k, src = 'ja', dst = 'en')
				translated_dict[k] = en
				json.dump(translated_dict, open(translated_dict_path, 'w'))
			enkw.append(translated_dict[k])

		if limit:
			topic_subset[d+'-Topic'+t].extend([kw[0]])
			if len(kw) > 1:
				topic_subset[d+'-Topic'+t].extend([kw[1]])
		else:
			topic_subset[d+'-Topic'+t].extend(enkw)



json.dump(topic_subset, open(output_file,'w'), indent=True)

topicjson_file = "/Users/brenoust/Google Drive/StageRecherche_REN/SeaCove/Web/client/data/subtopics-all.json"
json.dump(subset_topic_info, open(topicjson_file,'w'), indent=True)


js_file = "/Users/brenoust/Google Drive/StageRecherche_REN/SeaCove/Web/client/data/topic_info-all.js"
with open(topicjson_file) as infile:
	text = 'local_topic_info ='+infile.read()
	with open(js_file, 'w') as outfile:
		outfile.write(text)


js_file = "/Users/brenoust/Google Drive/StageRecherche_REN/SeaCove/Web/client/data/topic_to_persons-all.js"
with open(output_file) as infile:
	text = 'local_fd_data ='+infile.read()
	with open(js_file, 'w') as outfile:
		outfile.write(text)
