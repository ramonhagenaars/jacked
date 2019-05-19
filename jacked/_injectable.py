"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``Injectable`` class and the ``injectable`` decorator.
"""
from functools import partial
from jacked import _container


class Injectable:
    """
    Objects of this class hold stuff that can be injected.
    """
    def __init__(self, subject, name):
        """
        Constructor.
        :param subject: the thing that is to be injected.
        :param name: the name of that thing.
        """
        self.subject = subject
        self.name = name


def injectable(
        decorated: object = None,
        *,
        name: str = None,
        container: _container.Container = _container.DEFAULT
):
    """
    A decorator that marks something as injectable.

    Usage example:

        @injectable
        class Bird(Animal):
            def sound(self):
                return 'tweet'

    :param decorated: the thing (class, function, method) that is to become
    injectable.
    :param name: the name of that thing.
    :param container: the registry that stores the new injectable.
    :return:
    """
    if decorated:
        return _decorator(name, container, decorated)
    return partial(_decorator, name, container)


def _decorator(
        name: str,
        container: _container.Container,
        decorated: object) -> callable:
    # This is the actual decorator that registers the decorated object.
    name_ = name or decorated.__name__
    injectable_inst = Injectable(decorated, name_)
    container.register(injectable_inst)
    return decorated
