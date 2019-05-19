"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``BaseMatcher``class.
"""
from typing import Any, Optional
from jacked._compatibility_impl import get_naked_class
from jacked._injectable import Injectable
from jacked._state_holder import StateHolder


class BaseMatcher:
    """
    This is the base class for all matchers. A matcher tries to match some type
    hint with the type it can handle. For example, if a ``list`` is hinted, the
    ``ListMatcher`` should be able to match it and will handle the injection of
    a ``list``.
    """

    def can_match(self, hint: object) -> bool:
        """
        Determine whether this matcher can match the given ``hint``.
        :param hint: the type hint that is to be matched.
        :return: ``True`` if this matcher can handle ``hint``.
        """
        if hint is Any:
            return self._matching_type() is Any
        try:
            return issubclass(get_naked_class(hint), self._matching_type())
        except TypeError:
            return False

    def match(
            self,
            hint: object,
            injectable: Injectable,
            state_holder: StateHolder) -> Optional[object]:
        """
        See if there is a match between ``hint`` and the ``injectable``. If
        there is a match, return an object that corresponds to ``hint``.
        Otherwise, return ``None``.
        :param hint: the type hint that is to be matched.
        :param injectable: the ``Injectable`` that may be a match for ``hint``.
        :param state_holder: the instance that contains all injectables.
        :return: an object that corresponds to ``hint`` or ``None``.
        """
        raise NotImplementedError

    def priority(self) -> int:
        """
        Determine the priority of this matcher; whether ``can_match`` of this
        matcher should be invoked before or after that of other matchers. A
        higher integer corresponds to a higher priority and thus an earlier
        invocation of ``can_match``.
        :return: the priority of this matcher as a number (0 is lowest).
        """
        return 100  # Default.

    def _matching_type(self) -> type:
        """
        Return the type this matcher can handle.
        :return: the type that can be handled by this matcher.
        """
        raise NotImplementedError
