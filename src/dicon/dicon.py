import copy
import functools
import inspect
import itertools
from types import MappingProxyType
from typing import Callable

from .util import list_index


__all__ = [
    'DIContainerMissingError',
    'ClassResolutionNotRegisteredError',
    'inject_di_container',
    'DIContainer',
]


###
### Constant
###

_INIT_ARG_NAME_NAME = '__inject_di_container_init_arg_name_di_container__'


###
### Auxiliary functions
###

def _get_non_conflict_param_name(func: Callable, param_format: str) -> str:
    keys = list(inspect.signature(func).parameters.keys())
    for i in itertools.count(start=0, step=1):
        name = param_format.format(i)
        if name not in keys:
            return name

###
### Exceptions
###

class DIContainerMissingError(Exception):
    def __init__(self, cls):
        self.message = 'DI container missing for class `{}`.  Use `dicon.hoge.resolve[]` to create instances.'.format(cls.__name__)

    def __str__(self):
        return self.message


class ClassResolutionNotRegisteredError(Exception):
    def __init__(self, cls):
        self.message = 'class `{}` is not registered to DI container.'.format(cls.__name__)

    def __str__(self):
        return self.message


###
### Class decorator @inject_di_container
###

class inject_di_container:
    def __init__(self, locator_key: str):
        self._locator_key = locator_key

    def __call__(self, cls):
        assert not hasattr(cls, _INIT_ARG_NAME_NAME)

        init_arg_name_di_container = _get_non_conflict_param_name(cls.__init__, '__inject_di_container_di_container_{}')
        setattr(cls, _INIT_ARG_NAME_NAME, init_arg_name_di_container)

        original__init__ = cls.__init__
        locator_key = self._locator_key

        def modified__init__(self_, *args, **keywords):
            if init_arg_name_di_container not in keywords:
                raise DIContainerMissingError(cls)
            setattr(self_, locator_key, keywords[init_arg_name_di_container])
            del keywords[init_arg_name_di_container]
            original__init__(self_, *args, **keywords)

        added_param = inspect.Parameter(
            init_arg_name_di_container,
            inspect.Parameter.KEYWORD_ONLY
        )
        orig_params = list(inspect.signature(cls.__init__).parameters.values())
        VAR_KEYWORD = inspect.Parameter.VAR_KEYWORD
        i = list_index(orig_params, default=len(orig_params), pred=lambda p: p.kind == VAR_KEYWORD)
        params = orig_params[:i] + [added_param] + orig_params[i:]
        modified__init__.__signature__ = inspect.Signature(params)
        cls.__init__ = modified__init__

        return cls


###
### DI container
###

class DIContainer:
    register = None
    resolve = None

    def __init__(self):
        self._factory = {}
        self.singleton = {}
        self._freezed = False
        self.resolve = _Resolver(self)
        self.register = _Registerer(self)

    def clone(self):
        di_container = DIContainer()
        di_container._factory = copy.copy(self._factory)
        di_container.singleton = copy.copy(self.singleton)
        di_container._freezed = self._freezed
        return di_container

    def freeze(self):
        assert not self._freezed
        self._factory = MappingProxyType(self._factory)
        self.singleton = MappingProxyType(self.singleton)
        self._freezed = True

    def register_singleton(self, key, obj):
        self.singleton[key] = obj


class _Resolver:
    def __init__(self, di_container):
        self._di_container = di_container

    def __getitem__(self, cls):
        if cls not in self._di_container._factory:
            raise ClassResolutionNotRegisteredError(cls)
        return self._di_container._factory[cls]


class _Registerer:
    def __init__(self, di_container):
        self._di_container = di_container

    def __getitem__(self, key):
        assert not self._di_container._freezed

        return functools.partial(self._register, key)

    def _register(self, key):
        if type(key) is tuple:
            assert len(key) == 2, \
                'invalid argument'
            interface, concrete = key
            assert inspect.isclass(interface)
            assert inspect.isclass(concrete)
            assert issubclass(concrete, interface), \
                'In `dicon.DIContainer.register[interface, concrete]`, concrete must be subclass of interface'

            if hasattr(interface, _INIT_ARG_NAME_NAME):
                partial_args = {getattr(interface, _INIT_ARG_NAME_NAME): self._di_container}
                self._di_container._factory[interface] = functools.partial(cls, **partial_args)
            else:
                self._di_container._factory[interface] = concrete
        else:
            cls = key
            assert inspect.isclass(cls)

            if hasattr(cls, _INIT_ARG_NAME_NAME):
                partial_args = {getattr(cls, _INIT_ARG_NAME_NAME): self._di_container}
                self._di_container._factory[cls] = functools.partial(cls, **partial_args)
            else:
                raise Exception('class `{}` is not available for syntax `dicon.DIContainer.resister[cls]`.'.format(cls))
