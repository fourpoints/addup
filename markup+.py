"""
Markplus/Kwik-E-Mark/QuickMarkup
[c] 47-06-16
"""

## Imports

from filemanager import Filereader, Filewriter, Line
from interpreters import default_interpreter, asis, pre

TX = "program is running fine so far"

## Files to read/write

file_to_read  = "foo.m+"
file_to_write = "foo.html"

with open(file_to_read, mode='r') as read_file, open(file_to_write, mode='w') as write_file:
	#start
	print("Translation started")
	
	Write = Filewriter(write_file)
	Read = Filereader(read_file, Write, indent = '  ')
	
	#HTML5
	#Write.write("<!DOCTYPE html>\n")
	
	#Start default interpreter
	default_interpreter(Read, Write)
	
	#complete
	input("Translation completed")