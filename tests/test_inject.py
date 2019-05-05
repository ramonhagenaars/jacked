from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type, List
from unittest import TestCase
from jacked import inject, injectable
from jacked._discover import discover
from test_resources.color import Color


class Animal(ABC):
    @abstractmethod
    def sound(self):
        raise NotImplementedError


@injectable()
class Dog(Animal):
    def sound(self):
        return 'bark'


@injectable  # No parentheses.
class Cat(Animal):
    def sound(self):
        return 'meouw'


@injectable()
class Bird(Animal):
    def sound(self):
        return 'tweet'


class TestInject(TestCase):
    @inject()
    def test_simple_injection(self, cat: Cat):
        self.assertEqual('meouw', cat.sound())

    @inject
    def test_simple_injection_without_parentheses(self, cat: Cat):
        self.assertEqual('meouw', cat.sound())

    @inject()
    def test_inject_multiple(self, cat1: Cat, cat2: Cat):
        self.assertNotEqual(cat1, cat2)

    @inject()
    def test_inject_class(self, t: Type[Cat]):
        self.assertEqual(Cat, t)

    @inject()
    def test_inject_list(self, animals: List[Animal]):
        sounds = set([animal.sound() for animal in animals])
        self.assertTrue('bark' in sounds)
        self.assertTrue('meouw' in sounds)
        self.assertTrue('tweet' in sounds)

    @inject()
    def test_inject_list_of_classes(self, animals: List[Type[Animal]]):
        sounds = set([animal().sound() for animal in animals])
        self.assertTrue('bark' in sounds)
        self.assertTrue('meouw' in sounds)
        self.assertTrue('tweet' in sounds)

    def test_inject_on_class(self):
        with self.assertRaises(Exception):
            @inject()
            class C:
                pass

    def test_inject_with_discovery(self):

        @inject()
        def get_all_colors(colors: List[Color]):
            color_names = set([color.name() for color in colors])
            self.assertEqual(3, len(color_names))
            self.assertTrue('RED' in color_names)
            self.assertTrue('GREEN' in color_names)
            self.assertTrue('BLUE' in color_names)

        p = Path(__file__).parent.parent.joinpath('test_resources/injectables')
        discoveries = discover(str(p))

        self.assertTrue('red' in discoveries)
        self.assertTrue('green' in discoveries)
        self.assertTrue('blue' in discoveries)

        get_all_colors()
