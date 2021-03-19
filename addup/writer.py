from .node import Element, Text, Comment, Document

EMPTY = {
	"area", "base", "basefont", "br", "col", "frame", "hr", "img", "input",
	"link", "meta", "param", "mprescripts", "none", "mspace", "isindex",
}

class ElementWriter:
    @classmethod
    def print(cls, *args, **kwargs):
        print(cls.tostring(*args, **kwargs))

    @classmethod
    def tostring(cls, el, indent="  ", level=0, lsep="\n", xml=False):
        import io
        stream = io.StringIO()

        cls.write(stream.write, el, indent, level, lsep, xml)

        return stream.getvalue()

    @classmethod
    def write(cls, write, el, indent="  ", level=0, lsep="\n", xml=False):
        if el.tag == Document:
            for child in el:
                cls._write(write, child, indent, level, lsep, xml)
        else:
            cls._write(write, el, indent, level, lsep, xml)

    @staticmethod
    def _attribute(attribute, value, xml):
        if value is not None:
            return ' {a}="{v}"'.format(a=attribute, v=value)
        elif xml:
            return ' {a}=""'.format(a=attribute)
        else:
            return ' {a}'.format(a=attribute)

    @classmethod
    def _attributes(cls, el, xml=False):
        return "".join(cls._attribute(a, v, xml) for a, v in el.items())

    @classmethod
    def _write(cls, write, el, indent, level, lsep, xml):
        if el.tag is Text:
            for line in el.text.splitlines():
                write(indent*level + f"{line}" + lsep)

        elif el.tag is Comment:
            write(indent*level + f"<!-- {el.text.strip()} -->" + lsep)

        elif isinstance(el, Element):
            attributes = cls._attributes(el)

            ltag = el.tag.lower()

            if ltag in EMPTY:
                write(indent*level + f'<{el.tag}{attributes}/>' + lsep)

            elif ltag == "pre":
                write(indent*level + f'<{el.tag}{attributes}>')
                for child in el:
                    cls._write(write, child, "", level+1, lsep="", xml=xml)
                write(f'</{el.tag}>' + lsep)

            elif ltag in {"svg", "math"}:
                write(indent*level + f'<{el.tag}{attributes}>' + lsep)
                for child in el:
                    cls._write(write, child, indent, level+1, lsep, xml=True)
                write(indent*level + f'</{el.tag}>' + lsep)

            elif ltag == "doctype":
                write(indent*level + f'<!{el.tag.upper()}{attributes}>' + lsep)

            else:
                write(indent*level + f'<{el.tag}{attributes}>' + lsep)
                for child in el:
                    cls._write(write, child, indent, level+1, lsep, xml)
                write(indent*level + f'</{el.tag}>' + lsep)

        else:
            global ET
            import xml.etree.ElementTree as ET

            cls._fallback_writer(write, el, indent, level, lsep, xml)

    @classmethod
    def _fallback_writer(cls, write, el, indent, level, lsep, xml):

        attributes = cls._attributes(el)

        ltag = el.tag.lower()

        if ltag in EMPTY:
            write(indent*level + f'<{el.tag}{attributes}/>' + lsep)

        write(indent*level + f'<{el.tag}{attributes}>' + lsep)
        if el.text:
            write(indent*level + el.text + lsep)
        if len(el) != 0:
            for child in el:
                cls._fallback_writer(write, child, indent, level+1, lsep, xml)
            write(indent*level + child.tail + lsep)

        write(indent*level + f'</{el.tag}>' + lsep)
