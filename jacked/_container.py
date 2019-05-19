"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``StateHolder`` class and the default ``StateHolder``
instance.
"""
import jacked


class Container:
    def __init__(self):
        self._injectables = []
        self._subjects = set()

    def register(self, injectable: 'jacked.Injectable'):
        if injectable.subject.__name__ not in self._subjects:
            self._injectables.append(injectable)
            self._subjects.add(injectable.subject.__name__)

    @property
    def injectables(self):
        return self._injectables


DEFAULT = Container()
