#!/usr/bin/python -i
""" +^ [c] :: 47-06-16 | 47-08-02 """

## Imports

from addup.langs import *
from addup.blocks import *
import addup.filemanager as fm
import sys

#get file_name from terminal input
try:
	if sys.argv[1]:
		file_name = sys.argv[1][0:sys.argv[1].rfind('.')]
except IndexError:
	input("Input file is missing.")
	sys.exit()

#TAB or *SPACE
try:
	if sys.argv[2].lower() == 'tab':
		fm.INDENT = '\t'
	elif sys.argv[2][1:].lower() == 'space' or sys.argv[2][1:].lower() == 'spaces':
		fm.INDENT = int(sys.argv[2][0])*' '
except IndexError:
	print("Defaulting to tab.")
	fm.INDENT = '\t'
except ValueError:
	input("non-integer number of spaces.")
	sys.exit()

## Files to read/write
file_to_read  = f"{file_name}.add"
file_to_write = f"{file_name}.html"

with open(file_to_read, mode='r') as read_file, open(file_to_write, mode='w') as write_file:
	print("Translation started")

	#Wrap files in classes
	OFile = fm.Filewriter(write_file, indent = fm.INDENT)
	IFile = fm.Filereader(read_file, indent = fm.INDENT, offset = 0)

	#Define block type
	lang = Blank(I = IFile, O = OFile, block = wrapping_block, tag = None, attributes = {})

	#Start default interpreter
	lang.block()

	print("Translation completed")
