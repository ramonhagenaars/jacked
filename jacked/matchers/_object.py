"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``ObjectMatcher``class.
"""
import inspect
from jacked._injectable import Injectable
from jacked._state_holder import StateHolder
from jacked.matchers._base_matcher import BaseMatcher


class ObjectMatcher(BaseMatcher):

    def match(
            self,
            hint: object,
            injectable: Injectable,
            state_holder: StateHolder):
        # The hint is a regular type, so we're expecting to inject an instance.
        if (inspect.isclass(injectable.subject)
                and issubclass(injectable.subject, hint)):
            return injectable.subject()

    def _matching_type(self):
        return object

    def priority(self):
        return 0  # The lowest priority.
