import re
import xml.etree.cElementTree as ET
from .Context import ContextManager as CM
from .Token import MObject, MGroup, MAction


def treebuilder(text, **options):
	"""
	This function does things
	"""

	root = Math(tag = "math", attrib = {"align": "true"}, text = text)
	root.parse()

	return root

def Tokenizer(text):
	"""This is a tokenizer
	Note: text_ is also a function
	"""

	#test "if reader is alpha:"; faster, slower than text[p].isalpha()?

	def alpha(p):
		i = 1
		try:
			while CHAR_MAP.get(text[p+i]) is alpha:
				i += 1
		except IndexError:
			pass

		return CM.GET_CONTEXT_OR_DEFAULT(text[p:p+i]), p+i

	def numeric(p):
		if text[p] == "0":
			try:
				num_type = {
					'b': "01",                        #binary
					'B': "01",
					'o': "01234567",                  #octal
					'O': "01234567",
					'x': "0123456789abcdefABCDEF",    #hexadecimal
					'X': "0123456789abcdefABCDEF",
					'r': "IVXLCDM",                   #roman
					'R': "IVXLCDM",
				}.get(text[p+1], "")
			except IndexError:
				pass

			i = 2
			try:
				while text[p+i] in num_type:
					i += 1
			except IndexError:
				pass

			if i > 2:
				# Serif for roman numerals
				dict_= {"mathvariant": "normal"} if text[p+1] in {'r','R'} else {}
				return MObject("mn", dict_, "numeric", text[p+2:p+i]), p+i

		# 200 000,000 or 2.000.000
		j = 1
		try:
			while text[p+j] in "0123456789 ,.":
				if text[p+j] in " ,." and text[p+j+1] not in "0123456789": break
				j += 1
		except IndexError:
			pass
		return MObject("mn", {}, "numeric", text[p:p+j]), p+j

	def open_(p):
		bracket = text[p]
		if bracket == '{': bracket = ''
		return MAction("mo", {"fence": "true"}, "OPEN", bracket), p + 1

	def close(p):
		bracket = text[p]
		if bracket == '}': bracket = ''
		return MAction("mo", {"fence": "true"}, "CLOSE", bracket), p + 1

	def subb(p):
		if text[p+1] == '_':
			return MAction("munder", {}, "GROUPER", [-1, 1]), p + 2
		return MAction("msub", {}, "SUB", None), p + 1

	def supp(p):
		if text[p+1] == '^':
			return MAction("mover", {}, "GROUPER", [-1, 1]), p + 2
		return MAction("msup", {}, "SUP", None), p + 1


	# For action
	def collect_bracketed(p):
		opening = text[p]
		closing = {
			'{': '}',
			'(': ')',
			'[': ']',
		}.get(opening, ' ') #possible bug source

		j = 1
		while text[p+j] != closing:
			j += 1

		return text[p+1:p+j], j

	def attr(p):
		attribute, j = collect_bracketed(p)
		return MAction("NONE", {"unfinished": "unfinished"}, "ATTRIBUTE", [1]),j

	def class_(p):
		class_name, j = collect_bracketed(p)
		return MAction("NONE", {"class": class_name}, "ATTRIBUTE", [1]), j

	def id_(p):
		id_name, j = collect_bracketed(p)
		return MAction("NONE", {"id": id_name}, "ATTRIBUTE", [1]), j

	def begin(p):
		type_, j = collect_bracketed(p)
		return MAction("NONE", {}, "OPENTABLE", type_), j

	def end(p):
		type_, j = collect_bracketed(p)
		return MAction("NONE", {}, "CLOSETABLE", type_), j

	def cast(tag, kind, p):
		text, j = collect_bracketed(p)
		return MObject(tag, {}, kind, text), j

	def action(p):
		i = 1
		try:
			while text[p+i].isalpha():
				i += 1
		except IndexError:
			pass

		# Symbol is found
		if i == 1: return CM.GET_SYMBOL_OR_DEFAULT(text[p:p+i+1]), p+i+1

		# Try substitution
		mObject_or_Action = CM.GET_UNICODE(text[p:p+i])\
			or CM.GET_ACTION(text[p:p+i])

		if mObject_or_Action:
			return mObject_or_Action, p+i

		mObject_or_Action, j = {
			r"\attr"  : attr(p+i),
			r"\class" : class_(p+i),
			r"\id"    : id_(p+i),

			r"\begin" : begin(p+i),
			r"\end"   : end(p+i),

 			# CAST
			r"\var"    : cast("mi", "var", p+i),
			r"\num"    : cast("mn", "numeric", p+i),
			r"\op"     : cast("mo", "operator", p+i),
			r"\string" : cast("ms", "string", p+i),
			r"\space"  : cast("mspace", "space", p+i),
			r"\text"   : cast("mtext", "text", p+i),
		}.get(text[p:p+i], (None, 0))

		if mObject_or_Action:
			return mObject_or_Action, p+i+j+1

		# Error
		return MObject("mi", {"class": "UNKNOWN"}, "UNKNOWN", text[p:p+i]), p+i


	# Simple tokens
	operator = lambda p: (MObject("mo", {"form": "infix"}, "operator", text[p]), p + 1)
	relation = lambda p: (MObject("mo", {}, "relation", text[p]), p + 1)

	sep = lambda p: (MAction("mo", {"fence": "true"}, "SEP", text[p]), p + 1)
	eol      = lambda p: (MAction("NONE", {}, "EOL", text[p]), p + 1)
	text_    = lambda p: (MAction("mtext", {}, "TEXT", text[p]), p + 1)
	divider  = lambda p: (MAction("NONE", {}, "TABLEDIV", text[p]), p + 1)
	space    = lambda p: (MAction("NONE", {}, "SPACE", text[p]), p + 1)

	other    = lambda p: (MObject("ms", {}, "UNKNOWN", text[p]), p + 1)


	# Tokens
	ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	CHAR_TOKENS = {
		"alpha"    : dict.fromkeys(iter(ALPHABET), alpha),
		"numeric"  : dict.fromkeys(iter("0123456789"), numeric),
		"operator" : dict.fromkeys(iter("+-*/"), operator),
		"relation" : dict.fromkeys(iter("<=>"), relation),
		"open"     : dict.fromkeys(iter("{[("), open_),
		"close"    : dict.fromkeys(iter("}])"), close),
		"supp"     : dict.fromkeys(iter("^"), supp),
		"subb"     : dict.fromkeys(iter("_"), subb),
		"sep"      : dict.fromkeys(iter(",.|"), sep),
		"eol"      : dict.fromkeys(iter("\n"), eol),
		#comment  : dict.fromkeys(iter("%"), comme), #ironic that the comment is
		"text"     : dict.fromkeys(iter("$"), text_),
		"divider"  : dict.fromkeys(iter("&"), divider),
		"space"    : dict.fromkeys(iter(" "), space),
		"action"    : dict.fromkeys(iter("\\"), action),
	}

	CHAR_MAP = {}
	for MAP in CHAR_TOKENS.values():
		CHAR_MAP.update(MAP)

	p = 0
	while p < len(text):
		c = text[p]
		reader = CHAR_MAP.get(c, other)
		token, p = reader(p)
		#print(f"""T: {token}, P: {p}""")
		yield token


def fence(tokens):
	"""Pairs (brackets} (must not be of same type)
	"""
	def separator(p):
		# Some separators may be brackets;
		# if not, they're turned back into separators here.
		sep = tokens[p]
		tokens[p] = MObject("mo", sep.attr.copy(), "sep", sep.targs)
		return p+1

	def open_(p):
		bracket = tokens[p]
		tokens[p] = MAction("NONE", {}, "OPEN", [])
		if bracket.targs:
			tokens.insert(p+1, MObject("mo", bracket.attr.copy(), "bracket", bracket.targs))
			return p+2
		return p+1

	def close(p):
		bracket = tokens[p]
		tokens[p] = MAction("NONE", {}, "CLOSE", [])
		if bracket.targs:
			tokens.insert(p, MObject("mo", bracket.attr.copy(), "bracket", bracket.targs))
			return p+2
		return p+1

	def left(p):
		bracket = tokens[p+1]
		tokens[p] = MAction("NONE", {}, "OPEN", [])
		if bracket[3]: # by index (expect targs, but anything goes)
			tokens[p+1] = MObject("mo", bracket.attr.copy(), "bracket", bracket[3])
			return p+2
		else:
			tokens.pop(p+1)
			return p+1

	def middle(p):
		separator = tokens[p+1]
		tokens[p+1] = MObject("mo", separator.attr.copy(), "sep", separator.targs)

		tokens.pop(p)
		return p+1

	def right(p):
		bracket = tokens[p+1]
		tokens[p+1] = MAction("NONE", {}, "CLOSE", [])
		if bracket[3]: # by index (expect targs, but anything goes)
			tokens[p] = MObject("mo", bracket.attr.copy(), "bracket", bracket[3])
			return p+2
		else:
			tokens.pop(p)
			return p+1


	p = 0
	while p < len(tokens):
		token = tokens[p]
		p = {
			"SEP": separator,
			"OPEN": open_,
			"CLOSE": close,
			"LEFT": left,
			"MIDDLE": middle,
			"RIGHT": right,
		}.get(token.type, lambda p: p+1)(p)


def changes(tokens):
	"""add class to elements between \[\) and \(\] (may overlap)
	"""
	prev = False
	next_ = False

	def TOGGLE_PREV(state, p):
		tokens.pop(p)
		nonlocal prev
		prev = state
		return True

	def TOGGLE_NEXT(state, p):
		tokens.pop(p)
		nonlocal next_
		next_ = state
		return True

	def addclass(token, class_name):
		try:
			token.attr["class"] += f" {class_name}"
		except KeyError:
			token.attr["class"] = class_name

	from functools import partial

	p = 0
	while p < len(tokens):
		token = tokens[p]

		toggled = {
			"OPENPREV"  : partial(TOGGLE_PREV, True),
			"CLOSEPREV" : partial(TOGGLE_PREV, False),
			"OPENNEXT"  : partial(TOGGLE_NEXT, True),
			"CLOSENEXT" : partial(TOGGLE_NEXT, False),
		}.get(token.type, lambda p: False)(p)

		if toggled: continue

		if prev: addclass(token, "prev")
		if next_: addclass(token, "next")

		p += 1


def invisibles(tokens):
	"""This adds the semantically &it; and &af;
	where they are suitable:

	[var/numeric/constant/close]  [space -> it]  [var/numeric/constant/open]
	[var/numeric/constant/close]  [nothing->it]  [numeric/constant/open]
	    [numeric/constant/close]  [nothing->it]  [var/numeric/constant/open]
	              [var/operator]  [nothing->af]  [open]
	"""

	p = 0
	while p < len(tokens):
		if tokens[p].type in {"EOL", "SPACE"}:
			tokens.pop(p)
		else:
			p += 1



def treeize(tokens):
	"""Makes (a tree (out of) (((the))) (fences))
	"""
	def open_(p):
		bracketed_group = MGroup("mrow", {}, "TREE", [])

		p += 1
		while tokens[p].type != "CLOSE":
			token, p = group(p)
			bracketed_group.children.append(token)

		return bracketed_group, p+1 # skip close


	def table_open(p):
		# Customizable brackets?
		# Fix double predicates?
		matrix_table = MGroup("mtable", {}, "TREE", [])

		p += 1
		while tokens[p].type not in {"CLOSETABLE"}:
			matrix_row = MGroup("mtr", {}, "TREE", [])
			matrix_table.children.append(matrix_row)

			while tokens[p].type not in {"CLOSETABLE", "NEWLINE"}:
				matrix_cell = MGroup("mtd", {}, "TREE", [])
				matrix_row.children.append(matrix_cell)

				while tokens[p].type not in {"CLOSETABLE", "NEWLINE", "TABLEDIV"}:
					token, p = group(p)
					matrix_cell.children.append(token)

				if tokens[p].type not in {"CLOSETABLE", "NEWLINE"}:
					p += 1

			if tokens[p].type not in {"CLOSETABLE"}:
				p += 1


		matrix_container = MGroup("mrow", {}, "TREE", [
			MObject("mo", {"stretchy": "true"}, "bracket", "("),
			matrix_table,
			MObject("mo", {"stretchy": "true"}, "bracket", ")"),
		])

		return matrix_container, p+1 # skip tableclose

	def default(p):
		#if not isinstance(token, MObject): print("Wrong object"); return
		return tokens[p], p+1


	def group(p):
		return {
			"OPEN"      : open_,
			"OPENTABLE" : table_open,
		}.get(tokens[p].type, default)(p)

	tree = MGroup("math", {"displaystyle": "true"}, "MAIN", [])

	p = 0
	while p < len(tokens):
		#print(tokens[p])
		token, p = group(p)
		tree.children.append(token)

	return tree

def classify(tree):
	"""Adds class to grouping objects
	"""
	def update(attribute, value, token):
		try:
			token.attr[attribute] += f" {value}"
		except KeyError:
			token.attr[attribute] = value

	def attribute(tree, p):
		next_token = tree.children[p+1]
		for attrib, value in tree.children[p].attr.items():
			if attrib in {"class", "id"}:
				update(attrib, value, next_token)
			else: # Overwrite others
				next_token.attr[attrib] = value

		tree.children.pop(p)
		return p

	def row(tree, p):
		subtree = tree.children[p]
		attributize(subtree)
		return p+1

	def attributize(tree):
		p = 0
		while p < len(tree.children):
			p = {
				"ATTRIBUTE" : attribute,
				"TREE"       : row,
			}.get(tree.children[p].type, lambda*_: p+1)(tree, p)

	attributize(tree)


def process(tree):
	"""Uses tree manipulators such as \vec, \sup, \pre and _^
	"""
	def grouper(tree, p):
		action = tree.children[p]

		grouping = MGroup(action.tag, action.attr, "TREE", [])
		for i in action.targs:
			# fetches the neighbours given by relative position in targs
			grouping.children.append(tree.children[p+i])

		# Assumes children are continuous. Includes self & endpoint.
		# Saves first for insertion.
		del tree.children[p+min(min(action.targs), 0)+1:p+max(action.targs)+1]

		# Inserts the grouped at the first element in the grouper
		tree.children[p+min(min(action.targs), 0)] = grouping

		# Recursively apply to children
		group(grouping)

		return p + min(min(action.targs), 0) + 1


	def accent(tree, p):
		action = tree.children[p]

		accenting = MGroup("mover", action.attr, "TREE", [])
		accent = MObject(action.tag, {}, "accent", action.targs)
		accented = tree.children.pop(p+1)

		accenting.children.append(accented)
		accenting.children.append(accent)

		tree.children[p] = accenting

		# Recursively apply to children
		group(accenting)

		return p+1


	def sub(tree, p):
		i = 0
		try:
			while tree.children[p+i+2].type in {"SUB", "SUP"}:
				# p-1, p+i+3 may be Action
				if not isinstance(tree.children[p+i+1], MAction):
					i += 2
		except IndexError:
			pass

		if i == 0: # Only sub (or under)
			if "largeop" in tree.children[p-1].attr: #under
				undering = MGroup("munder", {}, "TREE", [])
				undering.children.append(tree.children[p-1])
				undering.children.append(tree.children[p+1])

				del tree.children [p:p+2]

				tree.children[p-1] = undering

				# Recursively apply to children
				group(undering)

			else:
				subing = MGroup("msub", {}, "TREE", [])
				subing.children.append(tree.children[p-1])
				subing.children.append(tree.children[p+1])

				del tree.children [p:p+2]

				tree.children[p-1] = subing

				# Recursively apply to children
				group(subing)

		elif i == 2: #Possibly sub + sub or sup
			if tree.children[p+i].type == "SUP":
				if "largeop" in tree.children[p-1].attr: #under
					underovering = MGroup("munderover", {}, "TREE", [])
					underovering.children.append(tree.children[p-1])
					underovering.children.append(tree.children[p+1])
					underovering.children.append(tree.children[p+3])

					del tree.children [p:p+i+2]

					tree.children[p-1] = underovering

					# Recursively apply to children
					group(underovering)

				else:
					subsuping = MGroup("msubsup", {}, "TREE", [])
					subsuping.children.append(tree.children[p-1])
					subsuping.children.append(tree.children[p+1])
					subsuping.children.append(tree.children[p+3])

					del tree.children [p:p+i+2]

					tree.children[p-1] = subsuping

					# Recursively apply to children
					group(subsuping)
			else:
				multiscripting = MGroup("mmultiscripts", {}, "TREE", [])
				none = MObject("none", {}, "empty", [])

				multiscripting.children.append(tree.children[p-1])
				multiscripting.children.append(tree.children[p+1])
				multiscripting.children.append(none)
				multiscripting.children.append(tree.children[p+3])
				multiscripting.children.append(none)

				del tree.children [p:p+i+2]

				tree.children[p-1] = multiscripting

				# Recursively apply to children
				group(multiscripting)


		elif i > 2:
			multiscripting = MGroup("mmultiscripts", {}, "TREE", [])
			none = MObject("none", {}, "empty", [])

			multiscripting.children.append(tree.children[p-1]) #main

			j = 1
			while j < i+2:
				if tree.children[p+j-1].type == "SUB":
					multiscripting.children.append(tree.children[p+j])
					j += 2
				else:
					multiscripting.children.append(none)

				if tree.children[p+j-1].type == "SUP":
					multiscripting.children.append(tree.children[p+j])
					j += 2
				else:
					multiscripting.children.append(none)


			del tree.children [p:p+i+2]

			tree.children[p-1] = multiscripting

			# Recursively apply to children
			group(multiscripting)

		return p

	def sup(tree, p):
		i = 0
		try:
			while tree.children[p+i+2].type in {"SUB", "SUP"}:
				# p-1, p+i+3 may be Action
				if not isinstance(tree.children[p+i+1], MAction):
					i += 2
		except IndexError:
			pass

		if i == 0:
			suping = MGroup("msup", {}, "TREE", [])
			suping.children.append(tree.children[p-1])
			suping.children.append(tree.children[p+1])

			del tree.children [p:p+2]

			tree.children[p-1] = suping

			# Recursively apply to children
			group(suping)

		elif i > 2: #mmultiscripts
			multiscripting = MGroup("mmultiscripts", {}, "TREE", [])
			none = MObject("none", {}, "empty", [])

			multiscripting.children.append(tree.children[p-1]) #main

			j = 1
			while j < i+2:
				if tree.children[p+j-1].type == "SUB":
					multiscripting.children.append(tree.children[p+j])
					j += 2
				else:
					multiscripting.children.append(none)

				if tree.children[p+j-1].type == "SUP":
					multiscripting.children.append(tree.children[p+j])
					j += 2
				else:
					multiscripting.children.append(none)


			del tree.children [p:p+i+2]

			tree.children[p-1] = multiscripting

			# Recursively apply to children
			group(multiscripting)

		return p

	def pre(tree, p):
		i = 0
		while tree.children[p+i+1].type in {"SUB", "SUP"}:
			# p-1, p+i+3 may be Action
			if not isinstance(tree.children[p+i+2], MAction):
				i += 2
		j = i
		try:
			while tree.children[p+j+2].type in {"SUB", "SUP"}:
				# p-1, p+i+3 may be Action
				if not isinstance(tree.children[p+j+1], MAction):
					j += 2
		except IndexError:
			pass

		multiscripting = MGroup("mmultiscripts", {}, "TREE", [])
		none = MObject("none", {}, "empty", [])

		multiscripting.children.append(tree.children[p+i+1]) #main

		# postscripts
		k = i+1
		while k < j:
			if tree.children[p+k+1].type == "SUB":
				multiscripting.children.append(tree.children[p+k+2])
				k += 2
			else:
				multiscripting.children.append(none)

			if tree.children[p+k+1].type == "SUP":
				multiscripting.children.append(tree.children[p+k+2])
				k += 2
			else:
				multiscripting.children.append(none)

		# prescripts
		prescripts = MObject("mprescripts", {}, "empty", [])
		multiscripting.children.append(prescripts)

		k = 1
		while k < i:
			if tree.children[p+k].type == "SUB":
				multiscripting.children.append(tree.children[p+k+1])
				k += 2
			else:
				multiscripting.children.append(none)

			if tree.children[p+k].type == "SUP":
				multiscripting.children.append(tree.children[p+k+1])
				k += 2
			else:
				multiscripting.children.append(none)

		del tree.children [p+1:p+j+2]

		tree.children[p] = multiscripting

		# Recursively apply to children
		group(multiscripting)

		return p



	def row(tree, p):
		subtree = tree.children[p]
		group(subtree)
		return p+1

	def group(tree):
		p = 0
		while p < len(tree.children):
			p = {
				"GROUPER"    : grouper,
				"ACCENT"     : accent,

				"SUB"        : sub,
				"SUP"        : sup,
				"PRE"        : pre,

				"TREE"       : row,
			}.get(tree.children[p].type, lambda tree, p: p+1)(tree, p)

			#input("\n\n"+str(tree))

	group(tree)

def align(tree, counter):
	"""Aligns the tree in a table
	"""
	matrix_table = MGroup("mtable", {"displaystyle": "true"}, "TREE", [])

	p = 0
	while p < len(tree.children):
		matrix_row = MGroup("mtr", {}, "TREE", [])
		matrix_table.children.append(matrix_row)

		#numbering:
		matrix_cell = MGroup("mtd", {}, "TREE", [])
		matrix_row.children.append(matrix_cell)
		matrix_numbering = MObject("mn", {"columnalign": "right"}, "var", str(counter))
		matrix_cell.children.append(matrix_numbering)
		counter += 1

		while tree.children[p].type not in {"NEWLINE"}:
			matrix_cell = MGroup("mtd", {"columnalign": "left"}, "TREE", [])
			matrix_row.children.append(matrix_cell)

			while tree.children[p].type not in {"NEWLINE", "TABLEDIV"}:
				matrix_cell.children.append(tree.children[p])

				p += 1
				if p >= len(tree.children): break

			if p >= len(tree.children): break
			if tree.children[p].type == "TABLEDIV":
				p += 1
		p += 1

	del tree.children[:]

	tree.children.append(matrix_table)

	return tree


def mmlise(parent, tree):
	def create_node(tag, attrib):
		return Node(tag = tag, attrib = attrib, text = '', tail = '')

	def to_mml(parent, tree):
		for token in tree.children:
			#print(f"mml: {token.tag}")
			node = create_node(tag = token.tag, attrib = token.attr)
			parent.append(node)
			if isinstance(token, MGroup): to_mml(node, token)
			if isinstance(token, MObject): node.text = token.text
			if isinstance(token, MAction): pass

		return parent

	to_mml(parent, tree)

def eat_arguments(node, text):
	# argend is } instead of ) in mathmode
	DEL = r'(?P<argend>\))|(?P<has_value>=)'
	ATTR = r'\s*(?P<attribute>[\w-]+)\s*'
	VAL = r'\s*"(?P<value>.*?)"\s*'

	tokens = re.compile('|'.join((VAL, ATTR, DEL))).finditer(text)

	for mo in tokens:
		kind = mo.lastgroup
		if kind == "attribute":
			attribute = mo.group(kind)
			node.attrib[attribute] = ""

		if kind == "has_value":
			mo = next(tokens)
			kind = mo.lastgroup
			node.attrib[attribute] = mo.group(kind)

		if kind == "argend":
			return text[mo.end():]


class Node(ET.Element):
	def __init__(self, tag, attrib, text, tail, **extra):
		super().__init__(tag, attrib.copy(), **extra)
		self.text = text or ""
		self.tail = tail or ""


class Math(Node):
	# substitution patterns
	sub_patterns = {
		"&": "&amp;",
		"<": "&lt;",
		">": "&gt;",
		"\\[^\\]": "",
	}

	def __init__(self, tag="", attrib={}, text="", tail="",  **extra):
		super().__init__(tag, attrib.copy(), text, tail, **extra)

	eat_arguments = eat_arguments

	def addNode(self, tag, attrib={}, text="", tail="", **extra):
		child = ET.Element(tag, attrib, **extra)
		self.append(child)
		child.text = text
		child.tail = tail
		return child

	def eat(self, text):
		has_argument = re.compile(r"(?P<ARGUMENT>\()").match(text)
		if has_argument:
			text = self.eat_arguments(text)

		#aligned = type(self.attrib.pop("align", 0)) is str

		END = rf'(?P<end>{re.escape(self.attrib.pop("token"))})'
		EOF = r'(?P<eof>\Z)'

		# End of math block-token
		token = re.compile('|'.join((END, EOF)), re.M).search(text)

		# Eat Math block
		self.text, inedible_text = text[:token.start()], text[token.end():]
		self.text = self.text.strip().replace('\n\n', r'\\')

		# Apply alignment (MathJax mode)
		#if aligned: self.text = rf"\begin{{align*}}{self.text}\end{{align*}}"

		# Check if multiline/block or inline math
		#if '\n' in self.text: self.attrib["display"] = "block"
		#else: self.attrib["display"] = "inline"

		self.parse()

		return inedible_text

	def parse(self):

		# make element
		# if normal:
		#	- make element (mi, mn, mtable)
		#	- check if succeeded by sub/sup (mmultiscripts)
		#	- if big -> under/over
		#	- check if succeeded by element -> &InvisibleTimes;
		# if pre:
		#	- get next element -> mmultiscripts
		# if mo:
		#	- check if it's function; is next element args? (postprocess?) &af;

		tokens = list(Tokenizer(self.text))
		fence(tokens)
		changes(tokens)
		invisibles(tokens) # unfinished
		tree = treeize(tokens)
		classify(tree)
		process(tree)

		try:
			self.attrib.pop("align")
			align(tree, counter = 0)
		except KeyError:
			pass

		self.text = ""
		mmlise(self, tree)

		def treeprinter(tree, level):
			input(" "*(level-1) + tree.tag + str(tree.attr))
			for token in tree.children:
				if isinstance(token, MGroup): treeprinter(token, level+1)
				if isinstance(token, MAction):
					input(" "*level + token.tag + str(token.attr))
				if isinstance(token, MObject):
					input(" "*level + token.tag + str(token.attr))

		#treeprinter(tree, 0)

MATHML = {"math", "maction", "maligngroup", "malignmark", "menclose", "merror", "mfenced", "mfrac", "mglyph", "mi", "mlabeledtr", "mlongdiv", "mmultiscripts", "mn", "mo", "mover", "mpadded", "mphantom", "mroot", "mrow", "ms", "mscarries", "mscarry", "msgroup", "mstack", "mlongdiv", "msline", "mspace", "msqrt", "msrow", "mstack", "mstyle", "msub", "msub", "msup", "msubsup", "mtable", "mtd", "mtext", "mtr", "munder", "munderover", "semantics", "annotation", "annotation-xml", "mprescripts", "none"}
