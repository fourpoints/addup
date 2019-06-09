import xml.etree.ElementTree as ET
import re

from pathlib import Path

try: # feels hacky
	from . import node
except ImportError:
	import node

# - [ ] improve pathstacking

### --------    --------    --------    --------


def get_base_path(base, local):
	from pathlib import Path

	# HACK: __file__ returns module path
	# actually nothing in here, cos setup ignores it
	default = Path(__file__).parent / "bases"

	L = set(map(lambda f: f.stem, Path(local).glob('*.add')))
	D = set(map(lambda f: f.stem, Path(default).glob('*.add')))

	if base in L: return Path(f"{local}/{base}.add")
	if base in D: return Path(f"{default}/{base}.add")

	print("Base not found. Extending failed.")
	return ""


def get_wrap_node(base):
	"""gets the wrapping node"""

	# Find insertion point
	wrap = filter(lambda e: 'add' in e.attrib, base.iter()).__next__()
	wrap.attrib.pop('add')

	return wrap


def get_type(text):
	# This parts checks if the first line contains a doctype
	# If it does, it trims of the first line.
	# Note: this does not read the content of the doctype specification.
	m = re.match(r"\+(?P<key>doctype|extend)\((?P<type>\w*)\)\s", text)
	
	# FIXME when None-aware operators exist
	return (text[m.end():], {m['key'] : m['type']}) if m else (text, {})


def treebuilder(file_path : Path, **options) -> ET.Element:
	"""
	This function does things
	"""

	file_path = Path(file_path)
	bases = options.get('base') or file_path.parent

	# reset directory
	old_path = node.pathstack # revert after extending
	node.pathstack = file_path.parent


	with open(file_path, mode="r", encoding="utf-8") as file:
		text = file.read()
	
	text, type_ = get_type(text)


	if "extend" in type_:
		base_path = get_base_path(type_.get("extend"), bases)
		root = treebuilder(base_path)
		wrap = get_wrap_node(root)
		wrap.parse(text)
	elif "doctype" in type_:
		root = node.Addup("root")
		root.parse(text)
		node.pathstack = old_path

		root.set("type", type_.get("doctype"))
	else: # no type_
		root = node.Addup("root")
		root.parse(text)

	return root
