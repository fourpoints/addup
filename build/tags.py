import json
import langs

def getlang(tag):
	tag = tag.lower()
	if tag in HTML5:
		if tag == "pre":
			return getattr(langs, "Pre")
		elif tag == "script":
			return getattr(langs, "Script")
		elif tag == "style":
			return getattr(langs, "CSS")
		else:
			return getattr(langs, "HTML")

	elif tag in CUSTOM:
		return getattr(langs, "Custom")
		
	elif tag == 'eqn':
		return getattr(langs, "Jax")
	
	else:
		print(f"{tag} is not a tag")
		
def is_selfclosing(tag):
	tag = tag.lower()
	if tag in SELFCLOSING:
		return True
	else:
		return False

## Custom

with open("custom_tags.json") as custom_tags:
	CUSTOM = json.load(custom_tags)

def tag(tag):
	return CUSTOM[tag][0].get("html5tag")

def attributes(tag):
	try:
		return CUSTOM[tag][0].get("attributes").copy()
	except AttributeError:
		return False

def parser(tag):
	return CUSTOM[tag][0].get("parser")

## HTML5

with open("html5.json") as html5_tags:
	HTML = json.load(html5_tags)
	HTML5 = HTML["HTML5"]
	SELFCLOSING = HTML["SELFCLOSING"]