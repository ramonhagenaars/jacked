"""
PRIVATE MODULE: do not import (from) it directly.

This module contains types that are not available by default.
"""
import typing


Module = type(typing)
NoneType = type(None)


class AttrDict(dict):
    """
    A simple wrapper around the default ``dict`` type that allows object-like
    access to attributes.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        :param args: any args.
        :param kwargs: any kwargs.
        """
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
