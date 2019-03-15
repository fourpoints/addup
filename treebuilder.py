import re
import xml.etree.ElementTree as ET
import mumath
import textwrap

# Allows for the exec() to be used to run code while compiling
EXEC = False

# pathlib.Path object
pathstack = None

def get_doctype(root):
	# This parts checks if the first line contains a doctype
	# If it does, it trims of the first line.
	# Note: this does not read the content of the doctype specification.
	m = re.match(r"\+doctype\((?P<type>\w*)\)\s", root.text)
	if m:
		root.set("doctype", m['type'])
		root.text = root.text[m.end():]

def treebuilder(file_path, dir, **options):
	"""
	This function does things
	"""

	# reset directory
	global pathstack
	pathstack = dir

	root = Addup("root")

	with open(file_path, mode="r", encoding="utf-8") as file:
		root.text = file.read()

	get_doctype(root) # possibly none

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
	ATTR = r'\s*(?P<attribute>[\w\-:\.@]+)\s*'
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

def eat_classifiers(node, text):
	classifiers = re.compile(r"(?P<CLASSID>[\.@][\w\-]+)+").match(text)

	# first element will be empty string, then every other element will be a separator (. or @) with the succeeding element the class/id name.
	classifier_list = re.split("([\.@])", text[:classifiers.end()])

	classifier_iter = iter(classifier_list[1:])
	# groups two at a time
	classifier_tuples = zip(classifier_iter, classifier_iter)

	def extend_attribute(attribute, value):
		try:
			node.attrib[attribute] += " " + value
		except KeyError:
			node.attrib[attribute] = value

	for classifier_token, classifier_name in classifier_tuples:
		classifier_type = "id" if classifier_token == "@" else "class"
		extend_attribute(classifier_type, classifier_name)

	return text[classifiers.end():]


class Node(ET.Element):
	def __init__(self, tag, attrib, text, tail, **extra):
		super().__init__(tag, attrib.copy(), **extra)
		self.text = text or ""
		self.tail = tail or ""


class Addup(Node):
	# substitution patterns
	sub_patterns = {
		#"&": "&amp;",
		"<": "&lt;",
		">": "&gt;",
	}

	# element token patterns
	token_patterns = [
		r"(?=^|[^\\])\+(?P<addup>[\w\-]+)",
		r"(?=^|[^\\])(?P<code>`+)",
		r"(?=^|[^\\])(?P<math>\$+)",
		r"(?=^|[^\\])(?P<comment>//)",
		r"(?P<eof>\Z)", # fix : rename to <eol>
	]

	# compile
	#sp = re.compile("|".join(map(re.escape, sub_patterns.keys())), re.M)
	sp = re.compile("|".join(sub_patterns.keys()), re.M)
	tp = re.compile("|".join(token_patterns), re.M)

	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		attrib = attrib.copy()
		super().__init__(tag, attrib, text, tail, **extra)

	eat_inline      = inline           # (bracketed)
	eat_block       = block            #     indented block
	eat_arguments   = eat_arguments    # (attribute="value")
	eat_classifiers = eat_classifiers  # .class@id

	def eat(self, text):
		has_classifier = re.compile(r"(?P<CLASSID>[\.@][\w\-]+)+").match(text)
		if has_classifier:
			text = self.eat_classifiers(text)

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
		# \e -> e (for escaped elements)
		self.text = re.sub(r'\\(.)', r'\1', self.text)

		while element_type != "eof":
			tag = mo.group(element_type)

			def addup(tag):
				return {
					"style"  : Raw,
					"script" : Raw,
					"math"   : Math, # For mathjax, deprecated
					"read"   : Read,
					"image"  : Image,
					"css"    : CSS,
					"js"     : JS,
					"now"    : Date,

					"update" : mumath.UpdateContext,
					"clear"  : mumath.ClearContext,
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
			if isinstance(child, ET.Element):
				self.append(child)

			if element_type == "eof": break

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
		self.text = self.text.strip('\n')

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

		lexer = self.getlexer()
		lang = lexer.aliases[0]

		class BlockHtmlFormatter(HtmlFormatter):
			def wrap(self, source, outfile):
			    return self._wrap_code(source)

			def _wrap_code(self, source):
			    yield 0, f'<code class="highlight">'
			    for i, t in source:
			        yield i, f'<span class="line">{t}</span>'
			    yield 0, '</code>'

			def _wrap_tablelinenos(self, inner):
				from pygments.util import StringIO
				dummyoutfile = StringIO()
				lncount = 0
				for t, line in inner:
					if t: lncount += 1
					dummyoutfile.write(line)

				fl = self.linenostart
				mw = len(str(lncount + fl - 1))
				sp = self.linenospecial
				st = self.linenostep
				la = self.lineanchors
				aln = self.anchorlinenos
				nocls = self.noclasses
				if sp:
					lines = []

					for i in range(fl, fl+lncount):
						if i % st == 0:
							if i % sp == 0:
								if aln:
									lines.append('<a href="#%s-%d" class="special">%*d</a>' %
									             (la, i, mw, i))
								else:
									lines.append('<span class="special">%*d</span>' % (mw, i))
							else:
								if aln:
									lines.append('<a href="#%s-%d">%*d</a>' % (la, i, mw, i))
								else:
									lines.append('%*d' % (mw, i))
						else:
							lines.append('')
					ls = '\n'.join(lines)
				else:
					lines = []
					for i in range(fl, fl+lncount):
						if i % st == 0:
							if aln:
								lines.append('<a href="#%s-%d">%*d</a>' % (la, i, mw, i))
							else:
								lines.append('%*d' % (mw, i))
						else:
							lines.append('')
					ls = '\n'.join(lines)

				# in case you wonder about the seemingly redundant <div> here: since the
				# content in the other cell also is wrapped in a div, some browsers in
				# some configurations seem to mess up the formatting...
				if nocls:
					yield 0, (#'<table class="%stable">' % self.cssclass +
								'<tr><td><div class="linenodiv" '
								'style="background-color: #f0f0f0; padding-right: 10px">'
								'<pre style="line-height: 125%">' +
								ls + '</pre></div></td><td class="code">')
				else:
					yield 0, (#'<table class="%stable">' % self.cssclass +
								'<tr><td class="linenos"><div class="linenodiv"><pre>' +
								ls + '</pre></div></td><td class="code">')
				yield 0, f'<pre class="code {lang}">' + dummyoutfile.getvalue() + '</pre>'
				yield 0, '</td></tr>'#</table>'

		class InlineHtmlFormatter(HtmlFormatter):
		    def wrap(self, source, outfile):
		        return self._wrap_code(source)

		    def _wrap_code(self, source):
		        yield 0, ''
		        for i, t in source:
		            yield i, t
		        yield 0, ''


		if '\n' in self.text or "block" in self.keys():
			type_ = "block"
			if "numbering" in self.keys():
				line_numbering = "table"
				self.attrib.pop("numbering", None)
				self.tag = "table"
				try:
					self.attrib["class"] += " highlighttable"
				except KeyError:
					self.attrib["class"] = "highlighttable"
			else:
				line_numbering = False
				self.tag = "pre"
				try:
					self.attrib["class"] += f" code {lang}"
				except KeyError:
					self.attrib["class"] = f"code {lang}"
		else:
			self.tag = "code"
			type_ = "inline"
			line_numbering = False
			try:
				self.attrib["class"] += " inline highlight"
			except KeyError:
				self.attrib["class"] = "inline highlight"

		#get the formatter(s)
		formatter = {
			"block": BlockHtmlFormatter(
				linenos       = line_numbering,
				linenostart   = 1, # start counting lineno from 1
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

		#print(self.text)


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
		self.text = self.text.strip('\n')

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
		global pathstack

		relative_path = self.attrib.pop("loc")
		path = pathstack / relative_path
		with open(path, mode='r') as ifile:
			import os
			if os.path.dirname(relative_path):
				pathstack / os.path.dirname(ifile.name)
			else: # if same folder
				pathstack / '.'

			try:
				parser = self.attrib.pop("parser")
			except KeyError:
				parser = "addup"

			template_root = {
				"addup" : Addup,
				"code"  : Code,
				"raw"   : Raw,
			}[parser]("root")
			template_root.attrib = self.attrib.copy() #buggy?
			template_root.text = ifile.read()
			template_root.parse()

			pathstack = pathstack.parent

			self.text = template_root.text
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

		return text

	def parse(self):
		path = pathstack / self.attrib.pop("src")
		try:
			_, ext = path.rsplit('.', 1)
			if ext == "svg":
				self.tag = "svg"
				svg_file = ET.parse(path).getroot()
				self.attrib.update(svg_file.attrib)
				self.attrib["height"] = "100%"
				self.attrib["width"]  = "100%"

				# this is not a general solution
				ns = {
					"": "http://www.w3.org/2000/svg",
					"xlink": "http://www.w3.org/1999/xlink",
				}

				# remove ns["0"] from tags
				for c in svg_file.iter():
					c.tag = c.tag.split('}', 1)[1]

				# remove ns["1"] from the href-attrib for use-tags
				for c in svg_file.iter("use"):
					c.attrib['href'] = c.attrib.pop(f'{{{ns["xlink"]}}}href')

				# proceed as usual
				for c in svg_file:
					self.append(c)

			else:
				self.tag = "img"
				with open(path, mode='rb') as img_file:
					import base64
					b64 = base64.b64encode(img_file.read()).decode("utf-8")
					self.set("src", f"data:image/png;base64,{b64}")
		except ValueError:
			self.tag = "img"
			pass #no '.' in path


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
		path = pathstack / self.attrib.pop("href")
		with open(path, mode='r') as css_file:
			self.text = css_file.read()

class JS(Node):
	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		super().__init__(tag, attrib.copy(), text, tail, **extra)

	eat_arguments = eat_arguments

	def eat(self, text):
		has_argument = re.compile(r"(?P<ARGUMENT>\()").match(text)
		if has_argument:
			text = self.eat_arguments(text)

		self.parse()
		self.tag = "script"

		return text

	def parse(self):
		path = pathstack / self.attrib.pop("src")
		with open(path, mode='r') as js_file:
			self.text = js_file.read()

class Date(Node):
	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		super().__init__(tag, attrib.copy(), text, tail, **extra)

	eat_arguments = eat_arguments

	def eat(self, text):
		has_argument = re.compile(r"(?P<ARGUMENT>\()").match(text)
		if has_argument:
			text = self.eat_arguments(text)

		self.tag = "time"
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
