## Imports

import tags as TAGS
import custom_tags as CUSTOM
from filemanager import Filereader

## Tokens

TOKENS = {'+', '@', '[[', '//', '(', ')', '+('}
ESCAPE = '\\' #Python can't handle raw strings ending in \. r'\' results in error.

## The Interpreter

def default_interpreter(Read, Write):
	while "not EOF":
		line = Read.readline()
		
		if line.isspace(): continue #No need to check if line == ''; every line has at least \n (except last)
		if line.string == '': break #last line
		
		#get the indentation change
		indent_change = Read.indent_change(line.string)
		
		#pop off tags if no indent change
		if indent_change == 0 and Write.tag_in_line:
			Read.pop_inline()
		
		#newline (this comment is redundant)
		Write.newline()
		
		#pop off end tags if line is dedented relatively to last line
		if indent_change <= 0:
			Read.pop_tags()
			
		#remove leading space and endline
		line.lstrip()
		Write.indents(count = Read.indent_count)
			
		#generator that generates (index, token)-pairs
		token_index, token = line.match(ESCAPE, *TOKENS)
		while token:
			
			#pop off content before token, then pop token off to oblivion (as it's no longer needed)
			Write.write(line.pop_to(token_index))
			line.pop_to(len(token))
			
			#escape
			if token == '\\' and len(line) > 0:
				Write.write(line.pop_to(1))
				
			#newfile
			if token == '+(':
				line.pop_to(1)
				arg_index, arg = line.match('")')
				file_name = line.pop_to(arg_index)
				line.pop_to(len(arg))
				
				with open(file_name, mode='r') as read_file:
					#start
					print(f"Reading from {file_name}")
					
					indent_level = Read.indent_count
					nextRead = Filereader(read_file, Write, indent = '    ', indent_base = indent_level)

					#Start default interpreter
					default_interpreter(nextRead, Write)
				
			#tag
			elif token == '+' or token == '@':
				if line[0].isspace():
					Write.write('+')
					token_index, token = 0, ''
					continue
				
				parser = None
				brackets = False #bracketed content
				custom_tag = '' #customized tag as defined
				attributes = {} #dict of attributes (if any)
				
				#Check if arguments
				arg_index, arg = line.match('(', ' ', '\n')
				
				#tag
				tag = line.pop_to(arg_index)
				if arg != '\n':
					line.pop_to(len(arg))
				
				if tag in CUSTOM.TAGS:
					custom_tag = tag
					tag = CUSTOM.tag(tag)
				
				#check if tag is a html5 tag
				if tag not in TAGS.HTML5:
					input(f"Error: {tag} in line {Read.line_number} is not a HTML tag.")
					
				Write.write(f"<{tag}")
				
				#attributes
				if custom_tag in CUSTOM.TAGS:
					attributes = CUSTOM.attributes(custom_tag) or {} #empty if no attributes
				
				#check if attributes or bracketed content
				if arg == '(':
					if line.isspace():
						peekline = Read.peek_next()
						_, sym = peekline.match('=', '\\', ')')
					else:
						_, sym = line.match('=', '\\', ')')
					
					#not attributes, but content
					if sym != '=':
						brackets = True
						
					#The use of '=' means we have attributes, not content; add these to the attribute-dictionary
					elif sym == '=':
						#looks for '")'; this is safer than looking for ')'
						end_index, end = line.match(')')
						#Check if end is found and make sure that we didn't find the parenthesis inside a value
						while not end and (line.string.count('"')%2 == 0):
							line += Read.readline()
							end_index, end = line.match(')')

						attribute_string = line.pop_to(end_index)
						line.pop_to(len(end))

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

							#concatenate if in attribues, add otherwise
							if name in attributes:
								attributes[name] += f" {value}"
							else:
								attributes[name] = f"{value}"
				
				#write attributes if any
				if attributes:
					#write attributes
					for name, value in attributes.items():
						if value:
							Write.write(f' {name}="{value}"')
						else: #binary attribute
							Write.write(f' {name}')

				#checks if content is bracket-dependent or whitespace-dependent
				content_index, content = line.match('(')
				if content_index == 0 and content == '(':
					line.pop_to(len('('))
					brackets = True
				
				#text after brackets isn't necessarily indented
				if not brackets:
					Write.tag_in_line = True
				
				#close attributes:
				if tag in TAGS.SELFCLOSING:
					Write.write('/>')
					brackets = False #why would anyone do this tho
				else:
					Write.write('>')
					if brackets:
						Read.add_partag(tag)
					else:
						if token == '+':
							Read.add_tag(tag)
						elif token == '@':
							Read.add_container_tag(tag)
				
				#parser
				if custom_tag in CUSTOM.TAGS:
					#feels tacky
					parser_name = CUSTOM.parser(custom_tag)
					possibles = globals().copy()
					possibles.update(locals())
					parser = possibles.get(parser_name)
				elif tag in {"style", "script"}:
					#change parser
					parser = asis
					
				elif tag in {"pre"}:
					parser = pre
					
				if parser:
					if brackets: print("the interpreter can't handle bracketed content")
						
					#Move pointer back and reset line
					Read.file.seek(Read.file.tell()-len(line)-1)
					line.pop_to(-1)
					parser(Read, Write)
			
			elif token == '[[':
				token_end_index, token_end = line.match(']]')
				Write.write(line.pop_to(token_end_index))
				line.pop_to(len(token_end))
			
			#beginning bracket
			elif token == '(':
				Write.write(token)
				Read.add_parenthesis_to_partag()
			
			#if end bracket
			elif token == ')':
				#This is not always ')'
				Read.pop_partag()
			
			#comment
			elif token == '//':
				line.trim()
				Write.write(f"<!--{line.pop_to(len(line))}-->")
				Write.newline()
			
			#get next token
			token_index, token = line.match(ESCAPE, *TOKENS)
		
		line.rstrip()
		Write.write(line.string)
	
	#pop off remaining tags at EOF
	Write.newline()
	Read.indent_count = -1
	Read.pop_tags()
	
## Parse as is

def asis(Read, Write):
	"""Parses block as-is"""
	
	start_indentation = Read.indent_count + Write.tag_in_line
	
	#The rest of the line should be printed as it is
	line = Read.readline()
	Write.write(line.rstrip())
	pos = Read.file.tell()
	
	while "not EOBlock":
		line = Read.readline()
		if line.isspace(): continue #No need to check if line == ''; every line has at least \n (except last)
			
		indentation = (len(line)-len(line.lstrip())) // len(Read.indent)
		if indentation < start_indentation:
			break
		
		#new save-point
		pos = Read.file.tell()
		
		Write.newline()
		Write.indents(count=indentation)
		Write.write(line.trim())
		
	Read.file.seek(pos)
	
## Parse whitespace

def pre(Read, Write):
	pass