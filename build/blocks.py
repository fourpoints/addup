"""
Blocks

TODO:
* Avoid newline/indent on certain tags, like Blank/Pre: self.__class__.__name__ != "Pre" (necessary?)
* Fixed: () popped len(token) twice
"""

## +block
def indented_block(self):
	print(f"Indent-dependent {self.tag} block started")
	start_O_line = self.O.line_number
	block_indent = self.I.indent_count + 1
	if self.offset:
		self.O.offset -= block_indent
	
	#Opening block
	self.opening_tag()
	
	#Main block loop
	while 1:
		loop_line = self.I.line_number
		
		index, token = self.next_token()
		if index > 0:
			self.O.indents(count = self.I.indent_count)
		self.O.write(self.I.popto(index))
		self.I.popto(len(token))
		if token:
			self.routine(token)
		
		#refill line
		if self.I.line == '':
			try:
				self.I.readline()
			except:
				break
		
		#check if next line is in block
		if loop_line != self.I.line_number:
			if block_indent > self.I.indent_count:
				break
			else:
				self.O.newline()
			
	#Closing block
	if start_O_line != self.O.line_number:
		self.O.newline()
		self.O.indents(count = block_indent - 1)
	self.closing_tag()
	
	if self.offset:
		self.O.offset += block_indent

## @wrapper:
def wrapping_block(self):
	print(f"Wrapping {self.tag} block started")
	start_O_line = self.O.line_number
	block_indent = self.I.indent_count
	if self.offset:
		self.O.offset -= block_indent
	
	#Opening block
	self.opening_tag()
	
	#Main block loop FIX
	while 1:
		loop_line = self.I.line_number
		
		index, token = self.next_token()
		if not token and index:
			self.O.indents(count = self.I.indent_count)
		self.O.write(self.I.popto(index))
		self.I.popto(len(token))
		if token:
			self.routine(token)
		
		#refill line
		if self.I.line == '':
			try:
				self.I.readline()
			except:
				break
		
		#check if next line is in block
		if loop_line != self.I.line_number:
			if block_indent > self.I.indent_count:
				break
			else:
				self.O.newline()
	
	#Closing block
	if start_O_line != self.O.line_number and self.__class__.__name__ != "Blank":
		self.O.newline()
		self.O.indents(count = block_indent)
	self.closing_tag()
	
	if self.offset:
		self.O.offset += block_indent

## +block()
def bracketed_block(self):
	print(f"Bracketed {self.tag} block started")
	start_O_line = self.O.line_number
	block_indent = self.I.indent_count
	if self.offset:
		self.O.offset -= block_indent
	
	#Opening block
	self.opening_tag()
	
	#Main block loop FIX
	level = 0 #number of brackets must match
	while 1:
		loop_line = self.I.line_number
		
		index, token = self.next_token('(', ')')
		if not token or token == '(' or token == ')':
			#indent will be added in the token's routine, if needed
			self.O.indents(count = self.I.indent_count)
		self.O.write(self.I.popto(index))
		self.I.popto(len(token))
		if token == '(':
			self.O.write('(')
			level += 1
		elif token == ')':
			if level == 0:
				break #end of block
			self.O.write(')')
			level -= 1
		else:
			self.O.write(self.I.popto(index))
			if token:
				self.routine(token)
			if self.I.line.isspace() or self.I.line == '':
				self.I.readline()
		
		#refill line
		if self.I.line == '':
			try:
				self.I.readline()
			except:
				break
		
		#check if next line is in block
		if loop_line != self.I.line_number:
			if block_indent > self.I.indent_count:
				break
			else:
				self.O.newline()
		
	
	#Closing block
	self.closing_tag()
	
	if self.offset:
		self.O.offset += block_indent
	
#Selfclosing pseudo-block
def selfclosing_block(self):
	print(f"Selfclosing {self.tag} tag started")
	self.opening_tag()