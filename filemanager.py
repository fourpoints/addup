INDENT = '\t' #alternatively INDENT = ' '*4 or whatever

class File:
	def __init__(self, file, indent):
		self.file = file
		self.indent = indent

class Filereader(File):
	def __init__(self, file, writefile, indent = INDENT, indent_base = 0):
		super().__init__(file, indent)
		self.writefile = writefile
		
		#indentation for file
		self.indent_base = indent_base
		self.indent_count = indent_base
		self.prev_indent_count = None
		self.line_number = 0
		
		#{dict with indentation as key: [list of tags]}
		self.tabclosing_tags = {}
		self.parclosing_tags = []
		
	def __next__(self):
		for line in self.file:
			self.line_number += 1
			return Line(self.indent_base*self.indent + line)
		raise StopIteration
	
	def __iter__(self):
		return self
	
	def readline(self):
		self.line_number += 1
		return Line(self.file.readline())
	
	def peek_next(self):
		pos = self.file.tell()
		line = self.file.readline()
		self.file.seek(pos) #reset position
		return Line(line)
	
	def indent_change(self, line):
		self.prev_indent_count = self.indent_count
		self.indent_count = (len(line)-len(line.lstrip())) // len(self.indent)
	
	def add_tag(self, tag):
		self.tabclosing_tags.setdefault(self.indent_count, []).append(f"</{tag}>")
		
	def add_container_tag(self, tag):
		self.tabclosing_tags.setdefault(self.indent_count-1, []).append('\t'*max(self.indent_count, 0)+f"</{tag}>")
	
	def add_partag(self, tag):
		self.parclosing_tags.append(f"</{tag}>")
	def add_parenthesis_to_partag(self):
		self.parclosing_tags.append(')')
		
	def pop_tags(self):
		popping = sorted([key for key in self.tabclosing_tags if key >= self.indent_count], reverse=True)
		for key in popping:
			tags = self.tabclosing_tags.pop(key)
			for tag in reversed(tags):
				self.writefile.indents(count = key) #readfiles may have different indentations
				self.writefile.write(tag)
				self.writefile.newline()
				
	def pop_inline(self):
		#Uses indent_change to get back to the previous line's indentation to pop off
		#the previous line's tags
		tags = self.tabclosing_tags.pop(self.prev_indent_count, []) #
		for tag in reversed(tags):
			self.writefile.write(tag)
	
	def pop_partag(self):
		self.writefile.write(self.parclosing_tags.pop())
	
class Filewriter(File):
	def __init__(self, file, indent = INDENT):
		super().__init__(file, indent)
		#\n\t-flipflop;
		self.nt = '\n'
		self.tag_in_line = False
	
	#remove?
	def move_anchor(self, indent_change):
		self.anchor += indent_change
	
	def write(self, string):
		self.file.write(string)
		
	def newline(self):
		if self.nt == '\t':
			self.nt = '\n'
			self.tag_in_line = False
			self.write('\n')
	
	def indents(self, count):
		if self.nt == '\n':
			self.nt = '\t'
			self.write(self.indent*count)
				
class Line:
	def __init__(self, string):
		self.string = string
	
	def __iadd__(self, string):
		self.string += string.string
		return self #return is broken
	
	def __getitem__(self, slice):
		return self.string[slice]
	
	def __str__(self):
		return f"Line: {self.string}"
	
	def __len__(self):
		return len(self.string)
	
	def trim(self):
		self.string = self.string.strip()
		return self.string
	
	def lstrip(self):
		self.string = self.string.lstrip()
		return self.string
	
	def rstrip(self):
		self.string = self.string.rstrip()
		return self.string
	
	def isspace(self):
		return self.string.isspace()
	
	def pop_to(self, val):
		substring, self.string = self.string[:val], self.string[val:]
		return substring
	
	#remove?
	def prepend(self, string):
		self.string = string + self.string
	
	def match(self, *tokens):
		"""
		Returns <first and longest token> in line. If no token is found <False> is returned
		TODO: use <dict> with <len> as <key>
		"""
		sorted_tokens = sorted(tokens, key=len, reverse=True)
		for index in range(len(self.string)):
			for token in sorted_tokens:
				if self.string[index:index+len(token)] == token:
					return index, token
		#if no token is found
		return len(self.string), ''