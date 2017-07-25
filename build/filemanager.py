from tags import is_selfclosing

INDENT = '\t' #or ' '*4

class EOF(Exception):
	""" End of file is reached """

class File:
	def __init__(self, file, indent):
		self.file = file
		self.indent = indent

class Filewriter(File):
	def __init__(self, file, indent = INDENT):
		super().__init__(file, indent)
		self.flipflop = '\n' #Flip between \n and \t
		self.indent_tag_in_line = False
		self.empty_line = True
		self.line_number = 0
		self.offset = 0
		self.indent_count = 0 #FIX
		
	def write(self, string):
		#if self.empty_line and string:
		#	self.indents(count = self.indent_count)
		#	self.empty_line = False
		self.file.write(string)
		
	def newline(self):
		if self.flipflop == '\t':
			self.flipflop = '\n'
			self.empty_line = True
			self.indent_tag_in_line = False
			self.line_number += 1
			self.file.write('\n')
	
	def indents(self, count):
		if self.flipflop == '\n':
			self.flipflop = '\t'
			self.file.write(self.indent*(count+self.offset))
			
class Filereader(File):
	def __init__(self, file, indent = INDENT):
		super().__init__(file, indent)
		#indentation for file
		self.indent_count = 0
		self.prev_indent_count = None
		self.line_number = 0
		self.line = ''
		self.offset = 0 #FIX
	
	def readline(self):
		while self.line.isspace() or self.line == '':
			self.line_number += 1
			self.line = self.file.readline()
			if self.line == '':
				raise EOF
		
		self.indent_change()
		#self.write_file.indent_count = self.indent_count FIX
		self.line = self.line.strip()
			
		return self.line
	
	def peekline(self):
		pos = self.file.tell()
		line = self.file.readline()
		self.file.seek(pos) #reset position
		return line
	
	def indent_change(self):
		self.prev_indent_count = self.indent_count
		print(self.indent)
		self.indent_count = (len(self.line)-len(self.line.lstrip())) // len(self.indent)
	
	def match(self, *tokens, line = None):
		if line is None: #HACKY
			line = self.line
		"""
		Returns <first and longest token> in line
		TODO: use <dict> with <len> as <key>
		"""
		sorted_tokens = sorted(tokens, key=len, reverse=True)
		for index in range(len(line)):
			for token in sorted_tokens:
				if line[index:index+len(token)] == token:
					return index, token
		#if none are found
		return len(line), ''
	
	def popto(self, n):
		substring, self.line = self.line[:n], self.line[n:]
		return substring
	
	def tagattr(self):
		"""
		This finds the TAG and ATTRIBUTES (if the latter exist).
		It also checks if content is bracketed.
		"""
		
		tag = None
		has_bracketed_content = False
		has_attributes = False
		attributes = {}
		
		index, end = self.match('(', ' ', '\n')
		tag = self.popto(index)
		self.popto(len(end))
		
		selfclosing = is_selfclosing(tag)
		
		if end == '(' and selfclosing:
			has_attributes = True
		
		#attributes OR content
		if end == '(' and not selfclosing:
			peekline = self.peekline()
			#Check if '=' is the first of the symbols on the current or next line. this indicates attrs.
			if self.match('=', '\\', ')', line = peekline)[1] == '=' and self.line.isspace() or self.match('=', '\\', ')')[1] == '=':
				has_attributes = True
			else:
				has_bracketed_content = True
		
		if has_attributes:
			#looks for '")'; this is safer than looking for ')'
			end_index, end = self.match(')')
			#Check if end is found and make sure that we didn't find the parenthesis inside a value
			while not end and (self.line.count('"')%2 == 0):
				self.readline()
				end_index, end = self.match(')')

			attribute_string = self.popto(end_index)
			self.popto(len(end))
			
			if self.line and self.line[0] == '(' and not selfclosing:
				has_bracketed_content = True

			#attributes are separated by a comma, may break if there's a hyperlink with a ','
			attribute_list = attribute_string.split(',')

			#add attributes 
			for attribute in attribute_list:
				if '=' in attribute:
					name, value = attribute.split('=', 1)
					name, value = name.strip(), value.strip()
				else: #binary attribute
					name, value = attribute.strip(), ''

				if value.startswith('"') and value.endswith('"'):
					value = value[1:-1]

				attributes[name] = value
		
		return tag, attributes, has_bracketed_content, selfclosing