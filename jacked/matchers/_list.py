"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``ListMatcher``class.
"""
import inspect
from jacked._inject import _get_candidates
from jacked._injectable import Injectable
from jacked._container import Container
from jacked.matchers._base_matcher import BaseMatcher


class ListMatcher(BaseMatcher):

    def match(
            self,
            hint: object,
            injectable: Injectable,
            container: Container):
        sub_hint = getattr(hint, '__args__', [None])[0]
        parameter = inspect.Parameter(name='_', kind=1,
                                      annotation=sub_hint)
        return _get_candidates(parameter, container)

    def _matching_type(self):
        return list
