import unittest

import dicon


@dicon.inject_di_container('_di_container')
class A:
    pass


class TestClone(unittest.TestCase):
    def test_clone(self):
        di_container = dicon.DIContainer()
        di_container.register[A]()
        di_container.register_singleton('b', 'bar')

        x = di_container.clone()

        di_container.freeze()

        self.assertEqual(
            x.resolve[A],
            di_container.resolve[A]
        )
        self.assertEqual(
            x.singleton['b'],
            di_container.singleton['b']
        )
        self.assertEqual(
            x._freezed,
            False
        )
        self.assertEqual(
            di_container._freezed,
            True
        )
