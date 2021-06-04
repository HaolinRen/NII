import os
import json

path = "/work/NII/news/tlpxscripts/data/statistics/topic_to_persons.json"
topic_to_persons = json.load(open(path))
print sorted(topic_to_persons.keys())
print len(topic_to_persons)
#for topic in sorted(topic_to_persons):
#	print topic_to_persons[topic]
people = ([y for x in topic_to_persons.values() for y in x])
print len(people)
print len(set(people))

days = [p.split('-')[0] for p in topic_to_persons]
print len(set(days))

