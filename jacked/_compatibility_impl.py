"""
PRIVATE MODULE: do not import (from) it directly.

This module contains functionality for supporting the compatibility with
multiple Python versions.
"""
import sys
from typing import (
    get_type_hints as get_type_hints_,
    Type,
    Callable,
    Dict,
    Tuple,
    Optional)


def get_naked_class(cls: type) -> type:
    """
    Return the given type without generics. For example, ``List[int]`` will
    result in ``List``.
    :param cls: the type that should be stripped off its generic type.
    :return: a type without generics.
    """
    # Python3.5: typing classes have __extra__
    # Python3.6: typing classes have __extra__
    # Python3.7: typing classes have __origin__
    # Return the non-generic class (e.g. dict) of a generic type (e.g. Dict).
    attr = '__origin__'
    if sys.version_info[1] in (5, 6):
        attr = '__extra__'
    return getattr(cls, attr, cls)


def get_type_hints(func: callable) -> Dict[str, type]:
    """
    Return the type hints of the parameters of the given callable.
    :param func: the callable of which the type hints are to be returned.
    :return: a dict with parameter names and their types.
    """
    # Python3.5: get_type_hints raises on classes without explicit constructor
    try:
        result = get_type_hints_(func)
    except AttributeError:
        result = {}
    return result


def get_args_and_return_type(
        hint: Type[Callable]) -> Tuple[Optional[Tuple[type]], Optional[type]]:
    """
    Get the argument types and the return type of a callable type hint
    (e.g. ``Callable[[int], str]).

    Example:
    ```
    arg_types, return_type = get_args_and_return_type(Callable[[int], str])
    # args_types is (int, )
    # return_type is str
    ```

    Example for when ``hint`` has no generics:
    ```
    arg_types, return_type = get_args_and_return_type(Callable)
    # args_types is None
    # return_type is None
    ```
    :param hint: the callable type hint.
    :return: a tuple of the argument types (as a tuple) and the return type.
    """
    if hint in (callable, Callable):
        arg_types = None
        return_type = None
    elif hasattr(hint, '__result__'):
        arg_types = hint.__args__
        return_type = hint.__result__
    else:
        arg_types = hint.__args__[0:-1]
        return_type = hint.__args__[-1]
    return arg_types, return_type
