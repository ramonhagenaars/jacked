import inspect
from jacked._inject import _get_candidates
from jacked._injectable import Injectable
from jacked._state_holder import StateHolder
from jacked.matchers._base_matcher import BaseMatcher


class ListMatcher(BaseMatcher):

    def match(
            self,
            hint: object,
            injectable: Injectable,
            state_holder: StateHolder):
        sub_hint = hint.__args__[0]  # TODO now assuming List!!!
        parameter = inspect.Parameter(name='_', kind=1,
                                      annotation=sub_hint)
        return _get_candidates(parameter, state_holder)

    def _matching_type(self):
        return list

    def priority(self):
        return 10
