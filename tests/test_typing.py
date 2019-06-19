from typing import List, Any
from unittest import TestCase
from jacked._typing import issubtype


class TestTyping(TestCase):
    def test_any(self):
        self.assertTrue(issubtype(list, Any))
        self.assertTrue(issubtype(List[str], Any))
        self.assertTrue(issubtype(str, Any))

    def test_issubtype_list(self):
        self.assertTrue(issubtype(list, list))
        self.assertTrue(issubtype(list, List))
        self.assertTrue(issubtype(List, List))
        self.assertTrue(issubtype(list, list))
        self.assertTrue(issubtype(List[str], List))
        self.assertTrue(issubtype(List[str], list))
        self.assertTrue(issubtype(List[str], List[str]))
        self.assertTrue(issubtype(List[List[List[List[str]]]], List[List[List[List[str]]]]))
        self.assertTrue(not issubtype(List[int], List[str]))
        self.assertTrue(not issubtype(List[List[List[List[str]]]], List[List[List[List[int]]]]))
        self.assertTrue(not issubtype(list, List[str]))
        self.assertTrue(not issubtype(List, List[str]))
