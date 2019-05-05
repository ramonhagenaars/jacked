"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``inject`` function and its required private
functions.
"""
import inspect
from collections import ChainMap
from functools import partial
from typing import List, Dict, Callable
from jacked import _state_holder
from jacked._injectable import Injectable


def inject(
        decorated: callable = None,
        *,
        state_holder: _state_holder.StateHolder = _state_holder.DEFAULT
):
    """
    Decorator that will inject all parameters that were not already explicitly
    provided.

    Usage example:

        @inject
        def func(x: SomeClass):
            x.some_func()  # x is now an instance of SomeClass.

    :param decorated: the callable that is decorated.
    :param state_holder: the storage that is used that contains all
    ``Injectables``.
    :return: a decorator.
    """
    if decorated:
        _check_decorated(decorated)
        return lambda *args, **kwargs: _wrapper(decorated, state_holder, *args,
                                                **kwargs)
    return partial(_decorator, state_holder=state_holder)


def _decorator(
        decorated: callable,
        state_holder: _state_holder.StateHolder) -> callable:
    _check_decorated(decorated)
    return lambda *args, **kwargs: _wrapper(decorated, state_holder, *args,
                                            **kwargs)


def _check_decorated(decorated: callable):
    if isinstance(decorated, type):
        raise Exception('The inject decorator can be used on callables only.')  # TODO use custom exception


def _wrapper(
        decorated: callable,
        state_holder: _state_holder.StateHolder,
        *args,
        **kwargs_):
    signature = inspect.signature(decorated)
    arguments = _get_arguments(signature, state_holder)
    kwargs_ = ChainMap(kwargs_, arguments)
    return decorated(*args, **kwargs_)


def _get_arguments(
        signature: inspect.Signature,
        state_holder: _state_holder.StateHolder) -> Dict[str, object]:
    result = {}
    for param_name in signature.parameters:
        if param_name in ('self', 'cls'):
            continue  # TODO see if this can be better
        candidates = _get_candidates(signature.parameters[param_name],
                                     state_holder)
        if not candidates:
            raise Exception('No suitable candidates.')  # TODO use custom exception

        result[param_name] = _choose_candidate(candidates)
    return result


def _get_candidates(
        parameter: inspect.Parameter,
        state_holder: _state_holder.StateHolder) -> List[object]:
    candidates = (_match(parameter, injectable, state_holder)
                  for injectable in state_holder.injectables)
    return [candidate for candidate in candidates if candidate]


def _choose_candidate(candidates: List[object]) -> object:
    return candidates[0]  # TODO


def _match(
        parameter: inspect.Parameter,
        injectable: Injectable,
        state_holder: _state_holder.StateHolder) -> object:
    hint = parameter.annotation

    # TODO: move matchers to separate modules.
    if issubclass(hint, type):
        # The hint is a generic type, so we're injecting a type.
        cls = hint.__args__[0]  # TODO naive
        if issubclass(injectable.subject, cls):
            return injectable.subject
    elif issubclass(hint, list):
        sub_hint = hint.__args__[0]  # TODO naive
        parameter = inspect.Parameter(name='_', kind=1, annotation=sub_hint)
        return _get_candidates(parameter, state_holder)
    elif issubclass(hint, object):
        # The hint is a regular type, so we're expecting to inject an instance.
        if issubclass(injectable.subject, hint):
            matching_type = injectable.subject
            return matching_type()  # TODO try except
