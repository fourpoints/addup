import re
import textwrap
from pathlib import Path
from html import escape as html_escape
from .node import Element, Text, Comment


"""
Elements are created in two stages
First the head is found, ```() or +tag() or $$()
depending on its attributes and config, then we process its content.
this unifies all +elements at the head stage, and adds flexibility
at the processing stage. This may also be useful code and math.

[x] todo separate content (blocked, inline, fenced) from parser
  - i.e. make it a 2-tuple like (div, block), (span, inline)
[x] 3-steps
    * read header, content
    * process header
    * process content
    either HEAD FENCE CONTENT or FENCE HEAD CONTENT

[x] todo printer

for v4 preprocess blocks to brackets? so we can parse until fence-end;
blocks complicate this a bit.
"""

r"""
[ ] Figure out how to register addup-types, i.e.
    [ ] normal (default, +div, +span, +h1)
    [ ] special i (+math, +code)
    [ ] special ii (+doctype, +current-time)
    [ ] special iii (templates, +main-heading)
    * templates may be implemented with special syntax, but most are simple
      and can more easily be implemented with builder functions. Few templates
      are needed, so implementing an interface seems unnecessary. This is
      backend anyway, and won't affect syntax.
      * point here is that templates should be independent of syntax and may
        only be used to enhance the creation of templates with objects instead
        of builder functions.
    * build templates from leaf up; only allow descendants to be modified.
    # (\+\w+) is faster than (\+[a|b|c]+)
[ ] Templates/Base/Extension
    Link to separate files or included within?
    * special iii are converted in POSTPROCESSING
    Keep it simple, don't end up like xslt
    * no loops.
    * defunctionalize; don't make it too complicated, stick to a few types
    [ ] alias (eg. fig-title -> h3.fig-title; makes post-processing simpler.)
    [ ] toc
    [ ] enumeration (tables, figures, listings, equations)
    [ ] references
    [ ] footnotes
    [ ] tags-list
    [ ] title
    [ ] figures (fig-title, fig-caption, fig-content?, fig-tag?)
[ ] Two layers: outer (open/close expr), inner (parser)
[ ] Arguments before block? Block before argument?
[ ] <meta> arguments? two-way templates?
[ ] Pipe dream: Variables? Global context?
[ ] printer matches tags; text | comment | text;
    * only special cases should be special

+head[[body]]tail-
whole vs fragments/particles
"""

# <https://en.wikipedia.org/wiki/Head%E2%80%93body_pattern>

r"""
mumath?
$$#triangle
a^2 + b^2 = c^2

// If last term is non-number, print dots, then non-number
\sum_{n=1}^{\infty}{a_i^n} = \expand\sum_{n=1}^{\infty}{a_i^n}
:= a_i^1 + a_i^2 + \cdots + a_i^\infty

// If no last number, print dots only
\sum_{n=1}{a_i^n} = \expand\sum_{n=1}{a_i^n}
:= a_i^1 + a_i^2 + \cdots

// If last term is number, print all
\{\expand\sum_{n=0}^{6}{x^n}\} = \{x_0 + x_1 + x_2 + x_3 + x_4 + x_5 + x_6\}

// \expand\sum vs \esum?
$$
"""


def build(el, text, **kwargs):
    Addup.parse_content(el, text, **kwargs)
    return el

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
                raise SyntaxError("Unmatched bracket for bracketed text")


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

    fatt, fval = next(attributes)

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

            if text: el.append(Text(html_escape(text)))

            name = match.lastgroup
            fence = match.group(name)
            ctx = cls.contexts[name]

            text = ctx.parse(el, fence, tail, **kwargs)

        if text: el.append(Text(html_escape(text)))


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
    suffixes: {str}  # TODO check that suffix(es) matches?

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
        return str(path)
        # with open(path, mode='r', encoding="utf-8") as file:
        #     return file.read()


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
        from .formatters.code import ElementFormatter, treehighlight

        keys = (
            "lang", "wrap", "linenos", "linenostart",
            "hl_lines", "lineanchor", "multiline",
        )

        attrib = el.attrib
        options = {key: attrib.pop(key) for key in keys if key in attrib}

        lexer = get_lexer_by_name(options.get("lang"))
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
    counter = 1

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

        if "multiline" in options:
            options["align"] = options.pop("multiline", False)

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
        comment, text = text.split("\n", maxsplit=1)

        parent.append(Comment(comment))

        return text


class Image(Addup):
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
                el.attrib["height"] = "100%"
                el.attrib["width"]  = "100%"

                # this is not a general solution
                ns = {
                    "": "http://www.w3.org/2000/svg",
                    "xlink": "http://www.w3.org/1999/xlink",
                }

                # remove ns["0"] from tags
                for c in svg.iter():
                    c.tag = c.tag.split('}', 1)[1]

                # remove ns["1"] from the href-attrib for use-tags
                for c in svg.iter("use"):
                    c.attrib['href'] = c.attrib.pop(f'{{{ns["xlink"]}}}href')

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
    def _build(src, **kwargs):
        el = Element(None)

        with open(src, mode="r", encoding="utf-8") as f:
            text = f.read()

        build(el, text, **kwargs)
        return el


Addup.register((Addup, Code, Math, InlineComment))
Addup.compile()
Addup.register_element((Timepoint, CSS, JS, Style, Script, Image, Add))

# [x] "style"  : Raw,
# [x] "script" : Raw,
# [-] "math"   : MathJax, # for mathjax, deprecated
# [-] "read"   : Read, # for content loading, for backwards-comp.
# [-] "content": Read, # for content loading, for backwards-comp.
# [ ] "add"    : Read, # +add? +block? fragment? particle?
#            - add(src="") for children, +add[empty] for extends
# [ ] "image"  : Image,
# [x] "css"    : CSS,
# [x] "js"     : JS,
# [x] "now"    : Date.parse_content,


def treebuilder(file_path: Path, **options) -> Element:
    """
    This function does things
    """

    file_path = Path(file_path)
    base = file_path.parent

    # use io.String or memoryview or mmap?
    with open(file_path, mode="r", encoding="utf-8") as file:
        text = file.read()

    root = Element(tag="DOCUMENT")
    Addup.parse_content(root, text, base=base)

    return root
