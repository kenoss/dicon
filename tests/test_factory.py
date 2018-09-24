import unittest

import dicon


class AnimalChild:
    def quack(self) -> str:
        raise NotImplementedError()


class AnimalChildA(AnimalChild):
    def __init__(self):
        pass

    def quack(self) -> str:
        return 'AnimalChildA.quack'


class AnimalChildB(AnimalChild):
    def __init__(self):
        pass

    def quack(self) -> str:
        return 'AnimalChildB.quack'


@dicon.inject_di_container('_di_container')
class Animal:
    _di_container = None # type: dicon.DIContainer

    def __init__(self):
        pass

    def quack(self) -> str:
        return 'Animal.quack'

    def spawn_child(self) -> AnimalChild:
        return self._di_container.resolve[AnimalChild]()


class TestFactory(unittest.TestCase):
    def test_factory(self):
        target_AnimalChild = AnimalChildA
        with self.subTest(target_AnimalChild = target_AnimalChild):
            di_container = dicon.DIContainer()
            di_container.register[AnimalChild, target_AnimalChild]()
            di_container.register[Animal]()
            di_container.freeze()

            animal = di_container.resolve[Animal]()

            self.assertEqual(
                animal.quack(),
                'Animal.quack'
            )
            self.assertEqual(
                animal.spawn_child().quack(),
                'AnimalChildA.quack'
            )
            
        target_AnimalChild = AnimalChildB
        with self.subTest(target_AnimalChild = target_AnimalChild):
            di_container = dicon.DIContainer()
            di_container.register[AnimalChild, target_AnimalChild]()
            di_container.register[Animal]()
            di_container.freeze()

            animal = di_container.resolve[Animal]()

            self.assertEqual(
                animal.quack(),
                'Animal.quack'
            )
            self.assertEqual(
                animal.spawn_child().quack(),
                'AnimalChildB.quack'
            )

    def test_class_constructor_is_modified_and_type_is_not_modified(self):
        di_container = dicon.DIContainer()
        di_container.register[Animal]()
        di_container.freeze()

        self.assertNotEqual(
            di_container.resolve[Animal],
            Animal
        )
        self.assertIs(
            type(di_container.resolve[Animal]()),
            Animal
        )
        self.assertIs(
            di_container.resolve[Animal]().__class__,
            Animal
        )

    def test_exception_DIContainerMissingError(self):
        with self.assertRaises(dicon.DIContainerMissingError):
            Animal()

    def test_exception_ClassResolutionNotRegisteredError(self):
        target_AnimalChild = AnimalChildA
        with self.assertRaises(dicon.ClassResolutionNotRegisteredError):
            di_container = dicon.DIContainer()
            # di_container.register[AnimalChild, target_AnimalChild]()
            di_container.register[Animal]()
            di_container.freeze()

            animal = di_container.resolve[Animal]()
            animal.spawn_child()

    def test_exception_assert_register_arguments_are_classes(self):
        with self.assertRaises(AssertionError):
            di_container = dicon.DIContainer()
            di_container.register[0]()
        with self.assertRaises(AssertionError):
            di_container = dicon.DIContainer()
            di_container.register[Animal, 0]()
        with self.assertRaises(AssertionError):
            di_container = dicon.DIContainer()
            di_container.register[0, Animal]()

    def test_exception_assert_concrete_must_be_subclass_of_interface(self):
        with self.assertRaises(AssertionError):
            di_container = dicon.DIContainer()
            di_container.register[str, Animal]()
