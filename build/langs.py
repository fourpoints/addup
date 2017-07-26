from blocks import *
from tags import *
from functools import partial

class Lang:
	def __init__(self, I, O, block, offset = 0, tag = None, attributes = {}):
		self.I = I #Input/read file
		self.O = O #Output/write file
		
		self.offset = False
		
		self.tag = tag
		self.attributes = attributes
		
		self.block = partial(block, self)

# Languages

class Blank(Lang):
	def next_token(self, *args):
		return self.I.match(HTML.escape, *HTML.tokens, *args)
	
	def opening_tag(self):
		pass
	
	def closing_tag(self):
		pass
	
	def routine(self, token):
		if token == "+":
			tag, attributes, has_bracketed_content, selfclosing = self.I.tagattr()
			#check if selfclosing
			
			Lang = getlang(tag)
			if selfclosing:
				lang = Lang(I = self.I, O = self.O,  block = selfclosing_block, tag = tag, attributes = attributes)
			elif has_bracketed_content:
				lang = Lang(I = self.I, O = self.O,  block = bracketed_block, tag = tag, attributes = attributes)
			else:
				lang = Lang(I = self.I, O = self.O,  block = indented_block, tag = tag, attributes = attributes)
			lang.block()
		elif token == "@":
			tag, attributes, has_bracketed_content, selfclosing = self.I.tagattr()
			#check if selfclosing
			
			Lang = getlang(tag)
			if selfclosing:
				lang = Lang(I = self.I, O = self.O,  block = selfclosing_block, tag = tag, attributes = attributes)
			elif has_bracketed_content:
				lang = Lang(I = self.I, O = self.O,  block = bracketed_block, tag = tag, attributes = attributes)
			else:
				lang = Lang(I = self.I, O = self.O,  block = wrapping_block, tag = tag, attributes = attributes)
			lang.block()
		elif token == "//":
			self.O.write(f"<!-- {self.I.popto(len(self.I.line))} -->")

class HTML(Lang):
	tokens = {"+", "@", "//"}
	escape = "\\"
	def __init__(self, **kwa):
		super().__init__(**kwa)
		
	def next_token(self, *args):
		return self.I.match(HTML.escape, *HTML.tokens, *args)
		
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
		if token == "+":
			tag, attributes, has_bracketed_content, selfclosing = self.I.tagattr()
			#check if selfclosing
			
			Lang = getlang(tag)
			if selfclosing:
				lang = Lang(I = self.I, O = self.O,  block = selfclosing_block, tag = tag, attributes = attributes)
			elif has_bracketed_content:
				lang = Lang(I = self.I, O = self.O,  block = bracketed_block, tag = tag, attributes = attributes)
			else:
				lang = Lang(I = self.I, O = self.O,  block = indented_block, tag = tag, attributes = attributes)
			lang.block()
		elif token == "@":
			tag, attributes, has_bracketed_content, selfclosing = self.I.tagattr()
			#check if selfclosing
			
			Lang = getlang(tag)
			if selfclosing:
				lang = Lang(I = self.I, O = self.O,  block = selfclosing_block, tag = tag, attributes = attributes)
			elif has_bracketed_content:
				lang = Lang(I = self.I, O = self.O,  block = bracketed_block, tag = tag, attributes = attributes)
			else:
				lang = Lang(I = self.I, O = self.O,  block = wrapping_block, tag = tag, attributes = attributes)
			lang.block()
		elif token == "//":
			self.O.indents(count = self.I.indent_count)
			self.O.write(f"<!-- {self.I.popto(len(self.I.line))} -->")

class CustomHTML(Lang):
	tokens = {"+", "@", "//"}
	escape = "\\"
	def __init__(self, tag, attributes = {}):
		super().__init__(tag, attributes = {})
		
class Pre(Lang):
	def __init__(self, **kwa):
		super().__init__(**kwa)
		self.offset = True
		
	def next_token(self, *args):
		return self.I.match(HTML.escape, *HTML.tokens, *args)
		
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
		if token == "+":
			tag, attributes, has_bracketed_content, selfclosing = self.I.tagattr()
			#check if selfclosing
			
			Lang = getlang(tag)
			if selfclosing:
				lang = Lang(I = self.I, O = self.O,  block = selfclosing_block, tag = tag, attributes = attributes)
			elif has_bracketed_content:
				lang = Lang(I = self.I, O = self.O,  block = bracketed_block, tag = tag, attributes = attributes)
			else:
				lang = Lang(I = self.I, O = self.O,  block = indented_block, tag = tag, attributes = attributes)
			lang.block()
		elif token == "@":
			tag, attributes, has_bracketed_content, selfclosing = self.I.tagattr()
			#check if selfclosing
			
			Lang = getlang(tag)
			if selfclosing:
				lang = Lang(I = self.I, O = self.O,  block = selfclosing_block, tag = tag, attributes = attributes)
			elif has_bracketed_content:
				lang = Lang(I = self.I, O = self.O,  block = bracketed_block, tag = tag, attributes = attributes)
			else:
				lang = Lang(I = self.I, O = self.O,  block = wrapping_block, tag = tag, attributes = attributes)
			lang.block()
		elif token == "//":
			self.O.indents(count = self.I.indent_count)
			self.O.write(f"<!-- {self.I.popto(len(self.I.line))} -->")

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
	def __init__(self, **kwa):
		super().__init__(**kwa)
		
	def next_token(self, *args):
		return self.I.match(*args)
		
	def opening_tag(self):
		self.O.indents(count = self.I.indent_count)
		self.O.write(r"\begin{equation}")
		if self.attributes.get("id"):
			label = self.attributes["id"]
			self.O.write(f"\\label{{{label}}}")
	
	def closing_tag(self):
		self.O.indents(count = self.I.indent_count)
		self.O.write(r"\end{equation}")