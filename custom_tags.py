TAGS = {
	"Section":
		{
			"html5tag"    : 'div',
			"attributes"  :
				{
					"class" : "section"
				}
		},
	
	"Q":
		{
			"html5tag"    : 'div',
			"attributes"  :
				{
					"class" : "sigma pi"
				}
		},
	
	"Math":
		{
			"html5tag"    : 'script',
			"attributes"  :
				{
					"type" : "math/tex"
				},
			"parser" : 'asis'
		},
	
	"Style":
		{
			"html5tag"    : 'script',
			"attributes"  :
				{
					"type" : "math/tex"
				},
			"parser" : 'asis'
		}
}

def tag(tag):
	return TAGS[tag].get("html5tag")

def attributes(tag):
	try:
		return TAGS[tag].get("attributes").copy()
	except AttributeError:
		return False

def parser(tag):
	return TAGS[tag].get("parser")