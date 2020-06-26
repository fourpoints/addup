#!/usr/bin/python -i
"""
File info
"""

try:
	from treebuilder import treebuilder
	from treemodifier import treemodifier
	from treeprinter import htmlprinter
except ImportError:
	from .treebuilder import treebuilder
	from .treemodifier import treemodifier
	from .treeprinter import htmlprinter

def addup(**options):

	### LOAD EXTENSIONS
	#extensions = options.get("extension")
	NotImplemented

	### PRE-PROCESSING
	NotImplemented

	### BUILD TREE
	ifile = options.get("infile")
	root = treebuilder(ifile)

	### POST-PROCESSING
	root = treemodifier(root)

	### PRINT ELEMENTTREE TO FILE
	ofile = options.get("outfile")
	with open(ofile, mode="w", encoding="utf-8") as file:
		# import sys; file = sys.stdout # For testing
		htmlprinter(file, root,
			compact = options.get("pretty"),
			doctype = root.get("type"),
		)



if __name__ == "__main__":
	addup(infile = "tests/site.add", outfile = "tests/site.html", extension =[])
