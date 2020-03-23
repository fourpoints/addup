import xml.etree.ElementTree as ET

# inline level elements
INLINE = {
	"a", "abbr", "acronym", "b", "bdo", "big", "br", "button", "cite", "code",
	"dfn", "em", "i", "img", "input", "kbd", "label", "map", "object", "q",
	"samp", "script", "select", "small", "span", "strong", "sub", "sup",
	"textarea", "time", "tt", "var", "math"
}

# block level elements with inline printing
ENDINLINE = {
	"pre", "mi", "mn", "mo", "ms", "mglyph", "mspace", "mtext", "h1", "h2",
	"h3", "h4", "h5", "h6", "title"
}

# block level elements that optionally have closing tags
OPTIONAL = {
	"body", "colgroup", "dd", "dt", "head", "html", "li", "option", "p",
	"tbody", "td", "tfoot", "th", "thead", "tr"
}

# block level elements that disallow closing tags (self-closing)
SELFCLOSE = {
	"area", "base", "basefont", "br", "col", "frame", "hr", "img", "input",
	"link", "meta", "param", "mprescripts", "none", "mspace",
}

# Math Markup Language elements
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

# Extensible Markup Language elements
# mostly special MML-elements (selc-closing) that require xml-style <el/> instead of <el>
XML = {
	"mspace", "mprescripts", "none"
}



# html writer
def htmlprinter(file, root, compact=True, doctype="html"):
	if doctype: file.write(f"<!DOCTYPE {doctype}>")

	for subtree in root:
		# for readability
		if compact:
			treeprinter(file, subtree, level=0, nl="", tab="")

		# for compactness
		else:
			treeprinter(file, subtree, level=0, nl="\n", tab="  ")

# sample writer
def treeprinter(file, tree, level, nl, tab):
	if tree.tag not in INLINE: file.write(nl+level*tab)

	# semi-redundant: adds newlien if math is displaystyled (depends on child)
	try:
		if tree.tag == "math" and tree[0].tag == "mtable" and tree[0].get("displaystyle", False):file.write(nl + level*tab)
	except IndexError:
		print("<math> element without children encountered.")

	if tree.tag is ET.Comment:
		file.write(f"<!--")
	else:
		file.write(f"<{tree.tag}")
		for attribute, value in tree.attrib.items():
			if isinstance(value, list):
				file.write(f' {attribute}="{" ".join(value)}"')
			else:
				file.write(f' {attribute}="{value}"')
		if tree.tag in XML:
			file.write("/>") # xml compliance for mathml
		else:
			file.write(">")

	# content
	if tree.text:
		lines = tree.text.splitlines()
		file.write(lines[0])
		if tree.tag == "pre" or tree.tag == "table" and "pyg-table" in tree.attrib.get("class", ""):
			for line in lines[1:]:
				# print(1, line)
				file.write('\n' + line) # nl?
		else:
			for line in lines[1:]:
				file.write(nl + level*tab + line)

	# subtree recursion
	if tree:
		for subtree in tree:
			if subtree.tag == "pre" or subtree.tag == "table" and "pyg-table" in subtree.get("class", ""):
				treeprinter(file, subtree, level=0, nl=nl, tab=tab)
			else:
				treeprinter(file, subtree, level=level+1, nl=nl, tab=tab)

	# closing tag
	if tree.tag not in INLINE | ENDINLINE:
		file.write(nl + level*tab)
	if tree.tag not in SELFCLOSE:
		if tree.tag is ET.Comment:
			file.write("-->")
		else:
			file.write(f"</{tree.tag}>")

	# tail
	if tree.tail:
		lines = tree.tail.splitlines()
		file.write(lines[0])
		for line in lines[1:]:
			file.write(nl + level*tab + line)
