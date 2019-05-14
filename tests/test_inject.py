from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type, List
from unittest import TestCase
from jacked import inject, injectable
from jacked._discover import discover
from jacked._exceptions import InvalidUsageError, InjectionError
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

    def test_inject_with_default(self):

        class NotInjectable:
            pass

        @inject()
        def _func(cat: Cat, obj: NotInjectable = 42):
            self.assertEqual('meouw', cat.sound())
            self.assertEqual(42, obj)

        @inject()
        def _func2(animal: Cat = Dog()):
            # Dog is a default value but should be overridden by the injection.
            self.assertEqual('meouw', animal.sound())

        _func()
        _func2()

    def test_inject_with_given_values(self):

        @inject()
        def _func(animal: Cat, another_animal: Bird):
            self.assertEqual('bark', animal.sound())
            self.assertEqual('tweet', another_animal.sound())

        class C:
            @inject()
            def method(self, animal: Cat, another_animal: Bird):
                outer_self.assertEqual('bark', animal.sound())
                outer_self.assertEqual('tweet', another_animal.sound())

        outer_self = self

        _func(animal=Dog())
        _func(Dog())

        C().method(animal=Dog())
        C().method(Dog())

    def test_inject_on_class(self):
        with self.assertRaises(InvalidUsageError):
            @inject()
            class C:
                pass

    def test_inject_fail(self):

        class NotInjectable:
            pass

        @inject()
        def _func(obj: NotInjectable):
            pass

        with self.assertRaises(InjectionError):
            _func()

        try:
            _func()
        except InjectionError as err:
            self.assertEqual('obj', err.parameter.name)

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

    # TODO: add a test with a failing import for discovery
