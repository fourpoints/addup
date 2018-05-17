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
	r"\phi"         : ("mi", {}, "var", "&#x3D5;"),
	r"\varphi"      : ("mi", {}, "var", "&phi;"),
	r"\chi"         : ("mi", {}, "var", "&chi;"),
	r"\psi"         : ("mi", {}, "var", "&psi;"),
	r"\omega"       : ("mi", {}, "var", "&omega;"),
	r"\Gamma"       : ("mo", {"form": "prefix"}, "operator", "&Gamma;"),
	r"\Digamma"     : ("mo", {"form": "prefix"}, "operator", "&Gammad;"),
	r"\Delta"       : ("mo", {"form": "prefix"}, "operator", "&Delta;"),
	r"\Theta"       : ("mo", {"form": "prefix"}, "operator", "&Theta;"),
	r"\Lambda"      : ("mo", {"form": "prefix"}, "operator", "&Lambda;"),
	r"\Xi"          : ("mo", {"form": "prefix"}, "operator", "&Xi;"),
	r"\Pi"          : ("mo", {"form": "prefix"}, "operator", "&Pi;"),
	r"\Sigma"       : ("mo", {"form": "prefix"}, "operator", "&Sigma;"),
	r"\Upsilon"     : ("mo", {"form": "prefix"}, "operator", "&Upsilon;"),
	r"\Phi"         : ("mo", {"form": "prefix"}, "operator", "&Phi;"),
	r"\Psi"         : ("mo", {"form": "prefix"}, "operator", "&Psi;"),
	r"\Omega"       : ("mo", {"form": "prefix"}, "operator", "&Omega;"),
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
}

POSTFIX = {
	r"\!": ("mo", {"form": "postfix"}, "operator", "&pm;"),
}

RELATIONS = {
	r"\leq": ("mo", {}, "operator", "&leq;"),
	r"\prec": ("mo", {}, "operator", "&Precedes;"),
	r"\preceq": ("mo", {}, "operator", "&PrecedesEqual;"),
	r"\ll": ("mo", {}, "operator", "&ll;"),
	r"\subset": ("mo", {}, "operator", "&subset;"),
	r"\subseteq": ("mo", {}, "operator", "&subseteq;"),
	r"\sqsubset": ("mo", {}, "operator", "&sqsubset;"),
	r"\sqsubseteq": ("mo", {}, "operator", "&sqsubseteq;"),
	r"\in": ("mo", {}, "operator", "&in;"),
	r"\ni": ("mo", {}, "operator", "&ni;"),
	r"\vdash": ("mo", {}, "operator", "&vdash;"),
	r"\vDash": ("mo", {}, "operator", "&vDash;"),
	r"\geq": ("mo", {}, "operator", "&geq;"),
	r"\succ": ("mo", {}, "operator", "&Succeeds;"),
	r"\succeq": ("mo", {}, "operator", "&SucceedsEqual;"),
	r"\gg": ("mo", {}, "operator", "&gg;"),
	r"\supset": ("mo", {}, "operator", "&supset;"),
	r"\supseteq": ("mo", {}, "operator", "&supseteq;"),
	r"\sqsupset": ("mo", {}, "operator", "&sqsupset;"),
	r"\sqsupseteq": ("mo", {}, "operator", "&sqsupseteq;"),
	r"\dashv": ("mo", {}, "operator", "&dashv;"),
	r"\Dashv": ("mo", {}, "operator", "&Dashv;"),
	r"\equiv": ("mo", {}, "operator", "&equiv;"),
	r"\sim": ("mo", {}, "operator", "&sim;"),
	r"\simeq": ("mo", {}, "operator", "&simeq;"),
	r"\asymp": ("mo", {}, "operator", "&asympeq;"),
	r"\approx": ("mo", {}, "operator", "&approx;"),
	r"\cong": ("mo", {}, "operator", "&cong;"),
	r"\doteq": ("mo", {}, "operator", "&doteq;"),
	r"\propto": ("mo", {}, "operator", "&prop;"),
	r"\models": ("mo", {}, "operator", "&models;"),
	r"\perp": ("mo", {}, "operator", "&#x27c2;"),
	r"\mid": ("mo", {}, "operator", "&#xff5c;"),
	r"\parallel": ("mo", {}, "operator", "&parallel;"),
	r"\bowtie": ("mo", {}, "operator", "&bowtie;"),
	r"\Join": ("mo", {}, "operator", "&bowtie;"),#two variants of this one exists in latek
	r"\ltimes": ("mo", {}, "operator", "&ltimes;"),
	r"\rtimes": ("mo", {}, "operator", "&rtimes;"),
	r"\smile": ("mo", {}, "operator", "&smile;"),
	r"\frown": ("mo", {}, "operator", "&frown;"),
}

NOTRELATIONS = {
	r"\not": ("mo", {}, "operator", "&not;"), #tempfix
	r"\neq": ("mo", {}, "operator", "&NotEqual;"),
	r"\nparallel": ("mo", {}, "operator", "&nparallel;"),
}

ARROWS = {
	r"\leftarrow": ("mo", {}, "operator", "&leftarrow;"),
	r"\Leftarrow": ("mo", {}, "operator", "&Leftarrow;"),
	r"\rightarrow": ("mo", {}, "operator", "&rightarrow;"),
	r"\Rightarrow": ("mo", {}, "operator", "&Rightarrow;"),
		r"\implies": ("mo", {}, "operator", "&Implies;"),
	r"\leftrightarrow": ("mo", {}, "operator", "&leftrightarrow;"),
	r"\Leftrightarrow": ("mo", {}, "operator", "&Leftrightarrow;"),
		r"\iff": ("mo", {}, "operator", "&Leftrightarrow;"),
		r"\equivalently": ("mo", {}, "operator", "&Leftrightarrow;"),
	r"\mapsto": ("mo", {}, "operator", "&mapsto;"),
	r"\hookleftarrow": ("mo", {}, "operator", "&hookleftarrow;"),
	r"\leftharpoonup": ("mo", {}, "operator", "&leftharpoonup;"),
	r"\leftharpoondown": ("mo", {}, "operator", "&leftharpoondown;"),
	r"\rightleftharpoons": ("mo", {}, "operator", "&rightleftharpoons;"),
	r"\longleftarrow": ("mo", {}, "operator", "&longleftarrow;"),
	r"\Longleftarrow": ("mo", {}, "operator", "&Longleftarrow;"),
	r"\longrightarrow": ("mo", {}, "operator", "&longrightarrow;"),
	r"\Longrightarrow": ("mo", {}, "operator", "&Longrightarrow;"),
	r"\longleftrightarrow": ("mo", {}, "operator", "&longleftrightarrow;"),
	r"\Longleftrightarrow": ("mo", {}, "operator", "&Longleftrightarrow;"),
	r"\longmapsto": ("mo", {}, "operator", "&longmapsto;"),
	r"\hookrightarrow": ("mo", {}, "operator", "&hookrightarrow;"),
	r"\righttharpoonup": ("mo", {}, "operator", "&rightharpoonup;"),
	r"\rightharpoondown": ("mo", {}, "operator", "&rightharpoondown;"),
	r"\leadsto": ("mo", {}, "operator", "&rarrc;"),
	r"\uparow": ("mo", {}, "operator", "&uparrow;"),
	r"\Uparrow": ("mo", {}, "operator", "&Uparrow;"),
	r"\downarrow": ("mo", {}, "operator", "&downarrow;"),
	r"\Downarrow": ("mo", {}, "operator", "&Downarrow;"),
	r"\updownarrow": ("mo", {}, "operator", "&updownarrow;"),
	r"\Updownarrow": ("mo", {}, "operator", "&Updownarrow;"),
	r"\nearrow": ("mo", {}, "operator", "&nearrow;"),
	r"\searrow": ("mo", {}, "operator", "&searrow;"),
	r"\swarrow": ("mo", {}, "operator", "&swarrow;"),
	r"\nwarrow": ("mo", {}, "operator", "&nwarrow;"),
}

MISC = {
	r"\ldots": ("mo", {}, "operator", "&hellip;"),
	r"\cdots": ("mo", {}, "operator", "&ctdot;"),
	r"\vdots": ("mo", {}, "operator", "&vellip;"),
	r"\ddots": ("mo", {}, "operator", "&dtdot;"),
	r"\Ddots": ("mo", {}, "operator", "&utdot;"),
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
	r"\partial": ("mo", {}, "operator", "&PartialD;"),
	r"\top": ("mo", {}, "operator", "&top;"),
	r"\bot": ("mo", {}, "operator", "&bot;"), #Left/Right Tack: dashv, vdash)
	r"\angle": ("mo", {}, "operator", "&angle;"),
}

BIG_OP = {
	r"\sum": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&sum;"),
	r"\prod": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&prod;"),
	r"\coprod": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&coprod;"),
	r"\int": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&int;"),
	r"\iint": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&#x222C;"),
	r"\iiint": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&#x222D;"),
	r"\oint": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&#x2232;"),
	r"\bigcap": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&bigcap;"),
	r"\intersection": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&Intersection;"),
	r"\bigcup": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&bigcup;"),
	r"\union": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&Union;"),
	r"\bigsqcup": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&bigsqcup;"),
	r"\bigvee": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&Vee;"),
	r"\bigwedge": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&Wedge;"),
	r"\bigodot": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&bigodot;"),
	r"\bigotimes": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&bigotimes;"),
	r"\bigoplus": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&bigoplus;"),
	r"\biguplus": ("mo", {"form": "prefix", "largeop": "true"}, "operator", "&biguplus;"),
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
	r"\exp": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "exp"),
	r"\log": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "log"),
	r"\lim": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "lim"),
	r"\limsup": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "limsup"),
	r"\liminf": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "liminf"),
	r"\max": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "max"),
	r"\min": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "min"),
	r"\det": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "det"),
	r"\ker": ("mo", {"form": "prefix", "rspace": "0"}, "operator", "ker"),
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
