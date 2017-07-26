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
		lang = CUSTOM[tag].get("lang")
		if lang == "HTML":
			lang = "CustomHTML"
		return getattr(langs, lang)
	
	else:
		return None
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

def get_tags_and_attributes_from_json(tag):
	return CUSTOM[tag].get("tags").copy()

def has_offset(tag):
	if CUSTOM[tag].get("offset") == "True":
		return True
	else:
		return False

## HTML5

with open("html5.json") as html5_tags:
	HTML = json.load(html5_tags)
	HTML5 = HTML["HTML5"]
	SELFCLOSING = HTML["SELFCLOSING"]