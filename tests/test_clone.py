import unittest

import dicon


@dicon.inject_di_container('_di_container')
class A:
    pass


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
