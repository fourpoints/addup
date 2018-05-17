"""
I felt like this page needed a docstring for some reason.
"""

import collections

MObject = collections.namedtuple("Object", ["tag", "attr", "type", "text"])
MGroup  = collections.namedtuple("Group",  ["tag", "attr", "type", "children"])
MAction = collections.namedtuple("Action", ["tag", "attr", "type", "targs"])
