#!/usr/bin/python -i
"""
File info
"""

from treebuilder import treebuilder
import xml.etree.cElementTree as et

def addup(**options):

	### LOAD EXTENSIONS
	#extensions = options.get("extension")
	NotImplemented

	### PRE-PROCESSING
	NotImplemented

	### BUILD TREE
	ifile = options.get("infile")
	with open(ifile, mode="r", encoding="utf-8") as file:
		text = file.read()

	root = treebuilder(text)

	### POST-PROCESSING
	NotImplemented

	### PRINT ELEMENTTREE TO FILE --- NOT HUMAN-READABLE OUTPUT
	ofile = options.get("outfile")
	with open(ofile, mode="w", encoding="utf-8") as file:
		if root.attrib.pop("doctype", False):
			file.write("<!DOCTYPE html>")
		for subtree in root:
			writer(file, subtree, -100)


INLINE = {"a", "abbr", "acronym", "b", "bdo", "big", "br", "button", "cite", "code", "dfn", "em", "i", "img", "input", "kbd", "label", "map", "object", "q", "samp", "script", "select", "small", "span", "strong", "sub", "sup", "textarea", "time", "tt", "var"}

OPTIONAL = {"body", "colgroup", "dd", "dt", "head", "html", "li", "option", "p", "tbody", "td", "tfoot", "th", "thead", "tr"}

SELFCLOSE = {"area", "base", "basefont", "br", "col", "frame", "hr", "img", "input", "link", "meta", "param"}

# sample writer
def writer(file, tree, level):
	if tree.tag not in INLINE: file.write("\n"+level*"\t")

	if tree.tag is et.Comment:
		file.write(f"<!--")
	else:
		file.write(f"<{tree.tag}")
		for attribute, value in tree.attrib.items():
			file.write(f' {attribute}="{value}"')
		file.write(">")

	#content
	if tree.text:
		lines = tree.text.splitlines()
		file.write(lines[0])
		if tree.tag != "pre":
			for line in lines[1:]:
				file.write("\n" + level*"\t" + line)
		else:
			for line in lines[1:]:
				print(line)
				file.write("\n" + line)

	#subtree
	if tree:
		for subtree in tree:
			if tree.tag != "pre": writer(file, subtree, level+1)
			else: writer(file, subtree, -100)

	#closing tag
	if tree.tag not in INLINE: file.write("\n" + level*"\t")
	if tree.tag not in SELFCLOSE:
		if tree.tag is et.Comment:
			file.write("-->")
		else:
			file.write(f"</{tree.tag}>")

	#tail
	if tree.tail:
		lines = tree.tail.splitlines()
		file.write(lines[0])
		for line in lines[1:]:
			file.write("\n" + level*"\t" + line)

if __name__ == "__main__":
	addup(infile = "tests/current.add", outfile = "tests/current.html", extension =[])
