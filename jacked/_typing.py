"""
PRIVATE MODULE: do not import (from) it directly.

This module contains types that are not available by default.
"""
import sys
import typing


T = typing.TypeVar('T')
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


def issubtype(cls: type, clsinfo: type) -> bool:
    """
    Return whether ``cls`` is a subclass of ``clsinfo`` while also considering
    generics.
    :param cls: the subject.
    :param clsinfo: the object.
    :return: True if ``cls`` is a subclass of ``clsinfo`` considering generics.
    """
    info_generic_type, info_args = _split_generic(clsinfo)
    if clsinfo in (typing.Any, object):
        result = True
    elif info_args:
        result = _issubtype_generic(cls, info_generic_type, info_args)
    else:
        result = issubclass(_without_generic(cls), _without_generic(clsinfo))
    return result


def _issubtype_generic(
        cls: type,
        info_generic_type: type,
        info_args: tuple) -> bool:
    # Check if cls is a subtype of info_generic_type, knowing that the latter
    # is a generic type.
    result = False
    cls_generic_type, cls_args = _split_generic(cls)
    if (cls_generic_type == info_generic_type and cls_args
            and len(cls_args) == len(info_args)):
        args_do_correspond = True
        for tup in zip(cls_args, info_args):
            args_do_correspond &= issubtype(*tup)
        result = args_do_correspond
    # Note that issubtype(list, List[...]) is always False.
    # Note that the number of arguments must be equal.
    return result


def _split_generic(t: type) -> \
        typing.Tuple[type, typing.Optional[typing.Tuple[type, ...]]]:
    # Split the given generic type into the type and its args.
    origin = getattr(t, '__origin__', t)
    args_ = getattr(t, '__args__', tuple()) or tuple()
    args = tuple([attr for attr in args_
                  if type(attr) != typing.TypeVar])
    return origin, args


def _without_generic(t: type) -> type:
    # Return type t without any generic type.
    attr = '__origin__'
    if sys.version_info[1] in (5, 6):
        attr = '__extra__'
    return getattr(t, attr, t)
