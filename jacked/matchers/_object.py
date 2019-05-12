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
        if issubclass(injectable.subject, hint):
            matching_type = injectable.subject
            return matching_type()

    def _matching_type(self):
        return object

    def priority(self):
        return 0
