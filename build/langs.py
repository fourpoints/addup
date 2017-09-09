"""
Language interpreting classes.

TODO:
* This file is riddled with pasta. Make more parent classes where it's needed.
* Make attributes attach to last attribute in custom tags.
* Ignore closing tags for selfclosing tags in custom tags.
* A tags .au-attributes are ignored in custom tags if the attribute doesn't in its custom tag.
* Multiline attributes will use the indentation of the last attribute line.
* Ignore space after attributes
* def __init__(**kwargs, attributes = {}) does not create new dict for new calls (?)
"""
from .blocks import *
from .tags import *
from .filemanager import *
from functools import partial, update_wrapper

class Lang:
	def __init__(self, I, O, block, offset = 0, tag = None, attributes = {}):
		self.I = I #Input/read file
		self.O = O #Output/write file

		self.offset = False #Set to True if one wants to offset the block back to the base (0-indentation)

		self.tag = tag #this is a string
		self.attributes = attributes #this is a dictionary

		self.block = update_wrapper(partial(block, self), block) #defined in blocks.py; defines a method for the class.

# Languages

class Blank(Lang):
	def next_token(self, *args):
		return self.I.match(HTML.escape, HTML.newfile, *HTML.tokens, *args)

	def opening_tag(self):
		pass

	def closing_tag(self):
		pass

	def routine(self, token):
		if token == '+' or token == '@':
			tag, attributes, has_bracketed_content, selfclosing = self.I.tagattr()

			if tag == '': #empty tag
				self.O.indents(count = self.I.indent_count)
				self.O.write(token+' ')
				return

			Lang = getlang(tag)
			if selfclosing:
				lang = Lang(I = self.I, O = self.O,  block = selfclosing_block, tag = tag, attributes = attributes)
			elif has_bracketed_content:
				lang = Lang(I = self.I, O = self.O,  block = bracketed_block, tag = tag, attributes = attributes)
			else:
				if token == '+':
					lang = Lang(I = self.I, O = self.O,  block = indented_block, tag = tag, attributes = attributes)
				else: #if token == '@':
					lang = Lang(I = self.I, O = self.O,  block = wrapping_block, tag = tag, attributes = attributes)
			lang.block()

		elif token == "//":
			self.O.indents(count = self.I.indent_count)
			self.O.write(f"<!-- {self.I.popto(len(self.I.line)).strip()} -->")
		elif token == '+("':
			self.O.indents(count = self.I.indent_count)
			index, end = self.I.match('")')
			filename = self.I.popto(index)
			self.I.popto(len(end))
			with open(filename, mode='r') as read_file:
				IFile = Filereader(read_file, indent = INDENT, offset = self.I.indent_count)
				#Define block type
				lang = Blank(I = IFile, O = self.O, block = wrapping_block, tag = None, attributes = {})

				#Start default interpreter
				lang.block()
		elif token == '\\':
			self.O.write(self.I.popto(1))

class HTML(Lang):
	tokens = {'+', '@', '//'}
	newfile = '+("'
	escape = '\\'
	def __init__(self, **kwa):
		super().__init__(**kwa)

	def next_token(self, *args):
		return self.I.match(HTML.escape, HTML.newfile, *HTML.tokens, *args)

	def opening_tag(self):
		self.O.indents(count = self.I.indent_count)
		opening_tag = f"<{self.tag}"
		for name, value in self.attributes.items():
			if value:
				opening_tag += f' {name}="{value}"'
			else: #binary attribute
				opening_tag += f' {name}'

		if self.tag.lower() not in SELFCLOSING:
			opening_tag += '>'
		else:
			opening_tag += '>'
		self.O.write(opening_tag)

	def closing_tag(self):
		self.O.indents(count = self.I.indent_count)
		self.O.write(f'</{self.tag}>')

	def routine(self, token):
		if token == '+' or token == '@':
			tag, attributes, has_bracketed_content, selfclosing = self.I.tagattr()
			print(tag)

			if tag == '': #empty tag
				self.O.indents(count = self.I.indent_count)
				self.O.write(token+' ')
				return

			Lang = getlang(tag)
			if selfclosing:
				lang = Lang(I = self.I, O = self.O,  block = selfclosing_block, tag = tag, attributes = attributes)
			elif has_bracketed_content:
				lang = Lang(I = self.I, O = self.O,  block = bracketed_block, tag = tag, attributes = attributes)
			else:
				if token == '+':
					lang = Lang(I = self.I, O = self.O,  block = indented_block, tag = tag, attributes = attributes)
				else: #if token == '@':
					lang = Lang(I = self.I, O = self.O,  block = wrapping_block, tag = tag, attributes = attributes)
			lang.block()
		elif token == '//':
			self.O.indents(count = self.I.indent_count)
			self.O.write(f"<!-- {self.I.popto(len(self.I.line)).strip()} -->")
		elif token == '+("':
			self.O.indents(count = self.I.indent_count)
			index, end = self.I.match('")')
			filename = self.I.popto(index)
			self.I.popto(len(end))
			with open(filename, mode='r') as read_file:
				IFile = Filereader(read_file, indent = INDENT, offset = self.I.indent_count)
				#Define block type
				lang = Blank(I = IFile, O = self.O, block = wrapping_block, tag = None, attributes = {})

				#Start default interpreter
				lang.block()
		elif token == '\\':
			self.O.indents(count = self.I.indent_count)
			self.O.write(self.I.popto(1))

class CustomHTML(Lang):
	def __init__(self, **kwa):
		super().__init__(**kwa)
		self.offset = has_offset(self.tag)

	def next_token(self, *args):
		return self.I.match(HTML.escape, HTML.newfile, *HTML.tokens, *args)

	def opening_tag(self):
		"""pls rewrite, this is uglee"""
		if (not self.O.empty_line) and self.offset:
			self.O.newline()
		self.O.indents(count = self.I.indent_count)
		tags_and_attributes_from_json = get_tags_and_attributes_from_json(self.tag)
		first_tag = tags_and_attributes_from_json.pop(0)
		if "attributes" in first_tag:
			self.O.write(f'<{first_tag.get("html5tag")}')
			for name, value in first_tag["attributes"].items():
				if name in self.attributes and value:
					self.O.write(f' {name}="{value} {self.attributes[name]}"')
					self.attributes.pop(name)
				elif value:
						self.O.write(f' {name}="{value}"')
				else: #binary attribute
					self.O.write(f' {name}')
		else:
			self.O.write(f'<{first_tag.get("html5tag")}')

		for name, value in self.attributes.items():
			if value:
				self.O.write(f' {name}="{value}"')
			else: #binary attribute
				self.O.write(f' {name}')

		for tag in tags_and_attributes_from_json:
			if "attributes" in tag:
				self.O.write(f'<{tag.get("html5tag")}')
				for name, value in tag["attributes"].items():
					if value:
						self.O.write(f' {name}="{value}"')
					else: #binary attribute
						self.O.write(f' {name}')
			else:
				self.O.write(f'<{tag.get("html5tag")}')

		self.O.write('>')

	def closing_tag(self):
		self.O.indents(count = self.I.indent_count)
		for tag in reversed(get_tags_and_attributes_from_json(self.tag)):
			self.O.write(f'</{tag.get("html5tag")}>')

	def routine(self, token):
		if token == '+' or token == '@':
			tag, attributes, has_bracketed_content, selfclosing = self.I.tagattr()

			if tag == '': #empty tag
				self.O.indents(count = self.I.indent_count)
				self.O.write(token)
				return

			Lang = getlang(tag)
			if selfclosing:
				lang = Lang(I = self.I, O = self.O,  block = selfclosing_block, tag = tag, attributes = attributes)
			elif has_bracketed_content:
				lang = Lang(I = self.I, O = self.O,  block = bracketed_block, tag = tag, attributes = attributes)
			else:
				if token == '+':
					lang = Lang(I = self.I, O = self.O,  block = indented_block, tag = tag, attributes = attributes)
				else: #if token == '@':
					lang = Lang(I = self.I, O = self.O,  block = wrapping_block, tag = tag, attributes = attributes)
			lang.block()
		elif token == "//":
			self.O.indents(count = self.I.indent_count)
			self.O.write(f"<!-- {self.I.popto(len(self.I.line)).strip()} -->")
		elif token == '+("':
			self.O.indents(count = self.I.indent_count)
			index, end = self.I.match('")')
			filename = self.I.popto(index)
			self.I.popto(len(end))
			with open(filename, mode='r') as read_file:
				IFile = Filereader(read_file, indent = INDENT, offset = self.I.indent_count)
				#Define block type
				lang = Blank(I = IFile, O = self.O, block = wrapping_block, tag = None, attributes = {})

				#Start default interpreter
				lang.block()
		elif token == '\\':
			self.O.indents(count = self.I.indent_count)
			self.O.write(self.I.popto(1))

class CustomNonHTML(Lang):
	def __init__(self, **kwa):
		super().__init__(**kwa)
		self.offset = has_offset(self.tag)

	def next_token(self, *args):
		return self.I.match(*args)

	def opening_tag(self):
		"""pls rewrite, this is uglee"""
		if (not self.O.empty_line) and self.offset:
			self.O.newline()
		self.O.indents(count = self.I.indent_count)
		tags_and_attributes_from_json = None
		if self.block.__name__ == "bracketed_block":
			inline_tag = f"{self.tag}-inline"
			try:
				tags_and_attributes_from_json = get_tags_and_attributes_from_json(inline_tag)
			except KeyError:
				tags_and_attributes_from_json = get_tags_and_attributes_from_json(self.tag)
		else:
			tags_and_attributes_from_json = get_tags_and_attributes_from_json(self.tag)
		print(self.I.line_number)
		first_tag = tags_and_attributes_from_json.pop(0)
		if "attributes" in first_tag:
			self.O.write(f'<{first_tag.get("html5tag")}')
			for name, value in first_tag["attributes"].items():
				if name in self.attributes and value:
					self.O.write(f' {name}="{value} {self.attributes[name]}"')
					self.attributes.pop(name)
				elif value:
						self.O.write(f' {name}="{value}"')
				else: #binary attribute
					self.O.write(f' {name}')
		else:
			self.O.write(f'<{first_tag.get("html5tag")}')

		for name, value in self.attributes.items():
			if value:
				self.O.write(f' {name}="{value}"')
			else: #binary attribute
				self.O.write(f' {name}')

		for tag in tags_and_attributes_from_json:
			if "attributes" in tag:
				self.O.write(f'<{tag.get("html5tag")}')
				for name, value in tag["attributes"].items():
					if value:
						self.O.write(f' {name}="{value}"')
					else: #binary attribute
						self.O.write(f' {name}')
			else:
				self.O.write(f'<{tag.get("html5tag")}')

		self.O.write('>')

	def closing_tag(self):
		self.O.indents(count = self.I.indent_count)
		for tag in reversed(get_tags_and_attributes_from_json(self.tag)):
			self.O.write(f'</{tag.get("html5tag")}>')

	def routine(self, token):
		if token == '+' or token == '@':
			tag, attributes, has_bracketed_content, selfclosing = self.I.tagattr()

			if tag == '': #empty tag
				self.O.indents(count = self.I.indent_count)
				self.O.write(token)
				return

			Lang = getlang(tag)
			if selfclosing:
				lang = Lang(I = self.I, O = self.O,  block = selfclosing_block, tag = tag, attributes = attributes)
			elif has_bracketed_content:
				lang = Lang(I = self.I, O = self.O,  block = bracketed_block, tag = tag, attributes = attributes)
			else:
				if token == '+':
					lang = Lang(I = self.I, O = self.O,  block = indented_block, tag = tag, attributes = attributes)
				else: #if token == '@':
					lang = Lang(I = self.I, O = self.O,  block = wrapping_block, tag = tag, attributes = attributes)
			lang.block()
		elif token == "//":
			self.O.indents(count = self.I.indent_count)
			self.O.write(f"<!-- {self.I.popto(len(self.I.line)).strip()} -->")
		elif token == '+("':
			self.O.indents(count = self.I.indent_count)
			index, end = self.I.match('")')
			filename = self.I.popto(index)
			self.I.popto(len(end))
			with open(filename, mode='r') as read_file:
				IFile = Filereader(read_file, indent = INDENT, offset = self.I.indent_count)
				#Define block type
				lang = Blank(I = IFile, O = self.O, block = wrapping_block, tag = None, attributes = {})

				#Start default interpreter
				lang.block()
		elif token == '\\':
			self.O.indents(count = self.I.indent_count)
			self.O.write(self.I.popto(1))

class Pre(Lang):
	def __init__(self, **kwa):
		super().__init__(**kwa)
		self.offset = True

	def next_token(self, *args):
		return self.I.match(HTML.escape, HTML.newfile, *HTML.tokens, *args)

	def opening_tag(self):
		if not self.O.empty_line:
			self.O.newline()
		self.O.indents(count = self.I.indent_count)
		opening_tag = f"<{self.tag}"
		for name, value in self.attributes.items():
			if value:
				opening_tag += f' {name}="{value}"'
			else: #binary attribute
				opening_tag += f' {name}'

		if self.tag.lower() not in SELFCLOSING:
			opening_tag += '>'
		else:
			opening_tag += '>'
		self.O.write(opening_tag)

	def closing_tag(self):
		self.O.indents(count = self.I.indent_count)
		self.O.write(f'</{self.tag}>')

	def routine(self, token):
		if token == '+' or token == '@':
			tag, attributes, has_bracketed_content, selfclosing = self.I.tagattr()

			if tag == '': #empty tag
				self.O.indents(count = self.I.indent_count)
				self.O.write(token)
				return

			Lang = getlang(tag)
			if selfclosing:
				lang = Lang(I = self.I, O = self.O,  block = selfclosing_block, tag = tag, attributes = attributes)
			elif has_bracketed_content:
				lang = Lang(I = self.I, O = self.O,  block = bracketed_block, tag = tag, attributes = attributes)
			else:
				if token == '+':
					lang = Lang(I = self.I, O = self.O,  block = indented_block, tag = tag, attributes = attributes)
				else: #if token == '@':
					lang = Lang(I = self.I, O = self.O,  block = wrapping_block, tag = tag, attributes = attributes)
			lang.block()
		elif token == "//":
			self.O.indents(count = self.I.indent_count)
			self.O.write(f"<!-- {self.I.popto(len(self.I.line)).strip()} -->")
		elif token == '+("':
			self.O.indents(count = self.I.indent_count)
			index, end = self.I.match('")')
			filename = self.I.popto(index)
			self.I.popto(len(end))
			with open(filename, mode='r') as read_file:
				IFile = Filereader(read_file, indent = INDENT, offset = self.I.indent_count)
				#Define block type
				lang = Blank(I = IFile, O = self.O, block = wrapping_block, tag = None, attributes = {})

				#Start default interpreter
				lang.block()
		elif token == '\\':
			self.O.indents(count = self.I.indent_count)
			self.O.write(self.I.popto(1))

class Script(Lang):
	def __init__(self, **kwa):
		super().__init__(**kwa)

	def next_token(self, *args):
		return self.I.match(*args)

	def opening_tag(self):
		self.O.indents(count = self.I.indent_count)
		opening_tag = f"<{self.tag}"
		for name, value in self.attributes.items():
			if value:
				opening_tag += f' {name}="{value}"'
			else: #binary attribute
				opening_tag += f' {name}'

		if self.tag.lower() not in SELFCLOSING:
			opening_tag += '>'
		else:
			opening_tag += '>'
		self.O.write(opening_tag)

	def closing_tag(self):
		self.O.indents(count = self.I.indent_count)
		self.O.write(f'</{self.tag}>')

class CSS(Lang):
	def __init__(self, **kwa):
		super().__init__(**kwa)

	def next_token(self, *args):
		return self.I.match(*args)

	def opening_tag(self):
		self.O.indents(count = self.I.indent_count)
		opening_tag = f"<{self.tag}"
		for name, value in self.attributes.items():
			if value:
				opening_tag += f' {name}="{value}"'
			else: #binary attribute
				opening_tag += f' {name}'

		if self.tag.lower() not in SELFCLOSING:
			opening_tag += '>'
		else:
			opening_tag += '>'
		self.O.write(opening_tag)

	def closing_tag(self):
		self.O.indents(count = self.I.indent_count)
		self.O.write(f'</{self.tag}>')

class Jax(Lang):
	tokens = {'\\\\'}
	def __init__(self, **kwa):
		super().__init__(**kwa)

	def next_token(self, *args):
		return self.I.match(*Jax.tokens, *args)

	def routine(self, token):
		self.O.indents(count = self.I.indent_count)
		if token == '\\\\':
			tag, attributes, has_bracketed_content, selfclosing = self.I.tagattr()
			if "id" in attributes:
				label = attributes["id"]
				self.O.write(rf"\\\label{{{label}}}")
			else:
				self.O.write('\\\\')

	def opening_tag(self):
		tags = get_tags_and_attributes_from_json(self.tag)
		self.O.indents(count = self.I.indent_count)
		self.O.write(rf"\begin{{{tags[0].get('jaxtag')}}}")
		if "id" in self.attributes:
			label = self.attributes["id"]
			self.O.write(rf"\label{{{label}}}")

	def closing_tag(self):
		tags = get_tags_and_attributes_from_json(self.tag)
		self.O.indents(count = self.I.indent_count)
		self.O.write(rf"\end{{{tags[0].get('jaxtag')}}}")

class Python(Lang):
	def __init__(self, **kwa):
		super().__init__(**kwa)
		self.offset = True

	def next_token(self, *args):
		return self.I.match(*args)

	def opening_tag(self):
		if (not self.O.empty_line) and self.offset:
			self.O.newline()
		self.O.indents(count = self.I.indent_count)
		tags_and_attributes_from_json = get_tags_and_attributes_from_json(self.tag)
		first_tag = tags_and_attributes_from_json.pop(0)
		if "attributes" in first_tag:
			self.O.write(f'<{first_tag.get("html5tag")}')
			for name, value in first_tag["attributes"].items():
				if name in self.attributes and value:
					self.O.write(f' {name}="{value} {self.attributes[name]}"')
				elif value:
						self.O.write(f' {name}="{value}"')
				else: #binary attribute
					self.O.write(f' {name}')
			self.O.write('>')
		else:
			self.O.write(f'<{first_tag.get("html5tag")}>')

		for tag in tags_and_attributes_from_json:
			if "attributes" in tag:
				self.O.write(f'<{tag.get("html5tag")}')
				for name, value in tag["attributes"].items():
					if value:
						self.O.write(f' {name}="{value}"')
					else: #binary attribute
						self.O.write(f' {name}')
				self.O.write('>')
			else:
				self.O.write(f'<{tag.get("html5tag")}>')

	def closing_tag(self):
		self.O.indents(count = self.I.indent_count)
		for tag in reversed(get_tags_and_attributes_from_json(self.tag)):
			self.O.write(f'</{tag.get("html5tag")}>')

	def routine(self, token):
		pass
