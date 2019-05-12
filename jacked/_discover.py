"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``discover`` function.
"""
import glob
import sys
from importlib import import_module
from pathlib import Path
from typing import List

from jacked._types import Module


def discover(directory: str = '.') -> List[Module]:
    """
    Discover all modules in the given directory recursively and import them.
    :param directory: the directory in which modules are to be discovered.
    :return: a ``list`` of all discovered modules.
    """
    path = Path(directory)
    abspath = str(path.absolute())
    sys.path.insert(0, abspath)

    path_to_discover = path.joinpath('**/*.py')
    paths = [Path(filename) for filename in
             glob.iglob(str(path_to_discover), recursive=True)]

    return _import(paths)


def _import(paths: List[Path]) -> List[Module]:
    result = []
    for p in paths:
        path_to_module = p.resolve().parent
        sys.path.insert(0, str(path_to_module))
        module_name = p.stem
        try:
            module = import_module(module_name)
            result.append(module)
        except ImportError:
            pass
    return result
