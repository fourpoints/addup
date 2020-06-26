from functools import partial
import xml.etree.ElementTree as ET
# from copy import deepcopy

# BUG: Nested <anchor> tags are disallowed, which can break headings
# e.g. footnotes in heading.
# Possible fix: wrap anchor heading in §-span element instead of heading.

def _class_iter(it, class_):
    for child in filter(lambda el: class_ in el.get("class", []), it):
        yield child


def _prepend(el, child):
    child.tail = el.text
    el.text = None
    el.insert(0, child)


def _branch(el, branch):
    branch.text = el.text
    branch.extend(list(el))
    #branch.tail = el.tail

    #el.text = el.tail = None
    el.text = None
    for child in list(el): el.remove(child)

    el.append(branch)

def _next(it):
    return next(it, None)

def table_of_contents(tree):
    # BUG bool(Element) == len(Element)
    if (toc := _next(tree.iter(f"toc"))) is None:
        return tree

    if (content := _next(_class_iter(tree.iter("section"), "content"))) is None:
        return tree



    HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
    # import re
    # is_heading = re.compile("^h[1-6]$").match

    toc_tree = {}
    path = []

    # iter does dfs (depth-first search)
    for h in filter(lambda e: e.tag in HEADINGS, content.iter()):
        # note that level > h.tag if <h#> < <h#>
        # expects tags to be lowercased (who uses uppercased tags??)

        # ignore headers marked with no-toc
        if "no-toc" in h.get("class", []): continue

        while path and h.tag <= path[-1].tag:
            path.pop()

        current = toc_tree
        for key in path:
            current = current[key]
        current[h] = {}

        path.append(h)



    def listify(d, level):
        ol = ET.Element("ol")
        for i, (el, children) in enumerate(d.items(), 1):
            current_level = f"{level}.{i}" if level else str(i)

            # Make <list><a>
            li = ET.SubElement(ol, "li")
            anchor = ET.SubElement(li, "a")

            # Add level to id and hyperlink reference to toc
            el.attrib.setdefault("id", []).append(f"toc-{current_level}")
            anchor.set("href", f"#toc-{current_level}")

            # Copy header text to anchor
            # deepcopy?
            anchor.text = el.text
            if len(el): anchor.extend(list(el)) # add children if any


            # Add link to self (wrap in <a>)
            if "no-ref" not in h.get("class", []):
                ref = ET.Element("a")
                ref.set("href", f"#toc-{current_level}")

                _branch(el, ref)


            # Add numbering to heading
            if "no-num" not in h.get("class", []):
                num = ET.Element("span", attrib={"class": "section-num"})
                num.text = current_level+" "

                _prepend(el, num)


            # Recurse on children
            if children: li.append(listify(children, current_level))

        return ol

    toc.tag = "details"
    summary = ET.SubElement(toc, "summary")
    summary.text = "Table of contents"

    toc_nav = ET.Element("nav")
    toc_nav.append(listify(toc_tree, ""))
    toc.append(toc_nav)

    return tree



def order_headings(tree):
    # Ensures headers after <h1> are <h2> and so on
    NotImplemented



def BEM_classing(tree):
    # .block__element--modifier1--modifier2 ->
    # .block__element.block__element--modifier1.block__element--modifier2
    NotImplemented



def treenumerate(tree, figure_tag):
    # BUG bool(Element) == len(Element)
    if (toc := _next(tree.iter(f"toc-{figure_tag}"))) is None:
        return tree

    if (content := _next(_class_iter(tree.iter("section"), "content"))) is None:
        return tree


    figures = {}
    toc_nav = ET.Element("nav")
    toc_list = ET.SubElement(toc_nav, "ol")

    figure_class = f"a-{figure_tag}"
    for i, fig in enumerate(_class_iter(content.iter("figure"), figure_class), 1):
        label = fig.get("id")[0]
        heading = fig[0]

        figures[label] = i

        # Make <list><a>
        li = ET.SubElement(toc_list, "li")
        anchor = ET.SubElement(li, "a")

        # Add level to id and hyperlink reference to toc
        heading.attrib.setdefault("id", []).append(f"toc-{figure_tag}-{i}")
        anchor.set("href", f"#toc-{figure_tag}-{i}")

        # Copy header text to anchor
        # deepcopy?
        anchor.text = heading.text
        if len(heading): anchor.extend(list(heading)) # add children if any


        # Add link to self (wrap in <a>)
        if "no-ref" not in heading.get("class", []):
            ref = ET.Element("a")
            ref.set("href", f"#toc-{figure_tag}-{i}")

            _branch(heading, ref)

        # Add numbering to heading
        if "no-num" not in heading.get("class", []):
            num = ET.Element("span", attrib={"class": "figure-num"})
            num.text = f"{figure_tag} {i}: "

            _prepend(heading, num)


    toc.tag = "details"
    summary = ET.SubElement(toc, "summary")
    summary.text = f"Table of {figure_tag}s"
    toc.append(toc_nav)


    # References
    for ref in content.iter("ref"):
        figtype, label = next(iter(ref.items()))
        if figtype.lower() == figure_tag and label in figures:
            ref.attrib.pop(figtype)

            ref.tag = "a"
            ref.set("href", f"#toc-{figure_tag}-{i}")
            ref.text = f"{figtype}&nbsp;{i}"

    return tree



def eqnumerate(tree):
    if (content := _next(_class_iter(tree.iter("section"), "content"))) is None:
        return tree


    equations = {}

    for equation in _class_iter(tree.iter("figure"), "a-equation"):
        label = equation.get("id")[0]

        first = equation[0][0][0][0][0][0].text
        last = equation[0][0][-1][0][0][0].text

        if first == last: equations[label] = first
        else: equations[label] = f"{first[:-1]}-{last[1:]}"

    # References
    for ref in content.iter("ref"):
        figtype, label = next(iter(ref.items()))
        if figtype.lower() == "equation" and label in equations:
            ref.attrib.pop(figtype)

            ref.tag = "a"
            ref.set("href", f"#{label}")
            ref.text = f"{figtype}&nbsp;{equations[label]}"

    return tree



def _citation(entry):
    span = ET.Element("span")

    entrytype = entry["type"]
    entrydata = entry["data"]

    entryfields = {
        "article" : ["author", "title", "journal", "year"],
        "book"    : ["author", "title", "journal", "year"],
        "misc"    : ["author", "title", "journal", "year", "url", "note"],
    }[entrytype]

    element = {
        "author"    : "span",
        "title"     : "cite",
        "journal"   : "span",
        "year"      : "time",
        "url"       : "a",
        "note"      : "span",
    }

    for key in entryfields:
        tag = element[key]
        el = ET.SubElement(span, tag)
        el.text = str(entrydata[key])
        el.tail = ", "

        if tag == "time": el.set("datetime", el.text); el.text = f"({el.text})"
        if tag == "a":
            el.set("href", el.text)
            el.set("class",
                ["link", "link__text", "link__action", "link__action--external"]
            )

    el.tail = ""

    #text = ", ".join(map(str, entry.values()))

    return span


def references(tree):
    from ast import literal_eval

    # BUG bool(Element) == len(Element)
    if (refblock := _next(tree.iter("references"))) is None:
        return tree

    if (content := _next(_class_iter(tree.iter("section"), "content"))) is None:
        return tree


    refblock.tag = "nav"


    ref_file = refblock.attrib.pop("src")
    with open(ref_file, mode="r", encoding="utf-8") as f:
        refs = literal_eval(f.read())


    reflist = ET.SubElement(refblock, "ul", attrib={"class" : "reference-list"})

    citations = {}

    for i, citation in enumerate(content.iter("ref"), 1):
        figtype, label = next(iter(citation.items()))
        if figtype.lower() != "citation": continue

        citation.attrib.pop(figtype)

        post = ", ".join(map(" ".join, citation.items()))

        citation.tag = "cite"
        citation.attrib.setdefault("class", []).append("citation")
        citation.set("id", f"reference-{i}")
        citation.text = f"{i}" if not post else f"{i}, {post}"

        ref = ET.Element("a")
        ref.set("href", f"#reference-pointer-{i}")

        _branch(citation, ref)


        if label not in citations:
            li = ET.SubElement(reflist, "li", attrib={"class" : "reference"})
            alist = ET.SubElement(li, "ul", attrib={"class" : "ref-pointers"})
            citations[label] = alist

            citing = ET.SubElement(li, "span")
            citing.append(_citation(refs[label]))


        alist = citations[label]
        li = ET.SubElement(alist, "li", attrib={"class" : "ref-pointer"})
        li.set("id", f"reference-pointer-{i}")
        pointer = ET.SubElement(li, "a")
        pointer.set("href", f"#reference-{i}")
        pointer.text = f"{i}^"


    return tree



def footnotes(tree):
    # BUG bool(Element) == len(Element)
    if (fnblock := _next(tree.iter("footnotes"))) is None:
        return tree

    if (content := _next(_class_iter(tree.iter("section"), "content"))) is None:
        return tree


    fnblock.tag = "nav"


    fnlist = ET.SubElement(fnblock, "ul", attrib={"class" : "footnote-list"})


    for i, footnote in enumerate(content.iter("footnote"), 1):
        footnote.set("title", "".join(footnote.itertext()))

        # move content
        li = ET.SubElement(fnlist, "li")

        pointer = ET.SubElement(li, "a")
        pointer.set("id", f"footnote-pointer-{i}")
        pointer.set("href", f"#footnote-{i}")
        pointer.text = f"{i}^ "

        note = ET.SubElement(li, "span")
        note.text = footnote.text
        note.extend(list(footnote))

        # clear footnote after moving content
        for child in footnote: footnote.remove(child)

        footnote.tag = "sup"
        footnote.attrib.setdefault("class", []).append("footnote")
        footnote.set("id", f"footnote-{i}")
        footnote.text = f"{i}"


        # make pointer
        ref = ET.Element("a")
        ref.set("href", f"#footnote-pointer-{i}")

        _branch(footnote, ref)

    return tree



def unused_elements(tree, tags):
    # It would be better to iterate over all elements
    # and check if they are valid html tags
    for tag in tags:
        for el in tree.iter(tag):
            print(f"Unused element {el.tag} with attrib {el.attrib}")

    return tree



modifiers = [
    table_of_contents,
    partial(treenumerate, figure_tag="table"),
    partial(treenumerate, figure_tag="figure"),
    partial(treenumerate, figure_tag="listing"),
    eqnumerate,
    references,
    footnotes,
    partial(unused_elements, tags=["ref"])
]

def treemodifier(tree):
    for modifier in modifiers:
        tree = modifier(tree)

    return tree
