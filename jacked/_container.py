"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``StateHolder`` class and the default ``StateHolder``
instance.
"""
from typing import Optional
import jacked


class Container:
    """
    An instance of ``Container`` holds registered injectables and can be used
    to inject from.
    """
    def __init__(self):
        """
        Constructor.
        """
        self._injectables = list()
        self._subjects = set()
        self._instances = dict()

    def register(self, injectable: 'jacked.Injectable'):
        """
        Register the given ``Injectable`` to this ``Container``.
        :param injectable: the ``Injectable`` that is to be registered.
        :return: None.
        """
        if injectable.name not in self._subjects:
            self._injectables.append(injectable)
            self._subjects.add(injectable.subject.__name__)

    @property
    def injectables(self):
        """
        Return all ``Injectables`` that were registered to this ``Container``.
        :return: a list of all ``Injectables``.
        """
        return self._injectables

    def get_instance(self, hint: object) -> Optional[object]:
        """
        Return the instance that corresponds to the given hint if there is an
        instance set.
        :param hint: a type hint that describes the object.
        :return: an instance for that hint or None.
        """
        return self._instances.get(hint, None)

    def set_instance(self, hint: object, instance: object):
        """
        Set an instance for a type hint.
        :param hint: a type hint that describes the object.
        :param instance: an instance for that hint.
        :return: None.
        """
        self._instances[hint] = instance


DEFAULT = Container()
