import re
import xml.etree.ElementTree as ET
import mumath
import textwrap

EXEC = False

#pathstack = ["tests/"] # when testing
pathstack = [] # for relative imports

def treebuilder(text, **options):
	"""
	This function does things
	"""

	root = Addup("root")

	# This parts checks if the first line contains a doctype
	# If it does, it trims of the first line.
	# Note: this does not read the content of the doctype specification.
	if re.match(r"\+doctype.*?\s", text):
		root.set("doctype", True)
		text = text[re.match(r"\+doctype.*?\s", text).end():]

	root.text = text
	root.parse()

	return root


def inline(node, text):
	ESC = r'(?P<escape>\\)'
	OPEN = r'(?P<open>\()'
	CLOSE = r'(?P<close>\))'
	QUOTE = r'(?P<quote>")'

	tokens = re.compile('|'.join((ESC, OPEN, CLOSE, QUOTE))).finditer(text)

	bracket_count = 0
	in_quotes = False
	for mo in tokens:
		type_ = mo.lastgroup
		if type_ == "quote":
			in_quotes = not in_quotes

		elif type_ == "open" and not in_quotes:
			bracket_count += 1

		elif type_ == "close" and not in_quotes:
			bracket_count -= 1

			if bracket_count == 0:
				# We start from 1 because we don't want the opening bracket
				node.text, text = text[1:mo.start()], text[mo.end():]
				break

	return text

def block(node, text):
	END = r'(?P<end>\n)(?=\S)'
	EOF = r'(?P<eof>\Z)'

	token = re.compile('|'.join((END, EOF)), re.M).search(text)

	node.text, text = text[:token.end()], text[token.end():]
	node.text = textwrap.dedent(node.text).strip()

	return text


def eat_arguments(node, text):
	DEL = r'(?P<argend>\))|(?P<has_value>=)'
	ATTR = r'\s*(?P<attribute>[\w-]+)\s*'
	VAL = r'\s*"(?P<value>.*?)"\s*'

	tokens = re.compile('|'.join((VAL, ATTR, DEL))).finditer(text)

	for mo in tokens:
		type_ = mo.lastgroup

		if type_ == "attribute":
			attribute = mo.group(type_)
			node.set(attribute, "")

		if type_ == "has_value":
			mo = next(tokens)
			type_ = mo.lastgroup
			node.set(attribute, mo.group(type_)) #attribute not defined? crash?

		if type_ == "argend":
			return text[mo.end():]


class Node(ET.Element):
	def __init__(self, tag, attrib, text, tail, **extra):
		super().__init__(tag, attrib.copy(), **extra)
		self.text = text or ""
		self.tail = tail or ""


class Addup(Node):
	# substitution patterns
	sub_patterns = {
		"&": "&amp;",
		"<": "&lt;",
		">": "&gt;",
	}

	# element token patterns
	token_patterns = [
		r"(?=^|[^\\])\+(?P<addup>\w+)",
		r"(?=^|[^\\])(?P<code>`+)",
		r"(?=^|[^\\])(?P<math>\$+)",
		r"(?=^|[^\\])(?P<comment>//)",
		r"(?P<eof>\Z)",
	]

	# compile
	#sp = re.compile("|".join(map(re.escape, sub_patterns.keys())), re.M)
	sp = re.compile("|".join(sub_patterns.keys()), re.M)
	tp = re.compile("|".join(token_patterns), re.M)

	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		super().__init__(tag, attrib.copy(), text, tail, **extra)

	eat_inline = inline
	eat_block = block
	eat_arguments = eat_arguments

	def eat(self, text):
		has_argument = re.compile(r"(?P<ARGUMENT>\()").match(text)
		if has_argument:
			text = self.eat_arguments(text)

		has_content = re.compile(r"(?P<CONTENT>:)").match(text)
		if has_content:
			text = text[has_content.end():]

			inline_element = re.compile(r"(?P<INLINE>\()").match(text)
			if inline_element:
				inedible_text = self.eat_inline(text)

			else: #block element
				inedible_text = self.eat_block(text)

		else:
			inedible_text = text

		self.parse()

		return inedible_text

	def parse(self):

		# Searches through tokens
		mo = Addup.tp.search(self.text)
		element_type = mo.lastgroup

		# text may be ""
		self.text, text = self.text[:mo.start()], self.text[mo.end():]

		# Add the text to the node
		self.text = Addup.sp.sub(lambda s: Addup.sub_patterns[s.group(0)], self.text)
		self.text = re.sub(r'\\(.)', r'\1', self.text)

		while text:
			tag = mo.group(element_type)

			def addup(tag):
				return {
					"style"  : Raw,
					"script" : Raw,
					"math"   : Math, # For mathjax, deprecated
					"read"   : Read,
					"image"  : Image,
					"css"    : CSS,
					"now"    : Date,
				}.get(tag, Addup)(tag = tag)
			code = lambda tag: Code(tag = "template", token = tag)
			math = lambda tag: mumath.Math(tag = "math", token = tag)
			comment = lambda tag: Comment(tag = ET.Comment)

			child = {
				"code"    : code,
				"math"    : math,
				"comment" : comment,
			}.get(element_type, addup)(tag)

			text = child.eat(text)
			self.append(child)

			if not text: break

			mo = Addup.tp.search(text)
			element_type = mo.lastgroup

			child.tail, text = text[:mo.start()], text[mo.end():]

			# Add the text to the node
			child.tail = Addup.sp.sub(lambda s: Addup.sub_patterns[s.group(0)], child.tail)
			child.tail = re.sub(r'\\(.)', r'\1', child.tail)


class Raw(Node):
	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		super().__init__(tag, attrib.copy(), text, tail, **extra)

	eat_inline = inline
	eat_block = block
	eat_arguments = eat_arguments

	def eat(self, text):
		has_argument = re.compile(r"(?P<ARGUMENT>\()").match(text)
		if has_argument:
			text = self.eat_arguments(text)

		has_content = re.compile(r"(?P<CONTENT>:)").match(text)
		if has_content:
			text = text[has_content.end():]

			inline_element = re.compile(r"(?P<INLINE>\()").match(text)
			if inline_element:
				inedible_text = self.eat_inline(text)

			else: #block element
				inedible_text = self.eat_block(text)

		else:
			inedible_text = text

		self.parse()

		return inedible_text

	def parse(self):
		pass

class Code(Node):
	# substitution patterns
	sub_patterns = {
		"&": "&amp;",
		"<": "&lt;",
		">": "&gt;",
		"\\[^\\]": "",
	}

	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		super().__init__(tag, attrib.copy(), text, tail, **extra)

		self.token = extra.pop("token", None)

	eat_arguments = eat_arguments

	def eat(self, text):
		has_argument = re.compile(r"(?P<ARGUMENT>\()").match(text)
		if has_argument:
			text = self.eat_arguments(text)


		END = rf'(?P<end>{self.attrib.pop("token")})'
		EOF = r'(?P<eof>\Z)'

		token = re.compile('|'.join((END, EOF)), re.M).search(text)

		self.text, inedible_text = text[:token.start()], text[token.end():]
		self.text = self.text.strip(r'\n')

		if '\n' in self.text or "block" in self.keys():
			self.tag = "div"
		else:
			self.tag = "span"

		if "run" in self.keys():
			self.attrib.pop("run")
			if EXEC == True:
				exec(self.text)

		self.parse()

		return inedible_text



	def getlexer(self):
		from pygments.util import ClassNotFound
		try:
			lang = list(self.keys())[0]
		except IndexError:
			lang = None

		from pygments.lexers import get_lexer_by_name
		# REMOVE? makes popping the key hard
		lang = {
			"SQL": "sql",
			"python": "python3",
			"js": "javascript",
		}.get(lang, lang)

		try:
			lexer = get_lexer_by_name(lang, encoding = "utf-8")
			self.attrib.pop(lang, None)
		except ClassNotFound:
			lexer = get_lexer_by_name("text", encoding = "utf-8")
		return lexer


	def parse(self):
		from pygments import highlight
		from pygments.formatters import HtmlFormatter
		from pygments.formatters import NullFormatter

		if '\n' in self.text or "block" in self.keys():
			type_ = "block"
			self.attrib.pop("block", None)
		else:
			type_ = "inline"

		lexer = self.getlexer()
		lang = lexer.aliases[0]

		class BlockHtmlFormatter(HtmlFormatter):
		    def wrap(self, source, outfile):
		        return self._wrap_code(source)

		    def _wrap_code(self, source):
		        yield 0, f'<pre class="code {lang.lower()}"><code class="highlight">'
		        for i, t in source:
		            yield i, f'<span class="line">{t}</span>'
		        yield 0, '</code></pre>'

		class InlineHtmlFormatter(HtmlFormatter):
		    def wrap(self, source, outfile):
		        return self._wrap_code(source)

		    def _wrap_code(self, source):
		        yield 0, ''
		        for i, t in source:
		            yield i, f'<code class="inline highlight">{t}</code>'
		        yield 0, ''

		if "numbering" in self.keys():
			line_numbering = "table"
			self.attrib.pop("numbering", None)
		else:
			line_numbering = False

		#get the formatter(s)
		formatter = {
			"block": BlockHtmlFormatter(
				linenos       = line_numbering,
				linenostart   = 0,
				lineanchors   = f"no_anchor",
				lineseparator = "<br>",
			),
			"inline": InlineHtmlFormatter(
				lineseparator = "",
			),
		}

		#formatted code
		self.text = highlight(
			code      = self.text,
			lexer     = lexer,
			formatter = formatter[type_],
		)


class Math(Node):
	# substitution patterns
	sub_patterns = {
		"&": "&amp;",
		"<": "&lt;",
		">": "&gt;",
		"\\[^\\]": "",
	}

	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		super().__init__(tag, attrib.copy(), text, tail, **extra)

		self.token = extra.pop("token", None)

	eat_arguments = eat_arguments

	def eat(self, text):
		has_argument = re.compile(r"(?P<ARGUMENT>\()").match(text)
		if has_argument:
			text = self.eat_arguments(text)

		aligned = type(self.attrib.pop("align", 0)) is str

		END = rf'(?P<end>{re.escape(self.token)})'
		EOF = r'(?P<eof>\Z)'

		token = re.compile('|'.join((END, EOF)), re.M).search(text)

		self.text, inedible_text = text[:token.start()], text[token.end():]
		self.text = self.text.strip().replace('\n\n', r'\\')

		if aligned:
			self.text = rf"\begin{{align*}}{self.text}\end{{align*}}"

		if '\n' in self.text:
			self.set("type", "math/tex; mode=display")
		else:
			self.set("type", "math/tex")

		self.parse()

		return inedible_text

	def parse(self):
		pass


class Comment(Node):
	# substitution patterns
	sub_patterns = {
		"&": "&amp;",
		"<": "&lt;",
		">": "&gt;",
		"\\[^\\]": "",
	}

	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		super().__init__(tag, attrib.copy(), text, tail, **extra)

	#REMOVE?
	"""
	@property
	def tag(self): return self.node.tag
	@tag.setter
	def tag(self, tag): self.node.tag = tag
	"""
	def eat(self, text):
		EOL = r'(?P<eol>$)'
		EOF = r'(?P<eof>\Z)'

		token = re.compile('|'.join((EOL, EOF)), re.M).search(text)

		self.text, inedible_text = text[:token.start()], text[token.end():]

		#There may be --> in text (?)
		self.text = self.text.strip(r'\n')

		return inedible_text

	def parse(self):
		pass


class Read(Node):
	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		super().__init__(tag, attrib.copy(), text, tail, **extra)

	eat_arguments = eat_arguments

	def eat(self, text):
		has_argument = re.compile(r"(?P<ARGUMENT>\()").match(text)
		if has_argument:
			text = self.eat_arguments(text)

		try:
			self.tag = self.attrib.pop("tag")
		except KeyError:
			self.tag = "div" #default

		self.parse()

		return text

	def parse(self):
		path = ''.join(pathstack)+self.attrib.pop("loc")
		with open(path, mode='r') as ifile:
			import os
			if os.path.dirname(ifile.name):
				pathstack.append(os.path.dirname(ifile.name)+'/')
			else: # if same folder
				pathstack.append('./')

			template_root = Addup("root")
			template_root.text = ifile.read()
			template_root.parse()

			pathstack.pop()

			for child in template_root:
				self.append(child)

class Image(Node):
	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		super().__init__(tag, attrib.copy(), text, tail, **extra)

	eat_arguments = eat_arguments

	def eat(self, text):
		has_argument = re.compile(r"(?P<ARGUMENT>\()").match(text)
		if has_argument:
			text = self.eat_arguments(text)

		self.parse()
		self.tag = "img"

		return text

	def parse(self):
		path = ''.join(pathstack)+self.attrib.pop("loc")
		with open(path, mode='rb') as img_file:
			import base64
			b64 = base64.b64encode(img_file.read()).decode("utf-8")
			self.set("src", f"data:image/png;base64,{b64}")


class CSS(Node):
	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		super().__init__(tag, attrib.copy(), text, tail, **extra)

	eat_arguments = eat_arguments

	def eat(self, text):
		has_argument = re.compile(r"(?P<ARGUMENT>\()").match(text)
		if has_argument:
			text = self.eat_arguments(text)

		self.parse()
		self.tag = "style"

		return text

	def parse(self):
		path = ''.join(pathstack)+self.attrib.pop("loc")
		with open(path, mode='r') as css_file:
			self.text = css_file.read()

class Date(Node):
	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		super().__init__(tag, attrib.copy(), text, tail, **extra)

	eat_arguments = eat_arguments

	def eat(self, text):
		has_argument = re.compile(r"(?P<ARGUMENT>\()").match(text)
		if has_argument:
			text = self.eat_arguments(text)

		from datetime import date
		self.text = str(date.today())
		self.set("datetime", date.today())

		return text

class Base(Node):
	# substitution patterns
	sub_patterns = {
		"&": "&amp;",
		"<": "&lt;",
		">": "&gt;",
		"\\[^\\]": "",
	}

	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		super().__init__(tag, attrib.copy(), text, tail, **extra)

	def eat(self, text):
		pass

	def parse(self):
		pass
