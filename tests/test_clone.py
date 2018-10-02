import unittest

import dicon


@dicon.inject_di_container('_di_container')
class A:
    pass

@dicon.inject_di_container('_di_container')
class B:
    def __init__(self):
        assert self._di_container.resolve[A]


class TestClone(unittest.TestCase):
    def test_clone(self):
        x = dicon.DIContainer()
        x.register[A]()
        x.register_singleton('b', 'bar')

        y = x.clone()

        x.freeze()

        self.assertEqual(
            y.resolve[A],
            x.resolve[A]
        )
        self.assertEqual(
            y.singleton['b'],
            x.singleton['b']
        )
        self.assertEqual(
            y._freezed,
            False
        )
        self.assertEqual(
            x._freezed,
            True
        )

        y.freeze()

        self.assertEqual(
            y.resolve[A],
            x.resolve[A]
        )
        self.assertEqual(
            y.singleton['b'],
            x.singleton['b']
        )
        self.assertEqual(
            y._freezed,
            True
        )

    def test_do_not_bind_di_container_before_clone(self):
        x = dicon.DIContainer()
        x.register[B]()

        y = x.clone()
        y.register[A]()
        assert y.resolve[B]()
        y.freeze()
        assert y.resolve[B]()

        z = x.clone()
        x.freeze()
        z.register[A]()
        assert z.resolve[B]()
        z.freeze()
        assert z.resolve[B]()
