"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``jacked`` error classes.
"""
import inspect


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
    def __init__(self, msg: str, parameter: inspect.Parameter):
        super(InjectionError, self).__init__(msg)
        self.parameter = parameter
