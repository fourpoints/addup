# TODO (in future)
# - Split nodebuilder into separate modules. The idea would be to make it more easy to add new custom modules.
# - Refactor Addup(Node) so that it does not explicitly use children in .parse(), but loads them dynamically.
# - Factor out TAGMAP to post-processing

import xml.etree.ElementTree as ET
import textwrap
import mumath
import re

from pathlib import Path


pathstack : Path = None


# Allows for the exec() to be used to run code while compiling (experimental feature)
EXEC = False


# tag aliases
TAGMAP = {
	"fig-title" : "h4",
}


def eat_inline(node, text):
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
				inline_text, text = text[1:mo.start()], text[mo.end():]
				break
	else:
		print("Unmatched bracket for inline element")

	return inline_text, text

def eat_block(node, text):
	END = r'(?P<end>\n)(?=\S)'
	EOF = r'(?P<eof>\Z)'

	token = re.compile('|'.join((END, EOF)), re.M).search(text)

	block_text, text = text[:token.end()], text[token.end():]
	block_text = textwrap.dedent(block_text).strip()

	return block_text, text


def eat_arguments(node, text):
	"""
	gets the (parameters) appended to the +tag
	"""

	DEL = r'(?P<argend>\))|(?P<has_value>=)'
	ATTR = r'\s*(?P<attribute>[\w\-:\.#]+)\s*'
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
	"""
	gets the .classes and #ids appeneded to the +tag
	"""

	classifiers = re.compile(r"(?P<CLASSID>[\.#][\w\-]+)+").match(text)

	# first element will be empty string, then every other element will be a separator (. or #) with the succeeding element the class/id name.
	classifier_list = re.split("([\.#])", text[:classifiers.end()])

	classifier_iter = iter(classifier_list[1:])
	# groups two at a time
	classifier_tuples = zip(classifier_iter, classifier_iter)

	def extend_attribute(attribute, value):
		node.attrib.setdefault(attribute, []).append(value)

	for classifier_token, classifier_name in classifier_tuples:
		classifier_type = "id" if classifier_token == "#" else "class"
		extend_attribute(classifier_type, classifier_name)

	return text[classifiers.end():]


### --------    --------    --------    --------


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
		r"(?P<eof>\Z)", # End of string
	]

	# compile
	#sp = re.compile("|".join(map(re.escape, sub_patterns.keys())), re.M)
	sp = re.compile("|".join(sub_patterns.keys()), re.M)
	tp = re.compile("|".join(token_patterns), re.M)

	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		attrib = attrib.copy()
		tag = TAGMAP.get(tag, tag)
		super().__init__(tag, attrib, text, tail, **extra)

	eat_inline      = eat_inline           # (bracketed)
	eat_block       = eat_block            #     indented block
	eat_arguments   = eat_arguments        # (attribute="value")
	eat_classifiers = eat_classifiers      # .class#id

	nodes = {
		"addup" : lambda tag: {
				"style"  : Raw,
				"script" : Raw,
				"math"   : MathJax, # for mathjax, deprecated
				"read"   : Read, # for content loading, for backwards-comp.
				"content": Read,
				"image"  : Image,
				"css"    : CSS,
				"js"     : JS,
				"now"    : Date,

				"update" : mumath.UpdateContext, # for mumath, deprecated
				"clear"  : mumath.ClearContext, # for mumath, deprecated
			}.get(tag, Addup)(tag = tag),
		"code" : lambda tag: Code(tag = "template", token = tag),
		"math" : lambda tag: mumath.Math(tag = "math", token = tag),
		"comment" : lambda tag: Comment(tag = ET.Comment),
	}


	def eat(self, text):
		has_classifier = re.compile(r"(?P<CLASSID>[\.#][\w\-]+)+").match(text)
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
				edible_text, inedible_text = self.eat_inline(text)

			else: #block element
				edible_text, inedible_text = self.eat_block(text)

		else:
			edible_text, inedible_text = "", text

		return edible_text, inedible_text

	def parse(self, text):
		# Searches through tokens
		mo = Addup.tp.search(text)
		element_type = mo.lastgroup

		# text may be "" (empty)
		self.text, text = text[:mo.start()], text[mo.end():]

		# Add the text to the node
		self.text = Addup.sp.sub(lambda s: Addup.sub_patterns[s.group(0)], self.text)
		# \e -> e (remove \ from escaped elements)
		self.text = re.sub(r'\\(.)', r'\1', self.text)

		while element_type != "eof":
			tag = mo.group(element_type)

			child = self.nodes.get(element_type)(tag)

			if child is None:
				print(f"Unknown element type {element_type} encountered.")

			child_text, text = child.eat(text)
			child.parse(child_text)

			if isinstance(child, ET.Element):
				self.append(child)

			mo = Addup.tp.search(text)
			element_type = mo.lastgroup

			child.tail, text = text[:mo.start()], text[mo.end():]

			# Add the text to the node
			child.tail = Addup.sp.sub(lambda s: Addup.sub_patterns[s.group(0)], child.tail)
			child.tail = re.sub(r'\\(.)', r'\1', child.tail)


class Raw(Node):
	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		super().__init__(tag, attrib.copy(), text, tail, **extra)

	eat_inline = eat_inline
	eat_block = eat_block
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
				edible_text, inedible_text = self.eat_inline(text)

			else: #block element
				edible_text, inedible_text = self.eat_block(text)

		else:
			edible_text, inedible_text = "", text

		return edible_text, inedible_text

	def parse(self, text):
		self.text = text

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

		edible_text, inedible_text = text[:token.start()], text[token.end():]
		self.text = self.text.strip('\n')

		if "run" in self.keys():
			self.attrib.pop("run")
			if EXEC == True:
				exec(self.text)

		return edible_text, inedible_text


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


	def parse(self, text):
		from pygments import highlight
		from pygments.formatters import HtmlFormatter
		from pygments.formatters import NullFormatter

		lexer = self.getlexer()
		lang = lexer.aliases[0]

		class BlockHtmlFormatter(HtmlFormatter):
			def wrap(self, source, outfile):
			    return self._wrap_code(source)

			def _wrap_code(self, source):
			    yield 0, f'<code class="code">'
			    for i, t in source:
			        yield i, f'<span class="pyg__row">{t}</span>'
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
								'<tr><td><div class="pyg__linenodiv" '
								'style="background-color: #f0f0f0; padding-right: 10px">'
								'<pre style="line-height: 125%">' +
								ls + '</pre></div></td><td class="pyg__code">')
				else:
					yield 0, (#'<table class="%stable">' % self.cssclass +
								'<tr><td class="pyg__linenos"><div class="pyg__linenodiv"><pre>' +
								ls + '</pre></div></td><td class="pyg__code">')
				yield 0, f'<pre class="code code--block">' + dummyoutfile.getvalue() + '</pre>' #NOTE "code--{lang}" could be re-added
				yield 0, '</td></tr>'#</table>'

		class InlineHtmlFormatter(HtmlFormatter):
		    def wrap(self, source, outfile):
		        return self._wrap_code(source)

		    def _wrap_code(self, source):
		        yield 0, ''
		        for i, t in source:
		            yield i, t
		        yield 0, ''


		if '\n' in text or "block" in self.keys():
			# remove pseudo-attribute
			self.attrib.pop("block", None)

			type_ = "block"
			if "numbering" in self.keys():
				line_numbering = "table"
				self.attrib.pop("numbering", None)
				self.tag = "table"
				self.attrib.setdefault("class", []).append("pyg-table")
			else:
				line_numbering = False
				self.tag = "pre"
				self.attrib.setdefault("class", []).append(f"code code--block")
		else:
			self.tag = "code"
			type_ = "inline"
			line_numbering = False
			self.attrib.setdefault("class", []).append(f"code code--inline")

		#get the formatter(s)
		formatter = {
			"block": BlockHtmlFormatter(
				linenos       = line_numbering,
				linenostart   = 1, # start counting lineno from 1
				lineanchors   = f"no_anchor",
				lineseparator = "<br/>",
			),
			"inline": InlineHtmlFormatter(
				lineseparator = "",
			),
		}

		#formatted code
		self.text = highlight(
			code      = text,
			lexer     = lexer,
			formatter = formatter[type_],
		)


class MathJax(Node):
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

		END = rf'(?P<end>{re.escape(self.token)})'
		EOF = r'(?P<eof>\Z)'

		token = re.compile('|'.join((END, EOF)), re.M).search(text)

		edible_text, inedible_text = text[:token.start()], text[token.end():]

		return edible_text, inedible_text

	def parse(self, text):
		self.text = text.strip().replace('\n\n', r'\\')

		aligned = type(self.attrib.pop("align", 0)) is str

		if aligned:
			self.text = rf"\begin{{align*}}{self.text}\end{{align*}}"

		if '\n' in self.text:
			self.set("type", "math/tex; mode=display")
		else:
			self.set("type", "math/tex")


class Comment(Node):
	# substitution patterns
	sub_patterns = {
		"&": "&amp;",
		"<": "&lt;",
		">": "&gt;",
		"\\[^\\]": "",
	}

	def __init__(self, tag=ET.Comment, attrib={}, text="", tail="", **extra):
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

		edible_text, inedible_text = text[:token.start()], text[token.end():]

		return edible_text, inedible_text

	def parse(self, text):
		#There may be --> in text (?)
		self.text = text.strip('\n')


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

		return "", text

	def parse(self, text):
		"""text argument is unused"""
		global pathstack

		relative_path = self.attrib.pop("loc")
		path = pathstack / relative_path

		old_path = pathstack
		pathstack = path.parent
		with open(path, mode='r', encoding="utf-8") as ifile:
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

			template_root.parse(ifile.read())

			pathstack = old_path

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

		return "", text

	def parse(self, text):
		"""text argument is unused"""
		path = pathstack / self.attrib.pop("src")

		try:
			if path.suffix == ".svg":
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

		self.tag = "style"

		return "", text

	def parse(self, text):
		"""text argument is unused"""
		path = pathstack / self.attrib.pop("href")
		with open(path, mode='r', encoding="utf-8") as css_file:
			self.text = css_file.read()

class JS(Node):
	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		super().__init__(tag, attrib.copy(), text, tail, **extra)

	eat_arguments = eat_arguments

	def eat(self, text):
		has_argument = re.compile(r"(?P<ARGUMENT>\()").match(text)
		if has_argument:
			text = self.eat_arguments(text)

		self.tag = "script"

		return "", text

	def parse(self, text):
		"""text argument is unused"""
		path = pathstack / self.attrib.pop("src")
		with open(path, mode='r', encoding="utf-8") as js_file:
			self.text = js_file.read()

class Date(Node):
	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		super().__init__(tag, attrib.copy(), text, tail, **extra)

	eat_arguments = eat_arguments

	SUB = {
		"{year}" : "%Y",
		"{month}" : "%m",
		"{day}" : "%d",
		"{hr}" : "%H",
		"{min}" : "%M",
	}

	def eat(self, text):
		has_argument = re.compile(r"(?P<ARGUMENT>\()").match(text)
		if has_argument:
			text = self.eat_arguments(text)

		self.tag = "time"
		from datetime import datetime

		now = datetime.now()

		if "unix" in self.keys():
			self.attrib.pop("unix", None)
			now = now.replace(year=now.year-1970)


		if format := self.attrib.pop("format", None):
			for bracket, pct in Date.SUB.items():
				format = format.replace(bracket, pct)
		else:
			format = "%Y-%m-%d"

		# Only 4-digits years are supported;
		# earlier years are prepended with 0s.
		self.text = now.strftime(format).lstrip("0")
		self.set("datetime", now.strftime(format))

		return "", text

	def parse(self, text):
		"""text argument is unused"""
		pass


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

	def parse(self, text):
		pass
