""" +^ [c] :: 47-06-16 | 47-07-24 """

## Imports

import time
from langs import *
from blocks import *
from filemanager import *

TX = "program is running fine so far"

## Files to read/write

file_to_read  = "drop.au"
file_to_write = "drop.html"

with open(file_to_read, mode='r') as read_file, open(file_to_write, mode='w') as write_file:

	print("Translation started")
	a = time.time()
	
	#Wrap files in classes
	OFile = Filewriter(write_file)
	IFile = Filereader(read_file)
	
	#Define block type
	lang = Blank(I = IFile, O = OFile, block = wrapping_block, tag = None, attributes = {})
	
	#Start default interpreter
	lang.block()
	b = time.time()
	print(b-a)
	input("Translation completed")