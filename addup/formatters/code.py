from pygments.formatter import Formatter
from pygments.formatters.html import webify, _get_ttype_class, STANDARD_TYPES
from pygments.util import get_int_opt, get_list_opt, get_bool_opt
import pygments.token as token
from html import escape
from ..node import Element, Text
from itertools import groupby

try:
    import ctags
    import os  # os is only used with ctags
except ImportError:
    ctags = None


class ElementFormatter(Formatter):
    def __init__(self, **options):
        Formatter.__init__(self, **options)

        # derived from HtmlFormatter
        self.noclasses = get_bool_opt(options, 'noclasses', False)
        self.classprefix = options.get('classprefix', '')
        self.tagsfile = self._decodeifneeded(options.get('tagsfile', ''))
        self.tagurlformat = self._decodeifneeded(options.get('tagurlformat',''))

        if self.tagsfile:
            if not ctags:
                raise RuntimeError('The "ctags" package must to be installed '
                                   'to be able to use the "tagsfile" feature.')
            self._ctags = ctags.CTags(self.tagsfile)


        linenos = options.get("linenos", False)

        self.lang = options.get("lang", "")  # language
        self.wrap = options.get("wrap", "block")  # inline | block | table

        self.linenos = bool(linenos)
        self.linenostart = abs(get_int_opt(options, 'linenostart', 1))
        self.lineseparator = options.get('lineseparator', Element("br"))
        self.lineanchors = options.get('lineanchors', '')
        self.hl_lines = set()
        for lineno in get_list_opt(options, 'hl_lines', []):
            try:
                self.hl_lines.add(int(lineno))
            except ValueError:
                pass

        self._create_stylesheet()

    def _create_stylesheet(self):
        ttc = self.ttype_to_class = {token.Token: ''}
        cts = self.class_to_style = {}

        for ttype, ndef in self.style:
            name = self._get_css_class(ttype)

            s = []
            if ndef['color']:
                s.append('color: {}'.format(webify(ndef['color'])))
            if ndef['bold']:
                s.append('font-weight: bold')
            if ndef['italic']:
                s.append('font-style: italic')
            if ndef['underline']:
                s.append('text-decoration: underline')
            if ndef['bgcolor']:
                s.append('background-color: {}'.format(webify(ndef['bgcolor'])))
            if ndef['border']:
                s.append('border: 1px solid {}'.format(webify(ndef['border'])))
            style = "; ".join(s)

            if style:
                ttc[ttype] = name
                # save len(ttype) to enable ordering the styles by
                # hierarchy (necessary for CSS cascading rules!)
                cts[name] = (style, ttype, len(ttype))

    def _get_css_class(self, ttype):
        """Return the css class of this token type prefixed with
        the classprefix option."""
        ttypeclass = _get_ttype_class(ttype)
        if ttypeclass:
            return self.classprefix + ttypeclass
        return ''

    def _get_css_classes(self, ttype):
        """Return the css classes of this token type prefixed with
        the classprefix option."""
        class_ = self._get_css_class(ttype)
        while ttype not in STANDARD_TYPES:
            ttype = ttype.parent
            class_ = self._get_css_class(ttype) + ' ' + class_
        return class_

    def _decodeifneeded(self, value):
        if isinstance(value, bytes):
            if self.encoding:
                return value.decode(self.encoding)
            return value.decode()
        return value

    def treeformat(self, tokensource, root):
        # TODO highlighting and numbering
        source = self._format_lines(tokensource)
        if self.wrap == "inline":
            source = self._join_lines(source)
            el = self._wrap_code(source)
            self._class(el, "code code--inline")

        elif self.wrap == "block":
            if self.linenos:
                source = self._number_lines(source, "span")
            if self.hl_lines:
                source = self._wrap_spans(source)
                source = self._highlight_lines(source)
            source = self._join_lines(source)
            el = self._wrap_precode(source)
            self._class(el, "code code--block")

        elif self.wrap == "table":
            source = self._wrap_codes(source)
            source = self._wrap_pres(source)
            source = self._wrap_cells(source)
            if self.linenos:
                source = self._number_lines(source, "td")
            source = self._wrap_rows(source)
            if self.hl_lines:
                source = self._highlight_lines(source)
            el = self._wrap_table(source)
            self._class(el, "code code--table")

        else:
            raise ValueError(f"Unknown wrap type {self.wrap}")

        root.append(el)

    def _ttype_class(self, ttype):
        nocls = self.noclasses
        # rename, remove 2's
        getcls = self.ttype_to_class.get
        cts = self.class_to_style

        if nocls:
            cclass = getcls(ttype)
            while cclass is None:
                ttype = ttype.parent
                cclass = getcls(ttype)
            return "style", cclass and cts[cclass][0] or None
        else:
            return "class", self._get_css_classes(ttype) or None

    def _lookup_ctag(self, token):
        entry = ctags.TagEntry()
        if self._ctags.find(entry, token, 0):
            return entry['file'], entry['lineNumber']
        else:
            return None, None

    def _value_tag(self, ttype, value):
        # for <span style=""> lookup only
        tagsfile = self.tagsfile

        if tagsfile and ttype in token.Token.Name:
            filename, linenumber = self._lookup_ctag(value)
            if linenumber:
                base, filename = os.path.split(filename)
                if base:
                    base += '/'
                filename, extension = os.path.splitext(filename)
                url = self.tagurlformat % {'path': base, 'fname': filename,
                                            'fext': extension}
                return "href", f'{url}#{self.lineanchors}-{linenumber}'
        return "href", None

    def _groupby_type(self, tokensource):
        for ttype, group in groupby(tokensource, key=lambda x:x[0]):
            yield ttype, "".join(value for _ttype, value in group)


    def _format_lines(self, tokensource):
        # https://pygments.org/docs/formatters/#HtmlFormatter
        """
        Just format the tokens, without any wrapping tags.
        Yield individual lines.

        goes a little different depending on
        * if token value is multiple lines
        * if token type is same as previous

        split up in two functions, one that groups values by cclass,
        another that groups elements on a line together

        it tries to build a line until a newline is found, then
        it yields the line
        """

        def _wrap(el, tag, attribute, value):
            if value is not None:
                _el = Element(tag)
                _el.append(el)
                _el.set(attribute, value)
                return _el
            else:
                return el

        line = []
        for ttype, value in self._groupby_type(tokensource):
            attrib, val = self._ttype_class(ttype)
            href, src = self._value_tag(ttype, value)


            parts = escape(value).split('\n')

            # encapsulate value in <span> and <a>
            # if value and src are set (respectively)
            parts_ = []
            for part in parts:
                el = Text(part)
                el = _wrap(el, "span", attrib, val)
                el = _wrap(el, "a", href, src)
                parts_.append(el)

            *parts, lastpart = parts_

            # for all but the last line
            # valid if `value` is multi-lined, e.g. a newline is found
            for part in parts:
                if line:
                    line.append(part)
                    yield line
                    line = []
                elif isinstance(part, Element):
                    # if line is one (part of) value
                    yield [part]
                elif part.tag is Text and part.text:
                    yield [part]
                else:
                    # if line is blank
                    yield []

            # a part will always be either Element or Text, so this is redundant
            if isinstance(lastpart, Element):
                line.append(lastpart)
            elif lastpart.tag is Text and lastpart.text:
                line.append(lastpart)

        if line:
            yield 1, line

    def _join_lines(self, inner):
        yield next(inner)
        for line in inner:
            yield self.lineseparator,
            yield line

    def _wrap_spans(self, inner):
        for line in inner:
            el = Element("span")
            el.extend(line)
            yield el,

    def _wrap_codes(self, inner):
        for line in inner:
            el = Element("code")
            el.extend(line)
            yield el,

    def _wrap_pres(self, inner):
        for line in inner:
            el = Element("pre")
            el.extend(line)
            yield el,

    def _wrap_cells(self, inner):
        for line in inner:
            el = Element("td")
            el.extend(line)
            yield el,

    def _wrap_rows(self, inner):
        for line in inner:
            el = Element("tr")
            el.extend(line)
            yield el,

    def _number_lines(self, inner, tag):
        la = self.lineanchors

        for i, el in enumerate(inner, start=self.linenostart):
            lineno = Element(tag, {"class": "lineno", "data-lineno": str(i)})
            if la: lineno.set("id", f"#{la}-{i}")
            # lineno.append(Text(str(i)))

            yield (lineno, *el)

    def _highlight_lines(self, inner):
        hls = self.hl_lines

        for i, (el,) in enumerate(inner, start=1):
            if i in hls:
                el.set("class", " ".join((el.get("class", default=""), "hll")))
            yield el,

    def _wrap_precode(self, inner):
        el = Element("code")
        for line in inner:
            el.extend(line)
        ell = Element("pre")
        ell.append(el)
        return ell

    def _wrap_code(self, inner):
        el = Element("code")
        for line in inner:
            el.extend(line)
        return el

    def _wrap_table(self, inner):
        el = Element("table")
        for line in inner:
            el.extend(line)
        return el

    def _class(self, el, class_):
        if self.lang:
            class_ += f" lang-{self.lang}"
        el.set("class", class_)



def treehighlight(code, lexer, formatter, root=None):
    if root is None:
        root = Element(tag="root")

    tokens = lexer.get_tokens(code)
    return formatter.treeformat(tokens, root)



if __name__ == "__main__":
    from io import StringIO
    from pygments.lexers import get_lexer_by_name
    from pygments import highlight
    from treeprinter import TreePrinter


    # make line numbers a <td> of the same row, like in gh
    # C:\Users\alpakka\AppData\Roaming\Python\Python38\site-packages\Pygments-2.5.2-py3.8.egg\pygments\formatters

    text = """def Python(*args, **kwargs):
    try:
        f = lambda: 1/0
        f()
    except ZeroDivisionError:
        pass
"""

    formatter = ElementFormatter(wrap="block", linenos=True)
    lexer = get_lexer_by_name("python3")
    string = StringIO()
    root = Element(tag="body")

    # highlight(
    #     code=text,
    #     lexer=lexer,
    #     formatter=formatter,
    #     outfile=string,
    # )

    # print(string.getvalue())

    treehighlight(
        code=text,
        lexer=lexer,
        formatter=formatter,
        root=root,
    )

    print(TreePrinter.tostring(root))

    with open("test.html", mode="w", encoding="utf-8") as f:
        print('<!DOCTYPE html><meta charset="utf-8">', file=f)
        print("""<style>
    /*code { white-space: pre; }*/
    pre { margin: 0; }
    [data-lineno]::before { content: attr(data-lineno); }
    .hll { background-color: yellow; }
</style>""", file=f)
        print(TreePrinter.tostring(root), file=f)
