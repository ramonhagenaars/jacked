"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``StateHolder`` class and the default ``StateHolder``
instance.
"""
import jacked


class Container:
    def __init__(self):
        self._injectables = list()
        self._subjects = set()
        self._instances = dict()

    def register(self, injectable: 'jacked.Injectable'):
        if injectable.name not in self._subjects:
            self._injectables.append(injectable)
            self._subjects.add(injectable.subject.__name__)

    @property
    def injectables(self):
        return self._injectables

    def get_instance(self, hint: object) -> object:
        return self._instances.get(hint, None)

    def set_instance(self, hint: object, instance: object):
        self._instances[hint] = instance


DEFAULT = Container()
