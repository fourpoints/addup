import re
import textwrap
from pathlib import Path
from html import escape as html_escape
from .node import Element, Text, Comment, Document


# to-do
# html_escape for < and > (not &)


def build(el, text, **kwargs):
    Addup.parse_content(el, text, **kwargs)
    Math.counter = 0
    return el


def treebuilder(file_path: Path, **options) -> Element:
    file_path = Path(file_path)
    base = file_path.parent

    # use io.String or memoryview or mmap?
    with open(file_path, mode="r", encoding="utf-8") as file:
        text = file.read()

    root = Element(tag="DOCUMENT")
    Addup.parse_content(root, text, base=base)

    return root


class ContentParser:
    pass


class Bracket(ContentParser):
    @staticmethod
    def content(text, open="(", close=")"):
        # ESC = r'(?P<escape>\\)'
        OPEN = rf'(?P<open>[{open}])'
        CLOSE = rf'(?P<close>[{close}])'
        QUOTE = r'(?P<quote>")'

        tokens = re.compile('|'.join((OPEN, CLOSE, QUOTE))).finditer(text)

        bracket_count = 0
        in_quotes = False
        for mo in tokens:
            type_ = mo.lastgroup
            if type_ == "quote":
                in_quotes = not in_quotes

            elif type_ == "open" and not in_quotes:
                bracket_count += 1

            elif type_ == "close" and not in_quotes:
                bracket_count -= 1

                if bracket_count == 0:
                    # We start from 1 because we don't want the opening bracket
                    return text[1:mo.start()], text[mo.end():]
        else:
            if bracket_count == 0:
                return text, ""
            else:
                raise SyntaxError("Unmatched bracket for bracketed text:\n{text}".format(text=text))


class Block(ContentParser):
    @staticmethod
    def content(text):
        text, trail = Fence.content(text, r'(?P<break>\n)(?=\S)')

        return textwrap.dedent(text).strip(), trail


class Fence(ContentParser):
    @staticmethod
    def content(text, fence):
        if match := re.search(fence, text):
            block_text, text = text[:match.start()], text[match.end():]
            return block_text, text
        else:
            return text, ""


def _attributes(text):
    # superset of attributes
    a = r'(?P<attrib>[\w:!.#-]+)'
    vq = r'=\s*[\'"](?P<quoted>.*)[\'"]'
    v = r'=\s*(?P<unquoted>\S*)'

    tokens = re.finditer('|'.join((a, vq, v)), text)

    att = None
    for m in tokens:
        t = m.lastgroup
        if t == "attrib":
            if att is not None:
                yield att, None
            att = m.group(t)
        else:
            yield att, m.group(t)
            att = None
    if att is not None:
        yield att, None


def attributes(text):
    pair = r'(?P<attribute>[\w:.#-]+)\s*=\s*"(?P<value>.*?)"'
    binary = r'(?P<binary>[\w:.#-]+)'

    tokens = re.finditer('|'.join((pair, binary)), text)

    for m in tokens:
        type_ = m.lastgroup
        if type_ == "value":
            yield (m["attribute"], m["value"])
        elif type_ == "binary":
            yield (m["binary"], None)


def parse_attributes(node, text):
    """
    gets attributes inside ()
    """
    if text == "" or text[0] != "(":
        return text

    text, trail = Bracket.content(text)

    for attribute, value in attributes(text):
        node.set(attribute, value)

    return trail


def classifiers(text):
    patterns = {
        "class" : r"\.(?P<class>[\w\-]+)",
        "id"    : r"#(?P<id>[\w\-]+)",
    }

    for key, pattern in patterns.items():
        yield (key, " ".join(re.findall(pattern, text)))


def parse_classifiers(node, text):
    """
    gets the .classes and #ids appeneded to the +tag
    """

    # find ( or : instead
    m = re.compile(r"([\.#][\w\-]+)*").match(text)

    text, trail = text[:m.end()], text[m.end():]

    for attribute, value in classifiers(text):
        if value:
            node.set(attribute, value)

    return trail


def parse_fence_attributes(node, text):
    # please refactor me
    if text == "":
        return text

    has_newline = "\n" in text

    if has_newline:
        node.set("multiline", True)

    if has_newline and text[0] != "(":
        text, trail = text.split("\n", maxsplit=1)
    elif text[0] == "(":
        text, trail = Bracket.content(text)
    else:
        return text

    attributes = _attributes(text)

    fatt, fval = next(attributes, (None, None))

    LANG_ALIAS = {
        # TODO check if these are necessary
        "py": "python3",
		"js": "javascript",
    }

    ATT_ALIAS = {
        "#": "linenos",
        "!": "hl_lines",
        "@": "lineanchors",
    }

    # TODO
    # inline|block|table?
    # use * style="white-space:nowrap"?

    if fval is None:
        # Assume first attribute is language if first value is None
        node.set("lang", LANG_ALIAS.get(fatt, fatt))
    else:
        node.set(ATT_ALIAS.get(fatt, fatt), fval)

    for att, val in attributes:
        node.set(ATT_ALIAS.get(att, att), val)

    if "linenos" in node.attrib:
        node.set("linenostart", node.get("linenos") or 1)
        node.set("linenos", True)

    return trail


class TreeBuilder:
    head_pattern: str
    tail_pattern: str
    sub_pattern: str

    contexts = {}
    heads = None

    @classmethod
    def register(cls, contexts):
        for ctx in contexts:
            cls.contexts[ctx.__name__.lower()] = ctx

    @classmethod
    def compile(cls):
        heads = [ctx.head_pattern for ctx in cls.contexts.values()]

        # we need to match ^ with start of lines
        cls.heads = re.compile("|".join(heads), re.MULTILINE)

    @classmethod
    def parse(cls, parent, tag, text, **kwargs):
        pass

    def parse_head(self, text):
        # reads +tag(): part
        pass

    def parse_content(self, el, text):
        # reads content part, after : or between ()
        pass


class Addup(TreeBuilder):
    head_pattern = r"(?=^|[^\\])\+(?P<addup>[\w\-]+)"
    # sub_patterns = {
    #     "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;",  # html.escape
    #     r'\\(.)': r'\1', # \e -> e (remove \ from escaped elements)
    # }

    elements = {}

    @classmethod
    def register_element(cls, elements):
        for element in elements:
            cls.elements[element.__name__.lower()] = element

    @staticmethod
    def _remove_escape(text):
        return re.sub(r'\\(.)', r'\1', text)

    @classmethod
    def _parse(cls, parent, tag, text, **kwargs):
        el = Element(tag=tag)
        text = cls.parse_head(el, text)

        if text == "":
            text, trail = "", text
        elif text[0] == ":":
            if text[1] == "(":
                text, trail = Bracket.content(text[1:])
            else:
                text, trail = Block.content(text[1:])
        else: # empty element
            text, trail = "", text

        cls.parse_content(el, text, **kwargs)
        parent.append(el)

        return trail

    @classmethod
    def parse(cls, parent, tag, text, **kwargs):
        element = cls.elements.get(tag, Addup)

        return element._parse(parent, tag, text, **kwargs)


    @staticmethod
    def parse_head(el, text):
        text = parse_classifiers(el, text)
        text = parse_attributes(el, text)
        return text

    @classmethod
    def parse_content(cls, el, text, **kwargs):
        while match := cls.heads.search(text):
            text, tail = text[:match.start()], text[match.end():]

            if text: el.append(Text(text))

            name = match.lastgroup
            fence = match.group(name)
            ctx = cls.contexts[name]

            text = ctx.parse(el, fence, tail, **kwargs)

        if text: el.append(Text(text))


class Timepoint(Addup):
    @classmethod
    def parse_head(cls, el, text):
        from .formatters.timepoint import TimepointFormatter

        el.tag = "time"
        text = super().parse_head(el, text)

        timepoint = el.attrib.pop("format")

        tp = TimepointFormatter.now()
        time = tp.strftime(timepoint)

        el.set("datetime", time)
        el.append(Text(time))

        return text


class Source(Addup):
    tag: str
    attributes: dict
    path: str
    # suffixes: {str}  # TODO check that suffix(es) matches?

    @classmethod
    def parse_content(cls, el, text, **kwargs):
        el.tag = cls.tag
        for k, v in cls.attributes.items():
            el.set(k, v)
        el.append(Text(cls._read(cls._path(el, **kwargs))))

    @classmethod
    def _path(cls, el, base, **kwargs):
        return base / el.attrib.pop(cls.path)

    @staticmethod
    def _read(path, **kwargs):
        with open(path, mode='r', encoding="utf-8") as file:
            return file.read()


class CSS(Source):
    tag = "style"
    attributes = {"rel": "stylesheet"}
    path = "href"


class JS(Source):
    tag = "script"
    attributes = {}
    path = "src"



class Unformatted(Addup):
    @classmethod
    def parse_content(cls, el, text, **kwargs):
        el.append(Text(text))


class Style(Unformatted):
    pass


class Script(Unformatted):
    pass


class Code(TreeBuilder):
    head_pattern = r"(?=^|[^\\])(?P<code>`+)"

    @staticmethod
    def parse_head(el, text):
        text = parse_fence_attributes(el, text)

        return text

    @classmethod
    def parse_content(cls, el, text, **kwargs):
        from pygments.lexers import get_lexer_by_name
        from pygments.lexers.special import TextLexer
        from pygments.util import ClassNotFound
        from .formatters.code import ElementFormatter, treehighlight

        keys = (
            "lang", "wrap", "linenos", "linenostart",
            "hl_lines", "lineanchor", "multiline",
        )

        attrib = el.attrib
        options = {key: attrib.pop(key) for key in keys if key in attrib}

        if "multiline" not in options:
            options["wrap"] = "inline"

        try:
            lang = options.get("lang") or kwargs.get("code_lang")
            lexer = get_lexer_by_name(lang)
        except ClassNotFound:
            lexer = TextLexer()

        formatter = ElementFormatter(**options)

        treehighlight(code=text, lexer=lexer, formatter=formatter, root=el)

    @classmethod
    def parse(cls, parent, tag, text, **kwargs):
        text, trail = Fence.content(text, tag)

        el = Element(tag=None)
        text = cls.parse_head(el, text)
        cls.parse_content(el, text)

        el[0].attrib.update(el.attrib)
        parent.append(el[0])

        return trail


class Math(TreeBuilder):
    head_pattern = r"(?=^|[^\\])(?P<math>\$+)"
    counter = 0

    @staticmethod
    def parse_head(el, text):
        text = parse_fence_attributes(el, text)

        return text

    @classmethod
    def parse_content(cls, el, text, **kwargs):
        from .formatters.mumath import MathParser

        keys = (
            "lang", "wrap", "linenos", "linenostart", "hl_lines",
            "lineanchor", "multiline", "numbering", "align"
        )

        attrib = el.attrib
        options = {key: attrib.pop(key) for key in keys if key in attrib}

        options["area"] = options["lang"]

        if "multiline" in options:
            options["align"] = options.pop("multiline", False)

        if "linenos" in options:
            options["linenostart"] = cls.counter + 1

            mp = MathParser(**options)
            mp.parse(text=text, root=el)

            lines = el.find("mtable")
            cls.counter += len(lines)
        else:
            mp = MathParser(**options)
            mp.parse(text=text, root=el)


    @classmethod
    def parse(cls, parent, tag, text, **kwargs):
        # we must escape $$ because it matches string end
        text, trail = Fence.content(text, re.escape(tag))

        el = Element(tag="math")
        text = cls.parse_head(el, text)
        cls.parse_content(el, text)

        # el.attrib.update(el.attrib)
        parent.append(el)

        return trail


class InlineComment(TreeBuilder):
    head_pattern = r"(?=^|[^\\])(?P<inlinecomment>//)"

    @staticmethod
    def parse(parent, tag, text, **kwargs):
        if "\n" in text:
            comment, text = text.split("\n", maxsplit=1)
        else:
            comment, text = text, ""

        parent.append(Comment(comment))

        return text


class Image(Addup):
    @staticmethod
    def _prefix(tree, namespaces):
        uri_prefix = {v:f"{k}:" if k else k for k, v in namespaces.items()}

        def _has_uri(name):
            return name.startswith("{")

        def _prefix(name):
            uri, name = name[1:].rsplit("}", 1)
            return uri_prefix[uri] + name

        for el in tree.iter():
            if _has_uri(el.tag):
                el.tag = _prefix(el.tag)

            for key in el.keys():
                if _has_uri(key):
                    el.set(_prefix(key), el.attrib.pop(key))

    @staticmethod
    def _namespaces(path):
        import xml.etree.ElementTree as ET
        return dict(
            node for _event, node
            in ET.iterparse(path, events=['start-ns'])
        )

    @classmethod
    def parse_content(cls, el, text, base, **kwargs):
        """text argument is unused"""
        path = base / el.attrib.pop("src")

        try:
            if path.suffix == ".svg":
                from xml.etree.ElementTree import parse
                el.tag = "svg"
                svg = parse(path).getroot()
                el.attrib.update(svg.attrib)
                # el.attrib["height"] = "100%"
                # el.attrib["width"]  = "100%"

                # convert from {uri}tag to prefix:tag
                # this is a *bad* solution,
                # but etree interface is limited
                cls._prefix(svg, cls._namespaces(path))

                # proceed as usual
                for c in svg:
                    el.append(c)

            else:
                el.tag = "img"
                with open(path, mode='rb') as f:
                    import base64
                    b64 = base64.b64encode(f.read()).decode("utf-8")
                    el.set("src", f"data:image/png;base64,{b64}")
        except ValueError:
            el.tag = "img"
            pass  # no '.' in path


class Add(Addup):
    # Alternatively this could be part of post-processing
    # NOTE: this is for attaching, not extending

    @classmethod
    def _parse(cls, parent, tag, text, **kwargs):
        element = cls.elements.get(tag, Addup)

        el = Element(tag=tag)
        text = element.parse_head(el, text)

        if src := el.get("src"):
            parent.extend(cls._build(src, **kwargs))
        else:
            # template entry
            parent.append(el)

        return text

    @staticmethod
    def parse_head(el, text):
        text = parse_classifiers(el, text)
        text = parse_attributes(el, text)
        return text

    @staticmethod
    def _build(src, base, **kwargs):
        root = Document()
        path = base / src

        with open(path, mode="r", encoding="utf-8") as f:
            text = f.read()

        # NOTE circular dependency
        from .core import _addup
        root = _addup(root, text, base=base, **kwargs)

        return root


Addup.register((Addup, Code, Math, InlineComment))
Addup.compile()
Addup.register_element((Timepoint, CSS, JS, Style, Script, Image, Add))
