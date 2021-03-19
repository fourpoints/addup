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
    def __call__(self, el, **kwargs):
        if el.find("doctype"):
            return el

        if (wrapper := el.find("extend") or el.find("extends")) is not None:
            return self._extend(wrapper, el, **kwargs)

    def _extend(self, wrapper, el, **kwargs):
        el.remove(wrapper)
        root = Document()

        wrap = next(iter(wrapper.attrib))
        with open(f"{wrap}.add", mode="r", encoding="utf-8") as f:
            text = f.read()

        build(root, text, **kwargs)

        wraphead = root.find(".//head")
        elhead = el.find(".//head")
        el.remove(elhead)
        self._replace_head(wraphead, elhead)

        add = root.find(".//add")
        padd = root.find(".//add/..")
        padd.remove(add)
        padd.extend(el)

        return root

    @staticmethod
    def _replace_head(h1, h2):
        tags = ("title",)
        for tag in tags:
            e1 = h1.find(tag)
            e2 = h2.find(tag)
            replace_element(e1, e2)
            h2.remove(e2)
        h1.extend(h2)




wrap = Wrap()
