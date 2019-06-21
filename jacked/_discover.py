"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``discover`` function.
"""
import glob
import sys
from importlib import import_module
from pathlib import Path
from typing import List
from jacked._typing import Module


def discover(directory: str = '.') -> List[Module]:
    """
    Discover all modules in the given directory recursively and import them.
    :param directory: the directory in which modules are to be discovered.
    :return: a ``list`` of all discovered modules.
    """
    paths = _find_paths(directory, '**/*.py', True)
    return _import(paths)


def _find_paths(directory: str, pattern: str, recursive: bool) -> List[Path]:
    # Find all paths in the given directory with the given pattern and return
    # them in a list.
    path = Path(directory)
    abspath = str(path.absolute())
    sys.path.insert(0, abspath)
    path_to_discover = path.joinpath(pattern)
    paths = [Path(filename) for filename in
             glob.iglob(str(path_to_discover), recursive=recursive)]
    return paths


def _import(paths: List[Path]) -> List[Module]:
    # Import the given list of paths and return the Module instances of the
    # successfully imported modules.
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
