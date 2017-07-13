import json

with open("custom_tags.json") as custom_tags:
	TAGS = json.load(custom_tags)

def tag(tag):
	return TAGS[tag][0].get("html5tag")

def attributes(tag):
	try:
		return TAGS[tag][0].get("attributes").copy()
	except AttributeError:
		return False

def parser(tag):
	return TAGS[tag][0].get("parser")