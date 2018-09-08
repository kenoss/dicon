import unittest

import yadi

import inspect


@yadi.inject_di_container('_di_container')
class Duck:
    _di_container = None # type: yadi.DIContainer

    def __init__(self, prefix: str, suffix: str = ''):
        self._prefix = prefix
        self._suffix = suffix

    def quack(self) -> str:
        return self._prefix + 'quack' + self._suffix


class OriginalDuck:
    _di_container = None # type: yadi.DIContainer

    def __init__(self, prefix: str, suffix: str = ''):
        pass


class TestInitMethod(unittest.TestCase):
    def test_init_args_are_collectly_passed(self):
        di_container = yadi.DIContainer()
        di_container.register[Duck]()
        di_container.freeze()

        with self.subTest('keywords not passed'):
            duck = di_container.resolve[Duck]('prefix ')

            self.assertEqual(
                duck.quack(),
                'prefix quack'
            )

        with self.subTest('keywords passed'):
            duck = di_container.resolve[Duck]('prefix ', suffix=' suffix')

            self.assertEqual(
                duck.quack(),
                'prefix quack suffix'
            )

    def test_type_annotation_is_preserved(self):
        duck_params = inspect.signature(Duck).parameters
        orig_params = inspect.signature(OriginalDuck).parameters

        # The key `'__inject_di_container_di_container_{}'.format(?)` is added.
        self.assertEqual(
            len(duck_params.keys()),
            len(orig_params.keys()) + 1
        )

        # The other parameters are preserved.
        for key in orig_params:
            self.assertEqual(
                duck_params[key],
                orig_params[key]
            )
