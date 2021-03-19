from . import UNICODE as U
from . import CONTEXT as C
from . import ACTION as A
from . import CUSTOM as Cu
from ..token import MObject, MGroup, MAction
import html
a = html.unescape("&sum;") #unused

"""
CONTEXT_MAP
UNICODE_MAP
ACTION_MAP
"""

CONTEXT_MAP = dict()
CONTEXT_MAPS = [
    C.COMMON,
    #C.CHEMISTRY,
]

# Update CONTEXT_MAP
for CONTEXT in CONTEXT_MAPS: CONTEXT_MAP.update(CONTEXT)

# --- # --- # --- # --- # --- # --- # --- #

UNICODE_MAP = dict()
UNICODE_MAPS = [
    U.SPACES,
    U.GREEK,
    U.VARLETTERS,
    U.PREFIX,
    U.INFIX,
    U.POSTFIX,
    U.RELATIONS,
    U.NOTRELATIONS,
    U.ARROWS,
    U.MISC,
    U.BIG_OP,
    U.FUNCTIONS,
    U.SETS,
    U.LOGIC,
    U.GEOMETRY,
    U.CALCULUS,
    U.CHEMISTRY,
    U.PHYSICS,

    C.STATISTICS,
]

# Update UNICODE_MAP
for UNICODE in UNICODE_MAPS: UNICODE_MAP.update(UNICODE)

# --- # --- # --- # --- # --- # --- # --- #

SYMBOL_MAP = {
    '\[' : (MAction, ("NONE", {}, "OPENNEXT", None)),
    '\)' : (MAction, ("NONE", {}, "CLOSENEXT", None)),
    '\(' : (MAction, ("NONE", {}, "OPENPREV", None)),
    '\]' : (MAction, ("NONE", {}, "CLOSEPREV", None)),
    r'\\': (MAction, ("NONE", {}, "NEWLINE", "")),
    '\{' : (MAction, ("mo", {"fence": "true"}, "OPEN", "{")),
    '\}' : (MAction, ("mo", {"fence": "true"}, "CLOSE", "}")),

    "\;" : (MObject, ("mspace", {"width": "3pt"}, "hardspace", "")),

    '\.' : (MObject, ("mo", {}, "bracket", "")), #???
    '\|' : (MObject, ("mo", {}, "bracket", "&Vert;")),
    '\,' : (MObject, ("mo", {}, "InvisibleComma", "&ic;")),
    '\*' : (MObject, ("mo", {}, "InvisibleTimes", "&it;")),
    '\¤' : (MObject, ("mo", {}, "ApplyFunction", "&af;")),

    "\!": (MObject, ("mo", {"form": "postfix", "lspace": "0"}, "operator", "!")),
}

# --- # --- # --- # --- # --- # --- # --- #

ACTION_MAP = dict()

ACTION_MAPS = [
    A.GROUPERS,
    A.ACCENTS,
    A.SEPARATORS,
    A.BRACKETS,
    A.ATTRIBUTES,
    Cu.CUSTOM_ACTIONS,
]

# Update ACTION_MAP
for ACTION in ACTION_MAPS: ACTION_MAP.update(ACTION)

# --- # --- # --- # --- # --- # --- # --- #

#dict.get(key, default) === dict.get(key) or default

def GET_CONTEXT_OR_DEFAULT(key):
    mObject = CONTEXT_MAP.get(key)
    if mObject:
        tag, attr, type_, text = mObject
        return MObject(tag, attr.copy(), type_, text)
    return MObject("mi", {}, "var", key)


def GET_SYMBOL_OR_DEFAULT(key):
    MTypeToken = SYMBOL_MAP.get(key)
    if MTypeToken:
        MType, MToken = MTypeToken
        tag, attr, type_, text = MToken
        return MType(tag, attr.copy(), type_, text)
    return MObject("mo", {"class": "UNKNOWN"}, "UNKNOWN", key)


def GET_UNICODE(key):
    mObject = UNICODE_MAP.get(key)
    if mObject:
        tag, attr, type_, text = mObject
        return MObject(tag, attr.copy(), type_, text)
    return None


def GET_ACTION(key):
    mAction = ACTION_MAP.get(key)
    if mAction:
        tag, attr, type_, text = mAction
        return MAction(tag, attr.copy(), type_, text)
    return None


def UPDATE_CONTEXT(CONTEXT):
    CONTEXT_MAP.update(CONTEXT)

def UPDATE_UNICODE(UNICODE):
    UNICODE_MAP.update(UNICODE)

def UPDATE_ACTION(ACTION):
    ACTION_MAP.update(ACTION)


def CLEAR_CONTEXT(CONTEXT):
    for key in CONTEXT:
        CONTEXT_MAP.pop(key, None)

def CLEAR_UNICODE(UNICODE):
    for key in UNICODE:
        UNICODE_MAP.pop(key, None)

def CLEAR_ACTION(ACTION):
    for key in ACTION:
        ACTION_MAP.pop(key, None)
