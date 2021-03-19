from ..token import MObject, MGroup, MAction


def replicate(tree, p, separator, ellipsis):
    if tree.children[p+1].type == "SUB":
        lower = tree.children[p+2]

        if tree.children[p+3].type == "SUP":
            upper = tree.children[p+4]
            template = tree.children[p+5]
            del tree.children[p:p+5+1]
        else:
            upper = None
            template = tree.children[p+3]

            del tree.children[p:p+3+1]
    else:
        lower = upper = None

        del tree.children[p:p+0+1]

    def grouper(children):
        """Groups elements between separators"""
        groups = []
        group = MGroup("mrow", {}, "TREE", [])

        gget = lambda g: g.children[0] if len(g.children) == 1 else g
        for child in children:
            if child.type == "sep":
                groups.append(gget(group))
                group = MGroup("mrow", {}, "TREE", [])
            else:
                group.children.append(child)
        groups.append(gget(group))

        return groups


    def search(node, sub, key):
        if isinstance(node, MGroup):
            for i in range(len(node.children)):
                child = node.children[i]
                if isinstance(child, MObject) and child.text == var.text:
                    node.children[i] = sub
                elif isinstance(child, MGroup):
                    node.children[i] = search(child, sub, key)
        elif isinstance(node, MObject) and node.text == var.text:
            node = sub

        return node



    substitutes = []
    from copy import deepcopy
    if lower is not None:
        var = lower.children[0]

        for sub in grouper(lower.children[2:]):
            t = deepcopy(template)

            substitutes.append(search(t, sub, var))
            substitutes.append(separator)

        if upper is not None:
            substitutes.append(ellipsis)

            for sub in grouper(upper.children):
                t = deepcopy(template)

                substitutes.append(separator)
                substitutes.append(search(t, sub, var))
        else:
            substitutes.pop() #pop last PLUS
    else:
        substitutes.append(tree.children[p])

    return substitutes

def series(tree, p):
    # shared attrib-dict
    PLUS     = MObject("mo", {"form": "infix"}, "operator", "+")
    ELLIPSIS = MObject("mo", {}, "ellipsis", "&ctdot;")

    # we insert a list of mml-nodes
    tree.children[p:p] = replicate(tree, p, PLUS, ELLIPSIS)

    return p # doesn't group its elements, so we continue from where we left off

def seq(tree, p):
    # shared attrib-dict
    COMMA = MObject("mo", {"fence": "true"}, "sep", ",")
    ELLIPSIS = MObject("mo", {}, "ellipsis", "&hellip;")

    sequence = replicate(tree, p, COMMA, ELLIPSIS)
    lfence = MObject("mo", {"fence": "true"}, "bracket", '(')
    rfence = MObject("mo", {"fence": "true"}, "bracket", ')')

    # we insert a mml-node
    tree.children.insert(p, MGroup("mrow", {}, "TREE", [lfence, *sequence, rfence]))

    return p


def wrap(tree, p, lwrap, rwrap = None):
    if rwrap is None: rwrap = lwrap #FIXME non-aware

    value = tree.children[p+1]

    if isinstance(value, MGroup) and value.tag == "mrow":
        GROUP = MGroup("mrow", value.attrib.copy(), "TREE", [lwrap, *value.children, rwrap])
    else:
        GROUP = MGroup("mrow", {}, "TREE", [lwrap, value, rwrap])

    tree.children[p+1] = GROUP
    del tree.children[p]


def abs(tree, p):
    BAR = MObject("mo", {"fence": "true"}, "bracket", '|')

    wrap(tree, p, BAR)

    return p # doesn't group its elements, so we continue from where we left off


def norm(tree, p):
    NORM = MObject("mo", {"fence": "true"}, "bracket", '&Vert;')

    wrap(tree, p, NORM)

    return p # doesn't group its elements, so we continue from where we left off


def inner(tree, p):
    lbrace = MObject("mo", {"fence": "true"}, "bracket", '&langle;')
    rbrace = MObject("mo", {"fence": "true"}, "bracket", '&rangle;')

    wrap(tree, p, lbrace, rbrace)

    return p # doesn't group its elements, so we continue from where we left off


CUSTOM_ACTIONS = {
    r"\series" : ("series", {}, "CUSTOM", series),
    r"\seq" : ("sequence", {}, "CUSTOM", seq),

    r"\abs" : ("absolute", {}, "CUSTOM", abs),
    r"\norm" : ("norm", {}, "CUSTOM", norm),
    r"\inner" : ("norm", {}, "CUSTOM", inner),
}


def custom(tree, p):
    return tree.children[p][3](tree, p) # fourth argument is func
