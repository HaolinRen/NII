import datetime
import operator
import json
from translation import bing
import os

base = "/Users/brenoust/Google Drive/StageRecherche_REN/SeaCove/Web/client/data/"
base= "/Users/brenoust/Google Drive/StageRecherche_REN/"
data_file = base+"SeaCove/Web/server/data (1)/topic_to_persons.json"
keyword_path = "/work/NII/news/topicseg/goolabs/keywords/"
trans_keyword_path = "/work/NII/news/topicseg/goolabs/keywords_translate/"
translated_dict_path = "/work/NII/news/topicseg/goolabs/keywords_translate/translated_dict.json"
old_translated_dict_path = "/work/NII/topicalAnalysis/dict/jp_en_kw.json"

output_file = base+"topic_to_persons_kw-all.json"
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

topic_info  = json.load(open(base+"SeaCove/Web/server/data (1)/date_to_topics.json"))
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

topicjson_file = base+"subtopics-all.json"
json.dump(subset_topic_info, open(topicjson_file,'w'), indent=True)


js_file = base+"topic_info-all.js"
with open(topicjson_file) as infile:
	text = 'local_topic_info ='+infile.read()
	with open(js_file, 'w') as outfile:
		outfile.write(text)


js_file = base+"topic_to_persons-all.js"
with open(output_file) as infile:
	text = 'local_fd_data ='+infile.read()
	with open(js_file, 'w') as outfile:
		outfile.write(text)

def getTopicContentByLine(filename, topic_boundaries):
	local_xm_path = '/work/NII/news/topicseg//nlp/experiment/xm/'
	topic_to_lines = {}

	with open(local_xm_path+'/'+filename+'.xm', 'r') as f:
		for line in f:
			#print chardet.detect(f.readline())
			unicodeline = line.decode('SHIFT_JIS')
			tokens = [t.strip() for t in unicodeline.split(' ')]
			dt = datetime.datetime.strptime(tokens[1], "%H:%M:%S")#.strftime("%H:%M:%S")
			delta = datetime.timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)

			topic = check_topic(delta, topic_boundaries)

			if topic not in topic_to_lines:
				topic_to_lines[topic] = []

			topic_to_lines[topic].append(tokens[3])

	return topic_to_lines

def check_topic(time, topics):
	current_topic = 0
	for t in sorted(topics):
		current_topic = t
		boundaries = topics[t]
		if time < boundaries[0]:
			return current_topic - .5
		if time < boundaries[1]:
			return current_topic
	return current_topic + .5


def getTopicBoundaries(filename):
	local_seg_path = '/work/NII/news/topicseg/nlp/experiment/seg'
	topic_boundaries = {}
	
	with open(local_seg_path+'/'+filename+'.seg', 'r') as f:
		for line in f:
			topics = [int(t.strip()) for t in line.split(';')]
			topic_boundaries[topics[0]] = [datetime.timedelta(seconds=x) for x in topics[1:3]] 
	
	return topic_boundaries


#captions = "/work/NII/news/topicseg/nlp/experiment/xm/"
big_dict = {}
for date in subset_topic_info.keys()[0:]:
	boundaries = []
	all_boundaries = getTopicBoundaries(date)
	big_dict[date] = getTopicContentByLine(date, all_boundaries)

json.dump(big_dict, open(base+"SeaCove/Web/server/data (1)/date_to_topics_to_captions.json",'w'), indent=True)

	#for t in subset_topic_info[date]:
	#	boundaries.append([subset_topic_info[date][t]['begin_sec'],subset_topic_info[date][t]['end_sec']])
	#print boundaries


