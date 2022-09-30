GROUPERS = {
    # GROUPERS
	r"\over" : ("mfrac", {}, "GROUPER", [-1, 1]),
	r"\bover" : ("mfrac", {"bevelled": "true"}, "GROUPER", [-1, 1]),
	r"\frac" : ("mfrac", {}, "GROUPER", [1, 2]),
	r"\sub" : ("msub", {}, "GROUPER", [1, 2]),
	r"\sup" : ("msup", {}, "GROUPER", [1, 2]),
	r"\subsup" : ("msubsup", {}, "GROUPER", [1, 2, 3]),
	r"\underset" : ("munder", {}, "GROUPER", [2, 1]),
	r"\overset" : ("mover", {}, "GROUPER", [2, 1]),
	r"\underover" : ("munderover", {}, "GROUPER", [1, 2, 3]),
	r"\root" : ("mroot", {}, "GROUPER", [2, 1]),
	r"\sqrt" : ("msqrt", {}, "GROUPER", [1]),
	r"\binom" : ("mfrac", {"linethickness": "0"}, "GROUPER", [1, 2]),
	r"\choose" : ("mfrac", {"linethickness": "0"}, "GROUPER", [-1, 1]),
	r"\enclose" : ("menclose", {}, "GROUPER", [1]),
	r"\cancel" : ("menclose", {"notation": "updiagonalstrike"}, "GROUPER", [1]),
	r"\pad" : ("mpadded", {"lspace": "0.5em", "rspace": "0.5em"}, "GROUPER", [1]),
	r"\prescript" : ("mmultiscripts", {}, "PRE", []),
		r"\pre" : ("mmultiscripts", {}, "PRE", []),
}

ACCENTS = {
	r"\hat": ("mover", {"accent": "true"}, "ACCENT", "&Hat;"),
	r"\check": ("mover", {"accent": "true"}, "ACCENT", "&check;"),
	r"\acute": ("mover", {"accent": "true"}, "ACCENT", "&acute;"),
	r"\grave": ("mover", {"accent": "true"}, "ACCENT", "&grave;"),
	r"\bar": ("mover", {"accent": "true"}, "ACCENT", "&macr;"),
	r"\vec": ("mover", {"accent": "true"}, "ACCENT", "&rarr;"), # "&#8407;"),
	r"\dot": ("mover", {"accent": "true"}, "ACCENT", "&dot;"),
	#"\ddot": "&ddot;",
	r"\breve": ("mover", {"accent": "true"}, "ACCENT", "&breve;"),
	r"\tilde": ("mover", {"accent": "true"}, "ACCENT", "&tilde;"),
	r"\overline": ("mover", {}, "ACCENT", "&oline;"),
		r"\ov": ("mover", {}, "ACCENT", "&OverBar;"), #???
		r"\inverse": ("mover", {"accent": "false"}, "ACCENT", "&macr;"), #???
	#"\underline": "&uline;",
	r"\underbrace": ("munder", {"movablelimits": "false"}, "ACCENT", "&UnderBrace;"), #???
	r"\overbrace": ("mover", {"movablelimits": "false"}, "ACCENT", "&OverBrace;"), #???
}

SEPARATORS = {
    r"\left"   : ("NONE", {}, "LEFT", None),
    r"\l"      : ("NONE", {}, "LEFT", None),
    r"\middle" : ("NONE", {}, "MIDDLE", None),
    r"\m"      : ("NONE", {}, "MIDDLE", None),
    r"\right"  : ("NONE", {}, "RIGHT", None),
    r"\r"      : ("NONE", {}, "RIGHT", None),
}

BRACKETS = {
	r"\lfloor"   : ("mo", {"fence": "true"}, "OPEN", "&lfloor;"),
	r"\lceil"    : ("mo", {"fence": "true"}, "OPEN", "&lceil;"),
	r"\langle"   : ("mo", {"fence": "true"}, "OPEN", "&langle;"),
	r"\lvert"    : ("mo", {"fence": "true"}, "OPEN", "&vert;"),
	r"\lVert"    : ("mo", {"fence": "true"}, "OPEN", "&Vert;"),
	r"\lucorner" : ("mo", {"fence": "true"}, "OPEN", "&#11810;"),
	r"\lbcorner" : ("mo", {"fence": "true"}, "OPEN", "&#11812;"),

	r"\rfloor"   : ("mo", {"fence": "true"}, "CLOSE", "&rfloor;"),
	r"\rceil"    : ("mo", {"fence": "true"}, "CLOSE", "&rceil;"),
	r"\rangle"   : ("mo", {"fence": "true"}, "CLOSE", "&rangle;"),
	r"\rvert"    : ("mo", {"fence": "true"}, "CLOSE", "&vert;"),
	r"\rVert"    : ("mo", {"fence": "true"}, "CLOSE", "&Vert;"),
	r"\rucorner" : ("mo", {"fence": "true"}, "CLOSE", "&#11811;"),
	r"\rbcorner" : ("mo", {"fence": "true"}, "CLOSE", "&#11813;"),
}

ATTRIBUTES = {
    r"\mathbb" : ("NONE", {"mathvariant": "double-struck"}, "ATTRIBUTE", [1]),
    r"\bb"     : ("NONE", {"mathvariant": "double-struck"}, "ATTRIBUTE", [1]),
    r"\mathfrak":("NONE", {"mathvariant": "fraktur"}, "ATTRIBUTE", [1]),
    r"\frak"   : ("NONE", {"mathvariant": "fraktur"}, "ATTRIBUTE", [1]),
    r"\mathscr": ("NONE", {"mathvariant": "script"}, "ATTRIBUTE", [1]),
    r"\scr"    : ("NONE", {"mathvariant": "script"}, "ATTRIBUTE", [1]),
    r"\mathcal": ("NONE", {"mathvariant": "script", "class": "calligraphic"}, "ATTRIBUTE", [1]),
    r"\cal"    : ("NONE", {"mathvariant": "script", "class": "calligraphic"}, "ATTRIBUTE", [1]),

    r"\mathrm" : ("NONE", {"mathvariant": "normal"}, "ATTRIBUTE", [1]),
    r"\rm"     : ("NONE", {"mathvariant": "normal"}, "ATTRIBUTE", [1]),
    r"\mathit" : ("NONE", {"mathvariant": "italic"}, "ATTRIBUTE", [1]),
    r"\it"     : ("NONE", {"mathvariant": "italic"}, "ATTRIBUTE", [1]),
    r"\mathbf" : ("NONE", {"mathvariant": "bold"}, "ATTRIBUTE", [1]),
    r"\bf"     : ("NONE", {"mathvariant": "bold"}, "ATTRIBUTE", [1]),
    r"\mathsf" : ("NONE", {"mathvariant": "normal"}, "ATTRIBUTE", [1]),
    r"\sf"     : ("NONE", {"mathvariant": "normal"}, "ATTRIBUTE", [1]),
    r"\mathtt" : ("NONE", {"mathvariant": "monospace"}, "ATTRIBUTE", [1]),
    r"\tt"     : ("NONE", {"mathvariant": "monospace"}, "ATTRIBUTE", [1]),

    r"\bit"     : ("NONE", {"mathvariant": "bold-italic"}, "ATTRIBUTE", [1]),
    r"\bscr"     : ("NONE", {"mathvariant": "bold-script"}, "ATTRIBUTE", [1]),
    r"\bcal"     : ("NONE", {"mathvariant": "bold-script", "class": "calligraphic"}, "ATTRIBUTE", [1]),
	r"\bfrak"     : ("NONE", {"mathvariant": "bold-fraktur"}, "ATTRIBUTE", [1]),
	r"\bsf"     : ("NONE", {"mathvariant": "bold-sans-serif"}, "ATTRIBUTE", [1]),
	r"\bsfit"     : ("NONE", {"mathvariant": "sans-serif-bold-italic"}, "ATTRIBUTE", [1]),

    r"\displaystyle"     : ("NONE", {"displaystyle": "true"}, "ATTRIBUTE", [1]),
}
