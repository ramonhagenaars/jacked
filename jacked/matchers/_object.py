"""
PRIVATE MODULE: do not import (from) it directly.

This module contains the ``ObjectMatcher``class.
"""
import inspect
from jacked._injectable import Injectable
from jacked._container import Container
from jacked.matchers._base_matcher import BaseMatcher


class ObjectMatcher(BaseMatcher):

    def match(
            self,
            hint: object,
            injectable: Injectable,
            container: Container):
        # The hint is a regular type, so we're expecting to inject an instance.
        if (inspect.isclass(injectable.subject)
                and issubclass(injectable.subject, hint)):
            if injectable.singleton:
                if not container.get_instance(hint):
                    container.set_instance(hint, injectable.subject())
                result = container.get_instance(hint)
            else:
                result = injectable.subject()
            return result

    def _matching_type(self):
        return object

    def priority(self):
        return 0  # The lowest priority.
