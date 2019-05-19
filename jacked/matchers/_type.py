"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``TypeMatcher``class.
"""
import inspect
from jacked._injectable import Injectable
from jacked._state_holder import StateHolder
from jacked.matchers._base_matcher import BaseMatcher


class TypeMatcher(BaseMatcher):

    def match(
            self,
            hint: object,
            injectable: Injectable,
            state_holder: StateHolder):
        cls = hint.__args__[0]  # TODO assumption!
        if (inspect.isclass(injectable.subject)
                and issubclass(injectable.subject, cls)):
            return injectable.subject

    def _matching_type(self):
        return type

    def priority(self):
        return 200
