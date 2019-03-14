#!/usr/bin/python -i
"""
File info
"""

from treebuilder import treebuilder
import xml.etree.ElementTree as ET

PRESETS = {"simple"}

def presetbuilder(preset):
	# HACK: __file__ returns module path
	from pathlib import Path
	dir = Path(__file__).parent / "presets"

	preset_file = dir / f"{preset}.add"
	preset_root = treebuilder(preset_file, dir)

	return preset_root

def wrap(root, preset, name):
	"""Inserts root into preset"""

	# Find insertion point
	wrapper = filter(lambda e:'add' in e.attrib, preset.iter()).__next__()
	wrapper.attrib.pop('add') # remove attrib

	# Insert root into preset
	for element in root: wrapper.append(element)

	# Find title element
	title = filter(lambda e:'title'==e.tag, preset.iter()).__next__()
	title.text = name

	return preset

def addup(**options):

	### LOAD EXTENSIONS
	#extensions = options.get("extension")
	NotImplemented

	### PRE-PROCESSING
	NotImplemented

	### BUILD TREE
	ifile = options.get("infile")
	root = treebuilder(ifile, dir=options.get("dir"))

	doctype = root.get("doctype")
	if root.get("doctype") in PRESETS:
		preset = presetbuilder(doctype)
		root = wrap(root, preset, options.get("name"))

	### POST-PROCESSING
	NotImplemented

	### PRINT ELEMENTTREE TO FILE
	### NOT NECESSARILY HUMAN-READABLE OUTPUT DEPENDING ON PARAMETERS
	ofile = options.get("outfile")
	with open(ofile, mode="w", encoding="utf-8") as file:
		if doctype:
			file.write("<!DOCTYPE html>")
		for subtree in root:
			#writer(file, subtree, level=0, nl='\n', tab=' ')
			writer(file, subtree, level=0, nl='', tab='') #for compact file


INLINE = {
	"a", "abbr", "acronym", "b", "bdo", "big", "br", "button", "cite", "code",
	"dfn", "em", "i", "img", "input", "kbd", "label", "map", "object", "q",
	"samp", "script", "select", "small", "span", "strong", "sub", "sup",
	"textarea", "time", "tt", "var", "math"
}

ENDINLINE = {
	"pre", "mi", "mn", "mo", "ms", "mglyph", "mspace", "mtext", "h1", "h2",
	"h3", "h4", "h5", "h6", "title"
}

OPTIONAL = {
	"body", "colgroup", "dd", "dt", "head", "html", "li", "option", "p",
	"tbody", "td", "tfoot", "th", "thead", "tr"
}

SELFCLOSE = {
	"area", "base", "basefont", "br", "col", "frame", "hr", "img", "input",
	"link", "meta", "param", "mprescripts", "none", "mspace",
}

MML = {
	"math", "maction", "maligngroup", "malignmark", "menclose", "merror",
	"mfenced", "mfrac", "mglyph", "mi", "mlabeledtr", "mlongdiv",
	"mmultiscripts", "mn", "mo", "mover", "mpadded", "mphantom", "mroot",
	"mrow", "ms", "mscarries", "mscarry", "msgroup", "mstack", #?
	"mlongdiv","msline", "mspace", "msqrt", "msrow", "mstack", "mstyle",
	"msub", "msub", "msup", "msubsup", "mtable", "mtd", "mtext", "mtr",
	"munder", "munderover", "semantics", "annotation", "annotation-xml",
	"mprescripts", "none"
}

XML = {
	"mspace", "mprescripts", "none"
}

# sample writer
def writer(file, tree, level, nl, tab):
	if tree.tag not in INLINE: file.write(nl+level*tab)

	# semi-redundant: adds newlien if math is displaystyled (depends on child)
	if tree.tag == "math" and tree[0].tag == "mtable" and tree[0].get("displaystyle", False): file.write(nl+level*tab)

	if tree.tag is ET.Comment:
		file.write(f"<!--")
	else:
		file.write(f"<{tree.tag}")
		for attribute, value in tree.attrib.items():
			file.write(f' {attribute}="{value}"')
		if tree.tag in XML:
			file.write("/>") #xml compliance for mathml
		else:
			file.write(">")

	#content
	if tree.text:
		lines = tree.text.splitlines()
		file.write(lines[0])
		if tree.tag == "pre" or tree.tag == "table" and "highlighttable" in tree.attrib.get("class", ""):
			for line in lines[1:]:
				#print(1, line)
				file.write('\n' + line) # nl?
		else:
			for line in lines[1:]:
				file.write(nl + level*tab + line)

	#subtree
	if tree:
		for subtree in tree:
			if subtree.tag == "pre" or subtree.tag == "table" and "highlighttable" in subtree.get("class", ""):
				writer(file, subtree, level=0, nl=nl, tab=tab)
			else:
				writer(file, subtree, level=level+1, nl=nl, tab=tab)

	#closing tag
	if tree.tag not in INLINE | ENDINLINE:
		file.write(nl + level*tab)
	if tree.tag not in SELFCLOSE:
		if tree.tag is ET.Comment:
			file.write("-->")
		else:
			file.write(f"</{tree.tag}>")

	#tail
	if tree.tail:
		lines = tree.tail.splitlines()
		file.write(lines[0])
		for line in lines[1:]:
			file.write(nl + level*tab + line)

if __name__ == "__main__":
	addup(infile = "tests/site.add", outfile = "tests/site.html", extension =[])
