"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``CallableMatcher``class.
"""
import inspect
from typing import Callable, Tuple, Any, Awaitable
from jacked._compatibility_impl import get_args_and_return_type
from jacked._injectable import Injectable
from jacked._container import Container
from jacked._typing import NoneType, issubtype
from jacked.matchers._base_matcher import BaseMatcher


class CallableMatcher(BaseMatcher):

    def match(
            self,
            hint: object,
            injectable: Injectable,
            container: Container):
        if inspect.isfunction(injectable.subject):
            params_hint, return_hint = get_args_and_return_type(hint)
            return_hint = (inspect.Signature.empty if return_hint is NoneType
                           else return_hint)
            signature = inspect.signature(injectable.subject)
            params_injectable = tuple([signature.parameters[x].annotation
                                       for x in signature.parameters])
            return_injectable = signature.return_annotation
            if inspect.iscoroutinefunction(injectable.subject):
                return_injectable = Awaitable[return_injectable]
            if (self._params_match(params_hint, params_injectable)
                    and self._compatible_with(return_injectable, return_hint)):
                return injectable.subject

    def _matching_type(self):
        return Callable

    def _params_match(self, params_hint: Tuple[type, ...],
                      params_injectable: Tuple[type, ...]) -> bool:
        if len(params_hint) != len(params_injectable):
            return False
        for i, _ in enumerate(params_hint):
            if not self._compatible_with(params_injectable[i], params_hint[i]):
                return False
        return True

    def _compatible_with(self, t1: type, t2: type):
        return t2 is Any or issubtype(t1, t2)
