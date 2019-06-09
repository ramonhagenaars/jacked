[![Build Status](https://travis-ci.org/ramonhagenaars/jacked.svg?branch=master)](https://travis-ci.org/ramonhagenaars/jacked)
[![Pypi version](https://badge.fury.io/py/jacked.svg)](https://badge.fury.io/py/jsons)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/ramonhagenaars/jacked/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/ramonhagenaars/jacked/?branch=master)
[![codecov](https://codecov.io/gh/ramonhagenaars/jacked/branch/master/graph/badge.svg)](https://codecov.io/gh/ramonhagenaars/jacked)


_NOTE: This project is in ALPHA state_
# jacked ~ *python on roids*

* A light and easy to use dependency injection framework.
* Inject _objects_, _functions_, _classes_ or _lists_ containing any of these.
* Let **jacked** automatically discover your injectables in a package.
* Loose coupling _on the juice_!
* Excellent for making your code testable!

## Install
```
pip install jacked
```

## Usage

### Inject instances
To inject instances, mark a class with the ``injectable`` decorator:
```python
from jacked import injectable

@injectable
class Cat:
    def sound(self):
        return 'meow'
```
You can now inject it in a function anywhere. Place the ``inject`` decorator on 
top of the function or method. Let **jacked** know what type to inject by type 
hinting your parameters:
```python
@inject
def what_sound_does_it_make(cat: Cat):
    print(cat.sound())
    
what_sound_does_it_make()
```

### Inject functions
Injecting functions works similarly. Just make sure that your function has the
proper type hints:

```python
@injectable
def some_func(x: int, y: int) -> str:
    return f'The sum of {x} and {y} is {x + y}'
```
And like with instances, inject as follows:
```python
@inject
def do_something(func: Callable[[int, int], str]):
    print(func(21, 21))
    
do_something()
```
### Inject classes
Assuming that we have the same ``Cat`` injectable like before, we can inject
that class as follows:

```python
from typing import Type

@inject
def do_something(cat_type: Type[Cat]):
    print(cat_type.__name__)
    
do_something()
```


### Inject lists
Let's suppose that we have the following two injectables of the same parent:
```python
class Animal(ABC):
    @abstractmethod
    def sound(self):
        raise NotImplementedError
        
@injectable
class Cat(Animal):
    def sound(self):
        return 'meow'
        
@injectable
class Dog(Animal):
    def sound(self):
        return 'bark'
```
You can now inject them in a list:
```python
@inject
def what_sound_does_it_make(animals: List[Animal]):
    for animal in animals:
        print(f'The {animal.__class__.__name__} does {animal.sound()}')
        
what_sound_does_it_make()
```
You could have also injected a ``list`` of classes or functions by hinting
``List[Type[...]]`` or ``List[Callable[...]]`` (the ``...`` replaced by your
injection target).

### Singletons
You can annotate an injectable as singleton, meaning that if the injectable is 
a class, only one instance is ever injected:

```python
@injectable(singleton=True)
class Dog(Animal):
    def sound(self):
        return 'bark'
```

### Auto discovery
You can let **jacked** discover injectables in some package using the 
``discover`` function:
```python
from jacked import discover

discover('path/to/your/package')
```
All python modules in that package are imported and the injectables are 
registered.
