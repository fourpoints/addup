from os import stat
from typing import Type
from .node import Document
from .builder import build


def shape(el, **kwargs):
    el = wrap(el, **kwargs)

    return el


def replace_element(e1, e2):
    e1.tag = e2.tag
    e1.clear()
    e1.extend(e2)


class Wrap:
    def __init__(self, *wrappers):
        self.wrappers = {w.__name__.lower(): w for w in wrappers}

    def __call__(self, el, **kwargs):
        if el.find("doctype"):
            return el

        # include "extend" for backwards compatibility
        if (wrapper := el.find("extends") or el.find("extend")) is not None:
            return self._extend(wrapper, el, **kwargs)

        return el

    def _extend(self, wrapper, el, **kwargs):
        el.remove(wrapper)

        # new style wrapper
        if len(wrapper):
            return Template(wrapper).shape(el, **kwargs)

        # this gets the "template" part of "+extends(template)"
        wrap = list(wrapper.attrib)[0]

        # old style wrapper with <head>
        return self.wrappers[wrap].shape(el, **kwargs)


class Template:
    def __init__(self, wrapper):
        self.name = list(wrapper.attrib)[0]
        self.wrapper = wrapper

    def _text(self, base):
        path = base / f"{self.name}.add"
        with open(path, mode="r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def _addup(text, **kwargs):
        root = Document()

        # NOTE circular dependency
        from .core import _addup
        return _addup(root, text, **kwargs)

    @staticmethod
    def _pop(el, match):
        pop = el.find(match)
        el.remove(pop)
        return pop

    @staticmethod
    def _extend(root, el):
        padd = root.find(".//add/..")
        add = padd.find("add")
        i = tuple(padd).index(add)
        padd.remove(add)

        for child in reversed(el):
            padd.insert(i, child)

    def _substitute(self, template):
        from .node import Text, Element

        for mapping in self.wrapper:
            pattern = "{{" + mapping.tag + "}}"
            sub = mapping[0].text

            for el in template.iter(Text):
                el.text = el.text.replace(pattern, sub)

            for el in template.iter():
                for key, value in el.items():
                    if value is not None:
                        el.set(key, value.replace(pattern, sub))

    def shape(self, el, **kwargs):
        text = self._text(**kwargs)
        root = self._addup(text, **kwargs)

        self._substitute(root)
        self._extend(root, el)

        return root


class OldTemplate:
    @classmethod
    def _text(cls, base):
        path = base / f"{cls.__name__.lower()}.add"
        with open(path, mode="r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def _addup(text, **kwargs):
        root = Document()

        # NOTE circular dependency
        from .core import _addup
        return _addup(root, text, **kwargs)

    @staticmethod
    def _pop(el, match):
        pop = el.find(match)
        el.remove(pop)
        return pop

    @staticmethod
    def _extend(root, el):
        padd = root.find(".//add/..")
        add = padd.find("add")
        i = tuple(padd).index(add)
        padd.remove(add)

        for child in reversed(el):
            padd.insert(i, child)


class Base(OldTemplate):
    @staticmethod
    def _substitute_head(h1, h2):
        tags = ("title",)
        for tag in tags:
            e1 = h1.find(tag)
            e2 = h2.find(tag)
            replace_element(e1, e2)
            h2.remove(e2)
        h1.extend(h2)

    @classmethod
    def shape(cls, el, **kwargs):
        text = cls._text(**kwargs)
        root = cls._addup(text, **kwargs)

        wraphead = root.find(".//head")
        elhead = cls._pop(el, "head")

        cls._substitute_head(wraphead, elhead)
        cls._extend(root, el)

        return root


class Article(OldTemplate):
    @classmethod
    def _substitute_head(cls, root, el):
        h = cls._pop(el, "head")

        label = h.find("label")
        title = h.find("title")
        author = h.find("author")
        date = h.find("publish-date")

        id_ = label[0].text

        a = root.find("article")
        a.set("id", id_)

        _title = a.find("h2")
        _date = a.find("time")
        _author = a.find("p")
        _anchor = _title.find("a")

        _anchor.set("href", "#"+id_)

        _title.extend(title)
        _date.extend(date)
        _author.extend(author)


    @classmethod
    def shape(cls, el, **kwargs):
        text = cls._text(**kwargs)
        root = cls._addup(text, **kwargs)

        cls._substitute_head(root, el)
        cls._extend(root, el)

        return root


wrap = Wrap(Base, Article)
