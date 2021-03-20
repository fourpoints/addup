import argparse
from pathlib import Path
from .core import addup

def commandline_options():
    def check_valid_ext(filetype, valid_ext):
        def valid_file(file_path):
            path = Path(file_path)
            if path.suffix == valid_ext: return path
            raise argparse.ArgumentTypeError(f'{filetype} must have a {valid_ext} extension')
        return valid_file

    parser = argparse.ArgumentParser()
    parser.add_argument(dest="file",
        type=check_valid_ext("input file", ".add"), help='The source .add-file.')
    parser.add_argument("-f", "--out", default=None,
        type=check_valid_ext("output file", ".html"), help='The target .html-file.')
    parser.add_argument("-x", "--extension", nargs="*", default=[], help='Extensions (NotImplemented).')
    parser.add_argument("-p", "--pretty", default=False, action="store_true", help="Pretty readable printing.")

    options = parser.parse_args()
    options.out = options.out or options.file.with_suffix('.html')

    return vars(options)


if __name__ == "__main__":
    options = commandline_options()
    addup(**options)

