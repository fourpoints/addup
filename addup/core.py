from .node import Document
from .builder import build
from .reshaper import shape
from .writer import ElementWriter


def addup(**options):
    filename = options["file"]
    out = options["out"]
    root = Document()

    with open(filename, mode="r", encoding="utf-8") as f:
        text = f.read()


    ### LOAD EXTENSIONS
    #extensions = options.get("extension")
    NotImplemented

    ### POST-PROCESSING
    # todo: fix formatting etc.

    ### BUILD TREE
    root = build(root, text, base=filename.parent)

    ### POST-PROCESSING
    root = shape(root)


    p = options.get("pretty")
    print_options = dict(indent="  "*p, level=0, lsep="\n"*p, xml=False)

    ### PRINT ELEMENTTREE TO FILE
    # import sys
    # ElementWriter.write(sys.stdout.write, root, **print_options)
    with open(out, mode="w", encoding="utf-8") as file:
        ElementWriter.write(file.write, root, **print_options)
