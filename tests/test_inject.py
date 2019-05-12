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
        self.assertEqual('meouw', cat1.sound())
        self.assertEqual('meouw', cat2.sound())
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
        module_names = [module.__name__ for module in discoveries]

        self.assertTrue('red' in module_names)
        self.assertTrue('green' in module_names)
        self.assertTrue('blue' in module_names)

        get_all_colors()
