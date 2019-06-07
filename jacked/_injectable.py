"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``Injectable`` class and the ``injectable`` decorator.
"""
from functools import partial
from typing import Dict, Any
from jacked import _container
from jacked._types import AttrDict


class Injectable:
    """
    Objects of this class hold stuff that can be injected.
    """
    def __init__(
            self,
            *,
            subject: object,
            priority: int,
            singleton: bool,
            meta: Dict[str, Any]):
        """
        Constructor.
        :param subject: the thing that is to be injected.
        :param priority: a number that indicates how jacked should choose
        between candidates.
        :param singleton: if ``True`` and ``subject`` is a class, then only one
        instance is ever injected.
        :param meta: any meta information.
        """
        self._subject = subject
        self._singleton = singleton
        self._meta = meta
        self._priority = priority

    @property
    def name(self) -> str:
        return self._meta['name']

    @property
    def meta(self) -> AttrDict:
        return AttrDict(self._meta)

    @property
    def subject(self) -> object:
        # Set the meta data 'just in time' to allow different meta objects in
        # different Containers.
        result = self._subject
        result.__meta__ = self.meta  # Use the property, not the field.
        return result

    @property
    def singleton(self) -> bool:
        return self._singleton

    @property
    def priority(self) -> int:
        return self._priority


def injectable(
        decorated: object = None,
        *,
        name: str = None,
        priority: int = 0,
        meta: Dict[str, Any] = None,
        singleton: bool = False,
        container: _container.Container = _container.DEFAULT_CONTAINER
):
    """
    A decorator that marks something as injectable.

    Usage example:
    ```
    @injectable
    class Bird(Animal):
        def sound(self):
        return 'tweet'
    ```
    :param decorated: the thing (class, function, method) that is to become
    injectable.
    :param name: the name of that thing, stored in the meta information.
    :param priority: a number that indicates how jacked should choose between
    candidates; higher priorities are more likely to get injected.
    :param meta: any meta information that is added to the injectable.
    :param singleton: if True and ``decorated`` is a class, then a singleton
    instance will be injected for every injection on from ``container``.
    :param container: the registry that stores the new injectable.
    :return: a decorator.
    """
    if decorated:
        return _decorator(name, priority, meta, singleton,
                          container, decorated)
    return partial(_decorator, name, priority, meta, singleton, container)


def _decorator(
        name: str,
        priority: int,
        meta: Dict[str, Any],
        singleton: bool,
        container: _container.Container,
        decorated: object) -> callable:
    # This is the actual decorator that registers the decorated object.
    meta = {
        **(meta or {}),
        'name': name or decorated.__name__
    }
    injectable_inst = Injectable(subject=decorated,
                                 priority=priority,
                                 singleton=singleton,
                                 meta=meta)
    container.register(injectable_inst)
    return decorated
