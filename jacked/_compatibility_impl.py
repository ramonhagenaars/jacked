"""
PRIVATE MODULE: do not import (from) it directly.

This module contains functionality for supporting the compatibility with
multiple Python versions.
"""
import sys


def get_naked_class(cls: type) -> type:
    # Python3.5: typing classes have __extra__
    # Python3.6: typing classes have __extra__
    # Python3.7: typing classes have __origin__
    # Return the non-generic class (e.g. dict) of a generic type (e.g. Dict).
    attr = '__origin__'
    if sys.version_info[1] in (5, 6):
        attr = '__extra__'
    return getattr(cls, attr, cls)
