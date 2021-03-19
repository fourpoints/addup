COMMON = {
#    "a" : ("mi", {}, "var", "a"),
#    "d" : ("mo", {"form": "prefix", "rspace": "0"}, "operator", "d"),
#    "df" : ("mi", {"mathvariant": "italic"}, "var", "df"),
    "e" : ("mi", {}, "constant", "e"),
    #"E" : ("mo", {"rspace": "0"}, "operator", "E"),
#    "f" : ("mo", {"mathvariant": "italic", "lspace": "0", "rspace": "0"}, "operator", "f"),
    "i" : ("mi", {"mathvariant": "italic"}, "constant", "i"),
    "j" : ("mi", {"mathvariant": "italic"}, "constant", "j"),
    "k" : ("mi", {"mathvariant": "italic"}, "constant", "k"),
}

STATISTICS = {
	r"\done"   : ("mi", {}, "constant", "⚀"),
	r"\dtwo"   : ("mi", {}, "constant", "⚁"),
	r"\dthree" : ("mi", {}, "constant", "⚂"),
	r"\dfour"  : ("mi", {}, "constant", "⚃"),
	r"\dfive"  : ("mi", {}, "constant", "⚄"),
	r"\dsix"   : ("mi", {}, "constant", "⚅"),
}

CHEMISTRY = {
	r"H"  : ("mi", {"mathvariant": "normal"}, "chem-symbol", "H"), #Hydrogen
	r"D"  : ("mi", {"mathvariant": "normal"}, "chem-symbol", "D"), #Deuterium
	r"T"  : ("mi", {"mathvariant": "normal"}, "chem-symbol", "T"), #Tritium
	r"H"  : ("mi", {"mathvariant": "normal"}, "chem-symbol", "H"),
	r"He" : ("mi", {"mathvariant": "normal"}, "chem-symbol", "He"),
	r"Li" : ("mi", {"mathvariant": "normal"}, "chem-symbol", "Li"),
	r"Be" : ("mi", {"mathvariant": "normal"}, "chem-symbol", "Be"),
	r"C"  : ("mi", {"mathvariant": "normal"}, "chem-symbol", "C"),
	r"N"  : ("mi", {"mathvariant": "normal"}, "chem-symbol", "N"),
	r"O"  : ("mi", {"mathvariant": "normal"}, "chem-symbol", "O"),
	r"F"  : ("mi", {"mathvariant": "normal"}, "chem-symbol", "F"),
	r"Ne" : ("mi", {"mathvariant": "normal"}, "chem-symbol", "Ne"),
}
