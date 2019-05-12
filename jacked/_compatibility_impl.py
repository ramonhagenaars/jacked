"""
PRIVATE MODULE: do not import (from) it directly.

This module contains functionality for supporting the compatibility with
multiple Python versions.
"""
import sys
import typing


def get_naked_class(cls: type) -> type:
    # Python3.5: typing classes have __extra__
    # Python3.6: typing classes have __extra__
    # Python3.7: typing classes have __origin__
    # Return the non-generic class (e.g. dict) of a generic type (e.g. Dict).
    attr = '__origin__'
    if sys.version_info[1] in (5, 6):
        attr = '__extra__'
    return getattr(cls, attr, cls)


def get_type_hints(func: callable):
    # Python3.5: get_type_hints raises on classes without explicit constructor
    try:
        result = typing.get_type_hints(func)
    except AttributeError:
        result = {}
    return result
