#!/usr/bin/python -i
"""
File info
"""

import argparse
import os.path
import sys
from core import addup

def commandline_options():
	def check_valid_ext(filetype, valid_ext):
		def valid_file(file_):
			base, ext = os.path.splitext(file_)
			if ext == valid_ext: return base
			raise argparse.ArgumentTypeError(f'{filetype} must have a {valid_ext} extension')
		return valid_file

	parser = argparse.ArgumentParser()
	parser.add_argument(dest="infile",
		type=check_valid_ext("input file", ".add"), help='The input .add-file.')
	parser.add_argument("-f", "--outfile", default=None,
		type=check_valid_ext("output file", ".html"), help='The output .html-file.')
	parser.add_argument("-x", "--extension", nargs="*", default=None, help='Extensions (NotImplemented).')

	options = parser.parse_args()
	options.outfile = f"{options.outfile or options.infile}.html"
	options.infile = f"{options.infile}.add"
	if options.extension is None: options.extension = []

	return vars(options)


if __name__ == "__main__":
	options = commandline_options()
	addup(**options)
