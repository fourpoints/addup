#!/usr/bin/python -i
"""
File info
"""

import argparse
from pathlib import Path
import sys
try: # feels hacky
	from core import addup
except ImportError:
	from .core import addup

def commandline_options():
	def check_valid_ext(filetype, valid_ext):
		def valid_file(file_path):
			path = Path(file_path)
			if path.suffix == valid_ext: return path
			raise argparse.ArgumentTypeError(f'{filetype} must have a {valid_ext} extension')
		return valid_file

	parser = argparse.ArgumentParser()
	parser.add_argument(dest="infile",
		type=check_valid_ext("input file", ".add"), help='The input .add-file.')
	parser.add_argument("-f", "--outfile", default=None,
		type=check_valid_ext("output file", ".html"), help='The output .html-file.')
	parser.add_argument("-n", "--name", default=None, help='The name of the .html-file.')
	parser.add_argument("-b", "--base", default=None, help='The directory of the template bases.')
	parser.add_argument("-x", "--extension", nargs="*", default=None, help='Extensions (NotImplemented).')
	parser.add_argument("-p", "--pretty", default=True, action="store_false", help="Pretty readable printing.")

	options = parser.parse_args()
	options.name = options.name or options.infile.stem
	options.outfile = options.outfile or options.infile.with_suffix('.html')
	options.infile = options.infile or Path(options.name).with_suffix('.html')
	options.dir = options.infile.parent
	options.base = options.base or options.dir

	if options.extension is None: options.extension = []

	return vars(options)


if __name__ == "__main__":
	options = commandline_options()
	addup(**options)
