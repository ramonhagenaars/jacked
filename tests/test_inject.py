from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type, List, Callable, Any
from unittest import TestCase
from jacked import inject, injectable
from jacked._container import Container
from jacked._discover import discover
from jacked._exceptions import InvalidUsageError, InjectionError
from test_resources.color import Color


CUSTOM_CONTAINER = Container()


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


@injectable(name='Elephant', meta={'size': 'enormous', 'name': 'overridden'})
class Mouse(Animal):
    def sound(self):
        return 'peep'


@injectable(container=CUSTOM_CONTAINER)
class Goat(Animal):
    def sound(self):
        return 'meh'


# The same object injected in two different contains under different names.
@injectable()
@injectable(container=CUSTOM_CONTAINER, name='Kip')
class Chicken(Animal):
    def sound(self):
        return 'tok'


@injectable()
def func_str_str(x: str) -> str:
    return x.upper()


@injectable()
def func_int_str(x: int) -> str:
    return str(x)


@injectable()
def func_empty_float() -> float:
    return 42.0


@injectable()
def func_list_empty(x: list):
    return x + [1, 2, 3]


@injectable()
def func_cat_str(cat: Cat) -> str:
    return cat.sound()


class TestInject(TestCase):
    @inject()
    def test_simple_injection(self, cat: Cat):
        self.assertEqual('meouw', cat.sound())

    @inject()
    def test_injection_name(self, mouse: Mouse):
        self.assertEqual('Elephant', mouse.__meta__.name)
        self.assertEqual('enormous', mouse.__meta__.size)

    @inject
    def test_simple_injection_without_parentheses(self, cat: Cat):
        self.assertEqual('meouw', cat.sound())

    @inject(container=CUSTOM_CONTAINER)
    def test_injection_with_different_container(self, animal: Animal):
        self.assertEqual('meh', animal.sound())

    def test_injection_with_multiple_containers(self):

        @inject(container=CUSTOM_CONTAINER)
        def func1(chicken: Chicken):
            self.assertEqual('Kip', chicken.__meta__['name'])

        @inject()
        def func2(chicken: Chicken):
            self.assertEqual('Chicken', chicken.__meta__['name'])

        func1()
        func2()

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
        self.assertTrue('peep' in sounds)
        self.assertTrue('meh' not in sounds)  # Different container.

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

    def test_inject_function(self):

        @inject()
        def _func1(callable_: Callable[[int], str]):
            self.assertEqual(func_int_str, callable_)

        @inject()
        def _func2(callables: List[Callable[[str], str]]):
            self.assertEqual(1, len(callables))
            self.assertEqual('HELLO', callables[0]('hello'))

        @inject()
        def _func3(callable_: Callable[[], float]):
            self.assertEqual(func_empty_float, callable_)

        @inject()
        def _func4(callables: List[Callable[[Any], str]]):
            self.assertEqual(3, len(callables))
            self.assertTrue(func_int_str in callables)
            self.assertTrue(func_str_str in callables)

        @inject()
        def _func5(callables: List[Callable[[str], Any]]):
            self.assertEqual(1, len(callables))
            self.assertEqual(func_str_str, callables[0])

        @inject()
        def _func6(callable: Callable[[list], None]):
            self.assertEqual(func_list_empty, callable)

        @inject()
        def _func7(callable: Callable[[Animal], str]):
            self.assertEqual(func_cat_str, callable)

        _func1()
        _func2()
        _func3()
        _func4()
        _func5()
        _func6()
        _func7()

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
