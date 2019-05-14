"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``BaseMatcher``class.
"""
from typing import Any
from jacked._compatibility_impl import get_naked_class
from jacked._injectable import Injectable
from jacked._state_holder import StateHolder


class BaseMatcher:

    def can_match(self, hint):
        if hint is Any:
            return self._matching_type() is Any
        return issubclass(get_naked_class(hint), self._matching_type())

    def match(
            self, hint: object,
            injectable: Injectable,
            state_holder: StateHolder):
        raise NotImplementedError

    def priority(self) -> int:
        raise NotImplementedError

    def _matching_type(self) -> type:
        raise NotImplementedError
