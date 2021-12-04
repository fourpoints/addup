from .node import Document
from .builder import build
from .reshaper import shape
from .writer import ElementWriter


def _addup(root, text, **options):
    ### LOAD EXTENSIONS
    # extensions = options.get("extension")
    # NotImplemented

    ### POST-PROCESSING
    # fix formatting etc.

    ### BUILD TREE
    root = build(root, text, **options)

    ### POST-PROCESSING
    root = shape(root, **options)

    return root


class Addup:
    def __init__(self, **options):
        self.options = options
        self.root = Document()

    @property
    def print_options(self):
        n = self.options.pop("pretty", False)
        return {"indent":"   "*n, "level": 0, "lsep": "\n"*n, "xml": False}

    def convert(self, text, **options):
        self.root = _addup(self.root, text, **options)

    def convert_file(self, file, output, encoding="utf-8"):
        with open(file, mode="r", encoding=encoding) as f:
            text = f.read()

        self.convert(text, base=file.parent)

        if output is not None:
            self.write(output, encoding)
        else:
            self.print()

    def write(self, output, encoding="utf-8"):
        with open(output, mode="w", encoding=encoding) as file:
            ElementWriter.write(file.write, self.root, **self.print_options)

    def print(self):
        import sys
        ElementWriter.write(sys.stdout.write, self.root, **self.print_options)
