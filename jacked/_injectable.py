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
    def __init__(self, subject: object, meta: Dict[str, Any]):
        """
        Constructor.
        :param subject: the thing that is to be injected.
        :param meta: any meta information.
        """
        self._subject = subject
        self._meta = meta

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


def injectable(
        decorated: object = None,
        *,
        name: str = None,
        meta: Dict[str, Any] = None,
        container: _container.Container = _container.DEFAULT
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
    :param meta: any meta information that is added to the injectable.
    :param container: the registry that stores the new injectable.
    :return:
    """
    if decorated:
        return _decorator(name, meta, container, decorated)
    return partial(_decorator, name, meta, container)


def _decorator(
        name: str,
        meta: Dict[str, Any],
        container: _container.Container,
        decorated: object) -> callable:
    # This is the actual decorator that registers the decorated object.
    meta = {
        **(meta or {}),
        'name': name or decorated.__name__
    }
    injectable_inst = Injectable(decorated, meta)
    container.register(injectable_inst)
    return decorated
