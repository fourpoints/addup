SPACES = {
	r"\quad" : ("mspace", {"width": "1em"}, "hardspace", ""),
	r"\thinspace" : ("mspace", {"width": "1pt"}, "hardspace", ""),
	r"\enspace" : ("mspace", {"width": "5pt"}, "hardspace", ""),
}

GREEK = {
	r"\alpha"       : ("mi", {}, "var", "&alpha;"),
	r"\beta"        : ("mi", {}, "var", "&beta;"),
	r"\gamma"       : ("mi", {}, "var", "&gamma;"),
	r"\digamma"     : ("mi", {}, "var", "&gammad;"),
	r"\delta"       : ("mi", {}, "var", "&delta;"),
	r"\epsilon"     : ("mi", {}, "var", "&#x3f5;"),
	r"\varepsilon"  : ("mi", {}, "var", "&epsilon;"),
	r"\zeta"        : ("mi", {}, "var", "&zeta;"),
	r"\eta"         : ("mi", {}, "var", "&eta;"),
	r"\theta"       : ("mi", {}, "var", "&theta;"),
	r"\vartheta"    : ("mi", {}, "var", "&#x3D1;"),
	r"\kappa"       : ("mi", {}, "var", "&kappa;"),
	r"\lambda"      : ("mi", {}, "var", "&lambda;"),
	r"\mu"          : ("mi", {}, "var", "&mu;"),
	r"\nu"          : ("mi", {}, "var", "&nu;"),
	r"\xi"          : ("mi", {}, "var", "&xi;"),
	r"\omicron"     : ("mi", {}, "var", "&omicron;"),
	r"\pi"          : ("mi", {}, "var", "&pi;"),
	r"\varpi"       : ("mi", {}, "var", "&#982;"),
	r"\rho"         : ("mi", {}, "var", "&rho;"),
	r"\varrho"      : ("mi", {}, "var", "&#x3F1;"),
	r"\sigma"       : ("mi", {}, "var", "&sigma;"),
	r"\varsigma"    : ("mi", {}, "var", "&#x3C2;"),
	r"\tau"         : ("mi", {}, "var", "&tau;"),
	r"\upsilon"     : ("mi", {}, "var", "&upsilon;"),
	r"\phi"         : ("mi", {}, "var", "&straightphi;"),
	r"\varphi"      : ("mi", {}, "var", "&phi;"),
	r"\chi"         : ("mi", {}, "var", "&chi;"),
	r"\psi"         : ("mi", {}, "var", "&psi;"),
	r"\omega"       : ("mi", {}, "var", "&omega;"),
	r"\Alpha"       : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Alpha;"),
	r"\Beta"       : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Beta;"),
	r"\Gamma"       : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Gamma;"),
	r"\Digamma"     : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Gammad;"),
	r"\Delta"       : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Delta;"),
	r"\Zeta"       : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Zeta;"),
	r"\Eta"       : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Eta;"),
	r"\Theta"       : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Theta;"),
	r"\Iota"       : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Iota;"),
	r"\Kappa"       : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Kappa;"),
	r"\Lambda"      : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Lambda;"),
	r"\Mu"       : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Mu;"),
	r"\Nu"       : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Nu;"),
	r"\Xi"          : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Xi;"),
	r"\Omicron"       : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Omicron;"),
	r"\Pi"          : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Pi;"),
	r"\Rho"          : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Rho;"),
	r"\Sigma"       : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Sigma;"),
	r"\Tau"       : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Tau;"),
	r"\Upsilon"     : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Upsilon;"),
	r"\Phi"         : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Phi;"),
	r"\Chi"       : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Chi;"),
	r"\Psi"         : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Psi;"),
	r"\Omega"       : ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "&Omega;"),
}

VARLETTERS = {
	r"\ell" : ("mi", {}, "var", "&ell;"),
}

PREFIX = {
	r"\pm": ("mo", {"form": "prefix"}, "operator", "&pm;"), #Possibly infix tho
	r"\mp": ("mo", {"form": "prefix"}, "operator", "&mp;"),
}

INFIX = {
	r"\times": ("mo", {"form": "infix"}, "operator", "&times;"),
	r"\div": ("mo", {"form": "infix"}, "operator", "&div;"),
	r"\cross": ("mo", {"form": "infix"}, "operator", "&Cross;"),
	r"\ast": ("mo", {"form": "infix"}, "operator", "&ast;"),
	r"\star": ("mo", {"form": "infix"}, "operator", "&star;"),
	r"\circ": ("mo", {"form": "infix"}, "operator", "&#8728;"), #"&#x26ac;",
	r"\bullet": ("mo", {"form": "infix"}, "operator", "&bullet;"),
	r"\cdot": ("mo", {"form": "infix"}, "operator", "&centerdot;"),
	r"\cap": ("mo", {"form": "infix"}, "operator", "&cap;"),
	r"\cup": ("mo", {"form": "infix"}, "operator", "&cup;"),
	r"\given": ("mo", {"form": "infix"}, "operator", "&vert;"),
	r"\uplus": ("mo", {"form": "infix"}, "operator", "&uplus;"),
	r"\sqcap": ("mo", {"form": "infix"}, "operator", "&sqcap;"),
	r"\sqcup": ("mo", {"form": "infix"}, "operator", "&sqcup;"),
	r"\vee": ("mo", {"form": "infix"}, "operator", "&vee;"),
	r"\wedge": ("mo", {"form": "infix"}, "operator", "&wedge;"),
	r"\setminus": ("mo", {"form": "infix"}, "operator", "&setminus;"),
	r"\wr": ("mo", {"form": "infix"}, "operator", "&wr;"),
	r"\diamond": ("mo", {"form": "infix"}, "operator", "&diamond;"),
	r"\bigtriangleup": ("mo", {"form": "infix"}, "operator", "&bigtriangleup;"),
	r"\bigtriangledown": ("mo", {"form": "infix"}, "operator", "&bigtriangledown;"),
	r"\triangleleft": ("mo", {"form": "infix"}, "operator", "&LeftTriangle;"),
	r"\triangleright": ("mo", {"form": "infix"}, "operator", "&RightTriangle;"),
	r"\lhd": ("mo", {"form": "infix"}, "operator", "&LeftTriangle;"), # Same as above
	r"\rhd": ("mo", {"form": "infix"}, "operator", "&RightTriangle;"), # Same as above
	r"\unlhd": ("mo", {"form": "infix"}, "operator", "&LeftTriangleEqual;"),
	r"\unrhd": ("mo", {"form": "infix"}, "operator", "&RightTriangleEqual;"),
	r"\oplus": ("mo", {"form": "infix"}, "operator", "&oplus;"),
	r"\ominus": ("mo", {"form": "infix"}, "operator", "&ominus;"),
	r"\otimes": ("mo", {"form": "infix"}, "operator", "&otimes;"),
	r"\oslash": ("mo", {"form": "infix"}, "operator", "&osol;"),
	r"\odot": ("mo", {"form": "infix"}, "operator", "&odot;"),
	r"\ocirc": ("mo", {"form": "infix"}, "operator", "&ocir;"),
	r"\bigcirc": ("mo", {"form": "infix"}, "operator", "&cir;"),
	r"\dagger": ("mo", {"form": "infix"}, "operator", "&dagger;"),
	r"\ddagger": ("mo", {"form": "infix"}, "operator", "&Dagger;"),
	r"\amalg": ("mo", {"form": "infix"}, "operator", "&#x2a3f;"),

	r"\bowtie": ("mo", {}, "operator", "&bowtie;"),
	r"\Join": ("mo", {}, "operator", "&bowtie;"),#two variants of this one exists in latek
	r"\ltimes": ("mo", {}, "operator", "&ltimes;"),
	r"\rtimes": ("mo", {}, "operator", "&rtimes;"),
	r"\smile": ("mo", {}, "operator", "&smile;"),
	r"\frown": ("mo", {}, "operator", "&frown;"),
}

POSTFIX = {
	r"\!": ("mo", {"form": "infix"}, "operator", "&pm;"),
}

RELATIONS = {
	r"\qeq": ("mo", {}, "relation", "&questeq;"),

	r"\eq": ("mo", {}, "relation", "&equals;"),
	r"\gtreqless": ("mo", {}, "relation", "⋛"),
	r"\lesseqgtr": ("mo", {}, "relation", "⋚"),
	r"\gtrless": ("mo", {}, "relation", "≶"),
	r"\lessgtr": ("mo", {}, "relation", "≷"),
	r"\leq": ("mo", {}, "relation", "&leq;"),
	r"\prec": ("mo", {}, "relation", "&Precedes;"),
	r"\preceq": ("mo", {}, "relation", "&PrecedesEqual;"),
	r"\ll": ("mo", {}, "relation", "&ll;"),
	r"\subset": ("mo", {}, "relation", "&subset;"),
	r"\subseteq": ("mo", {}, "relation", "&subseteq;"),
	r"\sqsubset": ("mo", {}, "relation", "&sqsubset;"),
	r"\sqsubseteq": ("mo", {}, "relation", "&sqsubseteq;"),
	r"\in": ("mo", {}, "relation", "&in;"),
	r"\ni": ("mo", {}, "relation", "&ni;"),
	r"\vdash": ("mo", {}, "relation", "&vdash;"),
	r"\vDash": ("mo", {}, "relation", "&vDash;"),
	r"\geq": ("mo", {}, "relation", "&geq;"),
	r"\succ": ("mo", {}, "relation", "&Succeeds;"),
	r"\succeq": ("mo", {}, "relation", "&SucceedsEqual;"),
	r"\gg": ("mo", {}, "relation", "&gg;"),
	r"\supset": ("mo", {}, "relation", "&supset;"),
	r"\supseteq": ("mo", {}, "relation", "&supseteq;"),
	r"\sqsupset": ("mo", {}, "relation", "&sqsupset;"),
	r"\sqsupseteq": ("mo", {}, "relation", "&sqsupseteq;"),
	r"\dashv": ("mo", {}, "relation", "&dashv;"),
	r"\Dashv": ("mo", {}, "relation", "&Dashv;"),
	r"\equiv": ("mo", {}, "relation", "&equiv;"),
	r"\sim": ("mo", {}, "relation", "&sim;"),
	r"\simeq": ("mo", {}, "relation", "&simeq;"),
	r"\asymp": ("mo", {}, "relation", "&asympeq;"),
	r"\approx": ("mo", {}, "relation", "&approx;"),
	r"\cong": ("mo", {}, "relation", "&cong;"),
	r"\doteq": ("mo", {}, "relation", "&doteq;"),
	r"\propto": ("mo", {}, "relation", "&prop;"),
	r"\models": ("mo", {}, "relation", "&models;"),
	r"\perp": ("mo", {}, "relation", "&#x27c2;"),
	r"\mid": ("mo", {}, "relation", "&mid;"),
	r"\parallel": ("mo", {}, "relation", "&parallel;"),

	r"\implies": ("mo", {}, "arrow", "&Implies;"),
	r"\iff": ("mo", {}, "arrow", "&Leftrightarrow;"),
	r"\equivalently": ("mo", {}, "arrow", "&Leftrightarrow;"),

	r"\mapsto": ("mo", {}, "arrow", "&mapsto;"),
	r"\to": ("mo", {}, "arrow", "&rightarrow;"),
	r"\longmapsto": ("mo", {}, "arrow", "&longmapsto;"),
	r"\leadsto": ("mo", {}, "arrow", "&rarrc;"),
}

NOTRELATIONS = {
	r"\not": ("mo", {}, "relation", "&not;"), #fix

	r"\neq": ("mo", {}, "relation", "&NotEqual;"),
	r"\ngtrless": ("mo", {}, "relation", "≸"),
	r"\nlessgtr": ("mo", {}, "relation", "≹ "),
	r"\nleq": ("mo", {}, "relation", "&NotLess;"),
	r"\nprec": ("mo", {}, "relation", "&NotPrecedes;"),
	r"\npreceq": ("mo", {}, "relation", "&NotPrecedesSlantEqual;"),
	# <Not much less than> would be here
	r"\nsubset": ("mo", {}, "relation", "&nsub;"),
	r"\nsubseteq": ("mo", {}, "relation", "&nsubseteq;"),
	r"\nsqsubset": ("mo", {}, "relation", "&NotSquareSubset;"),
	r"\nsqsubseteq": ("mo", {}, "relation", "&NotSquareSubsetEqual;"),
	r"\nin": ("mo", {}, "relation", "&notin;"),
	r"\nni": ("mo", {}, "relation", "&notni;"),
	r"\nvdash": ("mo", {}, "relation", "&nvdash;"),
	r"\nvDash": ("mo", {}, "relation", "&nvDash;"),
	r"\ngeq": ("mo", {}, "relation", "&NotGreater;"),
	r"\nsucc": ("mo", {}, "relation", "&NotSucceeds;"),
	r"\nsucceq": ("mo", {}, "relation", "&NotSucceedsSlantEqual;"),
	# <Not much greater than> would be here
	r"\nsupset": ("mo", {}, "relation", "&nsup;"),
	r"\nsupseteq": ("mo", {}, "relation", "&nsupseteq;"),
	r"\nsqsupset": ("mo", {}, "relation", "&NotSquareSuperset;"),
	r"\nsqsupseteq": ("mo", {}, "relation", "&NotSquareSupersetEqual;"),
	r"\ndashv": ("mo", {}, "relation", "&ndashv;"),
	#<\nDashv> would be here
	#<\nequiv> would be here
	r"\nsim": ("mo", {}, "relation", "&nsim;"),
	r"\nsimeq": ("mo", {}, "relation", "&nsimeq;"),
	r"\nasymp": ("mo", {}, "relation", "&NotCupCap;"),
	r"\napprox": ("mo", {}, "relation", "&napprox;"),
	r"\ncong": ("mo", {}, "relation", "&ncong;"),
	#<\ndoteq> would be here
	#<npropto> would be here
	#<nmodels> would be here
	#<\nperp> would be here
	r"\nmid": ("mo", {}, "relation", "&nmid;"),
	r"\nparallel": ("mo", {}, "relation", "&nparallel;"),

	r"\nimplies": ("mo", {}, "arrow", "&nRightarrow;"),
	r"\niff": ("mo", {}, "arrow", "&nLeftrightarrow;"),
	r"\nequivalently": ("mo", {}, "arrow", "&nLeftrightarrow;"),
}

ARROWS = {
	r"\leftarrow": ("mo", {}, "arrow", "&leftarrow;"),
	r"\Leftarrow": ("mo", {}, "arrow", "&Leftarrow;"),
	r"\twoheadleftarrow": ("mo", {}, "arrow", "&twoheadleftarrow;"),
	r"\rightarrow": ("mo", {}, "arrow", "&rightarrow;"),
	r"\Rightarrow": ("mo", {}, "arrow", "&Rightarrow;"),
	r"\twoheadrightarrow": ("mo", {}, "arrow", "&twoheadrightarrow;"),
	r"\leftrightarrow": ("mo", {}, "arrow", "&leftrightarrow;"),
	r"\Leftrightarrow": ("mo", {}, "arrow", "&Leftrightarrow;"),
	r"\hookleftarrow": ("mo", {}, "arrow", "&hookleftarrow;"),
	r"\leftharpoonup": ("mo", {}, "arrow", "&leftharpoonup;"),
	r"\leftharpoondown": ("mo", {}, "arrow", "&leftharpoondown;"),
	r"\rightleftharpoons": ("mo", {}, "arrow", "&rightleftharpoons;"),
	r"\longleftarrow": ("mo", {}, "arrow", "&longleftarrow;"),
	r"\Longleftarrow": ("mo", {}, "arrow", "&Longleftarrow;"),
	r"\longrightarrow": ("mo", {}, "arrow", "&longrightarrow;"),
	r"\Longrightarrow": ("mo", {}, "arrow", "&Longrightarrow;"),
	r"\longleftrightarrow": ("mo", {}, "arrow", "&longleftrightarrow;"),
	r"\Longleftrightarrow": ("mo", {}, "arrow", "&Longleftrightarrow;"),
	r"\hookrightarrow": ("mo", {}, "arrow", "&hookrightarrow;"),
	r"\righttharpoonup": ("mo", {}, "arrow", "&rightharpoonup;"),
	r"\rightharpoondown": ("mo", {}, "arrow", "&rightharpoondown;"),
	r"\uparow": ("mo", {}, "arrow", "&uparrow;"),
	r"\Uparrow": ("mo", {}, "arrow", "&Uparrow;"),
	r"\downarrow": ("mo", {}, "arrow", "&downarrow;"),
	r"\Downarrow": ("mo", {}, "arrow", "&Downarrow;"),
	r"\updownarrow": ("mo", {}, "arrow", "&updownarrow;"),
	r"\Updownarrow": ("mo", {}, "arrow", "&Updownarrow;"),
	r"\nearrow": ("mo", {}, "arrow", "&nearrow;"),
	r"\searrow": ("mo", {}, "arrow", "&searrow;"),
	r"\swarrow": ("mo", {}, "arrow", "&swarrow;"),
	r"\nwarrow": ("mo", {}, "arrow", "&nwarrow;"),
}

MISC = {
	r"\ldots": ("mo", {}, "ellipsis", "&hellip;"),
	r"\cdots": ("mo", {}, "ellipsis", "&ctdot;"),
	r"\vdots": ("mo", {}, "ellipsis", "&vellip;"),
	r"\ddots": ("mo", {}, "ellipsis", "&dtdot;"),
	r"\Ddots": ("mo", {}, "ellipsis", "&utdot;"),
	r"\aleph": ("mi", {}, "constant", "&alefsym;"),
	r"\prime": ("mo", {}, "operator", "&prime;"),
	r"\forall": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&forall;"),
	r"\infty": ("mi", {}, "constant", "&infin;"),
	r"\exists": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&exist;"),
	r"\qed": ("mo", {}, "operator", "&#x25a1;"),
	r"\Box": ("mo", {}, "operator", "&#x25a1;"),
	r"\imath": ("mi", {"mathvariant": "italic"}, "constant", "&imath;"),
	r"\jmath": ("mi", {"mathvariant": "italic"}, "constant", "&jmath;"),
	r"\nabla": ("mo", {}, "operator", "&nabla;"),
	r"\del": ("mo", {}, "operator", "&Del;"),
	r"\d": ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "d"),
	r"\partial": ("mo", {}, "operator", "&PartialD;"),
	r"\top": ("mo", {}, "operator", "&top;"),
	r"\bot": ("mo", {}, "operator", "&bot;"), #Left/Right Tack: dashv, vdash)
	r"\angle": ("mo", {}, "operator", "&angle;"),
}

BIG_OP = {
	r"\sum": ("mo", {"form": "prefix", "largeop": "true", "movablelimits": "true"}, "operator", "&sum;"),
	r"\prod": ("mo", {"form": "prefix", "largeop": "true", "movablelimits": "true"}, "operator", "&prod;"),
	r"\coprod": ("mo", {"form": "prefix", "largeop": "true", "movablelimits": "true"}, "operator", "&coprod;"),
	r"\int": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&#x222B;"),
	r"\iint": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&#x222C;"),
	r"\iiint": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&#x222D;"),
	r"\oint": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&#x2232;"),
	r"\bigcap": ("mo", {"form": "prefix", "largeop": "true", "movablelimits": "true"}, "operator", "&bigcap;"),
	r"\intersection": ("mo", {"form": "prefix", "largeop": "true", "movablelimits": "true"}, "operator", "&Intersection;"),
	r"\bigcup": ("mo", {"form": "prefix", "largeop": "true", "movablelimits": "true"}, "operator", "&bigcup;"),
	r"\union": ("mo", {"form": "prefix", "largeop": "true", "movablelimits": "true"}, "operator", "&Union;"),
	r"\bigsqcup": ("mo", {"form": "prefix", "largeop": "true", "movablelimits": "true"}, "operator", "&bigsqcup;"),
	r"\bigvee": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&Vee;"),
	r"\bigwedge": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&Wedge;"),
	r"\bigodot": ("mo", {"form": "prefix", "largeop": "true", "movablelimits": "true"}, "operator", "&bigodot;"),
	r"\bigotimes": ("mo", {"form": "prefix", "largeop": "true", "movablelimits": "true"}, "operator", "&bigotimes;"),
	r"\bigoplus": ("mo", {"form": "prefix", "largeop": "true", "movablelimits": "true"}, "operator", "&bigoplus;"),
	r"\biguplus": ("mo", {"form": "prefix", "largeop": "true", "movablelimits": "true"}, "operator", "&biguplus;"),
}

FUNCTIONS = {
	r"\arg": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "arg"),
	r"\deg": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "deg"),
	r"\cos": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "cos"),
	r"\cosh": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "cosh"),
	r"\sin": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "sin"),
	r"\sinh": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "sinh"),
	r"\tan": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "tan"),
	r"\tanh": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "tanh"),
	r"\exp": ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "exp"),
	r"\log": ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "log"),
	r"\lim": ("mo", {"form": "prefix", "movablelimits": "true"}, "operator", "lim"),
	r"\sup": ("mo", {"form": "prefix", "movablelimits": "true"}, "operator", "sup"),
	r"\limsup": ("mo", {"form": "prefix", "movablelimits": "true"}, "operator", "limsup"),
	r"\inf": ("mo", {"form": "prefix", "movablelimits": "true"}, "operator", "inf"),
	r"\liminf": ("mo", {"form": "prefix", "movablelimits": "true"}, "operator", "liminf"),
	r"\max": ("mo", {"form": "prefix", "rspace": "0", "movablelimits": "true"}, "operator", "max"),
	r"\argmax": ("mo", {"form": "prefix", "movablelimits": "true"}, "operator", "argmax"),
	r"\min": ("mo", {"form": "prefix", "rspace": "0", "movablelimits": "true"}, "operator", "min"),
	r"\argmin": ("mo", {"form": "prefix", "movablelimits": "true"}, "operator", "argmin"),
	r"\det": ("mo", {"form": "prefix", "lspace": "0", "rspace": "0"}, "operator", "det"),
	r"\diag": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "diag"),
	r"\ker": ("mo", {"form": "prefix", "lspace": "0"}, "operator", "ker"),
	r"\mod": ("mo", {"form": "prefix", "lspace": "0"}, "operator", "mod"),
	r"\sgn": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "sgn"),

	r"\fourier": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "&Fouriertrf;"),
	r"\laplace": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "&Laplacetrf;"),
	r"\mellin": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "&Mellintrf;"),
}

SETS = {
	r"\emptyset": ("mi", {}, "constant", "&emptyset;"),
	r"\primes": ("mi", {}, "constant", "&Popf;"),
	r"\naturals": ("mi", {}, "constant", "&naturals;"),
	r"\integers": ("mi", {}, "constant", "&integers;"),
	r"\rationals": ("mi", {}, "constant", "&rationals;"),
	r"\algebraics": ("mi", {}, "constant", "&Aopf;"),
	r"\reals": ("mi", {}, "constant", "&reals;"),
	r"\imaginaries": ("mi", {}, "constant", "&Iopf;"),
	r"\complexes": ("mi", {}, "constant", "&complexes;"),
	r"\quaternions": ("mi", {}, "constant", "&quaternions;"),
	r"\octonions": ("mi", {}, "constant", "&Oopf;"),
	r"\sedenions": ("mi", {}, "constant", "&Sopf;"),
}

LOGIC = {
}

GEOMETRY = {
}

CALCULUS = {
}

CHEMISTRY = {
	r"\alembic": ("mi", {}, "symbol", "&#x2697;"), #⚗
	r"\atom": ("mi", {}, "symbol", "&#x269b;"), #⚛
	r"\radioactive": ("mi", {}, "symbol", "&#x2622;"), #☢
	r"\biohazard": ("mi", {}, "symbol", "&#x2623;"), #☣
	r"\poisonold": ("mi", {}, "symbol", "&#x2620;"), #☠
	r"\equilibrium": ("mo", {}, "operator", "&Equilibrium;"), #⇌
	r"\reverseequilibrium": ("mo", {}, "operator", "&ReverseEquilibrium;"), #⇋
	r"\biequation": ("mo", {}, "operator", "&rightleftarrows;"), #⇄
	r"\requation": ("mo", {}, "operator", "&rightarrow;"), #→
	r"\Requation": ("mo", {}, "operator", "&longrightarrow;"), #⟶
	r"\lequation": ("mo", {}, "operator", "&leftarrow;"), #←
	r"\Lequation": ("mo", {}, "operator", "&longleftarrow;"), #⟵
	r"\aqua": ("ms", {"lquote":"(", "rquote":")"}, "symbol", "aq"), #↑
	r"\liquid": ("ms", {"lquote":"(", "rquote":")"}, "symbol", "l"), #↑
	r"\gas": ("ms", {"lquote":"(", "rquote":")"}, "symbol", "g"), #↑
	r"\solid": ("ms", {"lquote":"(", "rquote":")", "class": "red"}, "symbol", "s"), #↑
	r"\togas": ("mi", {}, "symbol", "&uparrow;"), #↑
	r"\tosolid": ("mi", {}, "symbol", "&downarrow;"), #↓
}

PHYSICS = {
	r"\degree": ("mo", {}, "operator", "&deg;"),
	r"\hbar": ("mi", {}, "constant", "&planck;"),
	r"\h": ("mi", {}, "constant", "&planckh;"),
}
