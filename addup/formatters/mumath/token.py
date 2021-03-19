"""
I felt like this page needed a docstring for some reason.
"""

from collections import namedtuple


MObject = namedtuple("Object", ["tag", "attrib", "type", "text"])
MGroup  = namedtuple("Group",  ["tag", "attrib", "type", "children"])
MAction = namedtuple("Action", ["tag", "attrib", "type", "targs"])
