"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``jacked`` error classes.
"""
import inspect
from typing import Union


class JackedError(Exception):
    """
    Base class for all ``jacked`` errors.
    """


class InvalidUsageError(JackedError):
    """
    Raised when ``jacked`` was used in the wrong manner (e.g. decorating a
    class with ``@inject``).
    """


class InjectionError(JackedError):
    """
    Raised when injection failed.
    """
    def __init__(self, msg: str, subject: Union[inspect.Parameter, type]):
        """
        Constructor.
        :param msg: the message of the error.
        :param subject: a parameter in case of a decorator injection, a type in
        case of ``inject_here`` was used.
        """
        super(InjectionError, self).__init__(msg)
        self.subject = subject
