import xml.etree.ElementTree as ET

Comment = ET.Comment


def Text(text=None):
    """Copied ET.Comment implementation"""
    element = ET.Element(Text)
    element.text = text
    return element


def Document():
    """Copied ET.Comment implementation"""
    return Element(Document)


def _disabled_attribute(*args, **kwargs): raise AttributeError
class Element(ET.Element):
    # What is LSP?
    tail = property(_disabled_attribute)
    text = property(_disabled_attribute)

    def __init__(self, tag, attrib={}, **extra):
        # BUG cannot accept tag=tag
        super().__init__(tag, attrib=attrib, **extra)

    @property
    def attributes(self):
        return self.attrib
