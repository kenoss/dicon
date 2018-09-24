Dicon, simple DI container injection liblary for Python.

---

Dicon is a simple "DI container injection" library.

## FAQ

- Q. Is `dicon` a dependency injection library?
- A. No, it does not support dependency injection.  It supports DI container injection and service (singleton) locator.

## Important points

- Simple to use.
- Clear what it does on each stage.
- Small overhead.

## Features

- `@dicon.inject_di_container` class decorator supports nested DI container injection, without modification on type.
- `dicon.DIContainer` provides class resolver and singleton locating.

### Class resolver, no modification on type

```python
import dicon

class A:
    pass
    
di_container = dicon.DIContainer()
di_container.register[A]()
di_container.freeze()

# Resolve class.
class_A = di_container.resolve[A]
a = class_A()
# dicon.DIContainer does not modify type of the object.
assert type(a) is A
# It only modifies constructor.  (Normally it will be not a problem.)
assert not (class_A is A)
```

### Nested DI container injection

```python
@dicon.inject_di_container('_di_container')
class B:
    _di_container = None # Here we get instance of DIContainer.

    def __init__(self, message):
        print(message, self._di_container)

@dicon.inject_di_container('_di_container')
class C:
    _di_container = None # Here we get instance of DIContainer.

    def __init__(self):
        self._b = self._di_container.resolve[B]('B must be have DIContainer:')

di_container = dicon.DIContainer()
di_container.register[B]()
di_container.register[C]()
di_container.freeze()

di_container.resolve[C]()
# will print 'B must be have DIContainer: ...'
```

### Singleton locating

TBW...

## How it works

1. `@dicon.inject_di_container` modifies `__init__` of given class to make it possible `__init__` can take DIContainer as an argument.
2. `DIContainer.resolve` ties itself to that argument by `functools.partial`.

That's all.

For more details, see [tests](tests).

## Other existing solutions

- Dependency injection
  - There are lots of DI libraries: for example, [injector](https://github.com/alecthomas/injector), [pinject](https://github.com/google/pinject).
    - IMHO, DI is too complex for python.
    - Famous liblaries are too complex and not clear how affect to the program.
    - It seems no one support nested injection.
- Service locator
  - [wired](https://github.com/mmerickel/wired)
    - I personally felt it is too complex.
  - [factoryfactory](https://github.com/jammycakes/factoryfactory)
    - It does not support multiple service locators.
    
I borrowed design of [MicroResolver](https://github.com/neuecc/MicroResolver) in API.
