"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``inject`` function and its required private
functions.
"""
import inspect
from collections import ChainMap
from functools import partial, lru_cache
from pathlib import Path
from typing import List, Dict, Any
from jacked import _state_holder
from jacked._discover import discover
from jacked._exceptions import InjectionError, InvalidUsageError
from jacked._injectable import Injectable
from jacked.matchers._base_matcher import BaseMatcher


def inject(
        decorated: callable = None,
        *,
        state_holder: _state_holder.StateHolder = _state_holder.DEFAULT
) -> callable:
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
    # This function acts as the "actual decorator" if any arguments were passed
    # to `inject`.
    _check_decorated(decorated)
    return lambda *args, **kwargs: _wrapper(decorated, state_holder, *args,
                                            **kwargs)


def _check_decorated(decorated: callable):
    # This function validates the decorated object and raises upon an invalid
    # decoration.
    if isinstance(decorated, type):
        raise InvalidUsageError('The inject decorator can be used on '
                                'callables only.')
    params = inspect.signature(decorated).parameters
    for param_name in params:
        hint = params[param_name].annotation
        if hint != inspect.Parameter.empty:
            _check_hint(hint)


def _check_hint(hint: Any):
    # TODO deze moet ik nog maken!
    pass
    # try:
    #     naked_class = get_naked_class(hint)
    #     if not isinstance(naked_class, type) and not isinstance(naked_class, str):
    #         raise InvalidUsageError('TODO1')
    # except TypeError:
    #     raise
    #     raise InvalidUsageError('TODO2')


def _wrapper(
        decorated: callable,
        state_holder: _state_holder.StateHolder,
        *args,
        **kwargs_):
    # This function is wrapped around the decorated object. It will collect
    # arguments and inject them to `decorated` by providing these arguments.
    signature = inspect.signature(decorated)

    if args:
        # If there are any ordered parameters given, filter them out of the
        # signature to prevent the search for injection candidates:
        filtered_params = list(signature.parameters.values())[len(args):]
        signature = inspect.Signature(filtered_params)

    # Collect the arguments for injection:
    arguments = _collect_arguments(signature, state_holder)
    kwargs_ = ChainMap(kwargs_, arguments)  # Note: kwargs_ takes precedence.

    # Now all arguments are collected, "inject" them into `decorated`:
    return decorated(*args, **kwargs_)


def _collect_arguments(
        signature: inspect.Signature,
        state_holder: _state_holder.StateHolder) -> Dict[str, object]:
    # This function tries to collect arguments for the given signature and
    # returns a dictionary that corresponds to that signature.
    result = {}
    for param_name in signature.parameters:
        if param_name in ('self', 'cls'):
            continue
        param = signature.parameters[param_name]
        # Get all candidates that could be injected according to `signature`:
        candidates = _get_candidates(param, state_holder)
        if not candidates:
            result[param_name] = param.default
            if param.default is inspect.Parameter.empty:
                raise InjectionError('No suitable candidates for "{}".'
                                     .format(param_name), param)
        else:
            # If there are multiple candidates, select one:
            result[param_name] = _choose_candidate(candidates)
    return result


def _get_candidates(
        parameter: inspect.Parameter,
        state_holder: _state_holder.StateHolder) -> List[object]:
    # Search in the known injectables in `state_holder` for all matching
    # candidates.
    candidates = (_match(parameter, injectable, state_holder)
                  for injectable in state_holder.injectables)
    # TODO raise if candidates is empty
    return [candidate for candidate in candidates if candidate]


def _choose_candidate(candidates: List[object]) -> object:
    # From a list of candidates, pick and return one:
    return candidates[0]


def _match(
        parameter: inspect.Parameter,
        injectable: Injectable,
        state_holder: _state_holder.StateHolder) -> object:
    # Check if the given `parameter` matches with the given `injectable`. If
    # there appears to be a match, return what is to be injected (e.g. an
    # instance of a class, a class itself, ...). If no match, return `None`.
    hint = parameter.annotation

    for matcher in _get_matchers():
        if matcher.can_match(hint):
            # Match or no match, return anyway:
            return matcher.match(hint, injectable, state_holder)


@lru_cache()
def _get_matchers() -> List[BaseMatcher]:
    path_to_matchers = str(Path(__file__).parent.joinpath(Path('matchers')))
    modules = discover(path_to_matchers)

    public_elements = [getattr(mod, elem) for mod in modules
                       for elem in dir(mod) if not elem.startswith('_')]
    matchers = [cls() for cls in public_elements if isinstance(cls, type)
                and cls is not BaseMatcher and issubclass(cls, BaseMatcher)]

    matchers.sort(key=lambda m: m.priority(), reverse=True)

    return matchers
