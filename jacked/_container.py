"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``StateHolder`` class and the default ``StateHolder``
instance.
"""
from typing import Optional, List, Set, Dict, Tuple
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
        self._injectables: List['jacked.Injectable'] = list()
        self._subjects: Set[str] = set()
        self._instances: Dict[object, Tuple[object, int]] = dict()

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

        inst, _ = self._instances.get(hint, (None, None))
        return inst

    def set_instance(
            self,
            hint: object,
            instance: 'jacked.Injectable',
            priority: int = 0):
        """
        Set an instance for a type hint. If there already is an instance and
        the given priority is lesser than or equal to the priority of the
        existing instance, then the given instance will NOT override the
        existing.
        :param hint: a type hint that describes the object.
        :param instance: an instance for that hint.
        :param priority: the priority of the instance.
        :return: None.
        """
        _, prio_existing = self._instances.get(hint, (None, -1))
        if priority > prio_existing:
            self._instances[hint] = (instance, priority)


DEFAULT_CONTAINER = Container()
