from .node import Document
from .builder import build
from .reshaper import shape
from .writer import ElementWriter


def _addup(root, text, **options):
    ### LOAD EXTENSIONS
    #extensions = options.get("extension")
    NotImplemented

    ### POST-PROCESSING
    # todo: fix formatting etc.

    ### BUILD TREE
    root = build(root, text, **options)

    ### POST-PROCESSING
    root = shape(root, **options)

    return root


def addup(file, out=None, **options):
    base = file.parent
    p = options.pop("pretty", False)
    print_options = dict(indent="  "*p, level=0, lsep="\n"*p, xml=False)

    root = Document()

    with open(file, mode="r", encoding="utf-8") as f:
        text = f.read()


    root = _addup(root, text, base=base)


    ### PRINT ELEMENTTREE TO FILE
    if out is not None:
        with open(out, mode="w", encoding="utf-8") as file:
            ElementWriter.write(file.write, root, **print_options)
    else:
        import sys
        ElementWriter.write(sys.stdout.write, root, **print_options)
