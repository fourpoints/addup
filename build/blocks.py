## +block
def indented_block(self):
	print("Indent-dependent block started")
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
				self.O.indents(count = block_indent)
			
	#Closing block
	if start_O_line != self.O.line_number:
		self.O.newline()
		self.O.indents(count = block_indent - 1)
	self.closing_tag()
	
	if self.offset:
		self.O.offset += block_indent
	
	print(f"Indent-dependent block was successfully printed")

## @wrapper:
def wrapping_block(self):
	print("Wrapping block started")
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
				self.O.indents(count = block_indent)
	
	#Closing block
	if start_O_line != self.O.line_number:
		self.O.newline()
		self.O.indents(count = block_indent)
	self.closing_tag()
	
	if self.offset:
		self.O.offset += block_indent
	
	print(f"Wrapping block was successfully printed")

## +block()
def bracketed_block(self):
	print("Bracketed block started")
	start_O_line = self.O.line_number
	block_indent = self.I.indent_count
	if self.offset:
		self.O.offset -= block_indent
	
	#Opening block
	self.opening_tag()
	
	#Main block loop FIX
	while 1:
		level = 0
		loop_line = self.I.line_number
		
		index, token = self.next_token('(', ')')
		self.O.write(self.I.popto(index))
		self.I.popto(len(token))
		print(self.I.line)
		if token == '(':
			level += 1
		elif token == ')':
			if level == 0:
				break #end of block
			level -= 1
		else:
			self.O.write(self.I.popto(index))
			self.I.popto(len(token))
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
				self.O.indents(count = block_indent)
		
	
	#Closing block
	self.closing_tag()
	
	if self.offset:
		self.O.offset += block_indent
	
	print(f"Bracketed block was successfully printed")
	
#Selfclosing pseudo-block
def selfclosing_block(self):
	self.opening_tag()
	print(f"Selfclosing tag was successfully printed")