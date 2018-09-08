import unittest

import yadi


class TestAuxiliaryFunctions(unittest.TestCase):
    def test_get_non_conflict_param_name(self):
        def f(a_0, b_0, b_1=None, c_0=None):
            pass

        with self.subTest():
            self.assertEqual(
                yadi.yadi._get_non_conflict_param_name(f, 'a_{}'),
                'a_1'
            )
        with self.subTest():
            self.assertEqual(
                yadi.yadi._get_non_conflict_param_name(f, 'b_{}'),
                'b_2'
            )
        with self.subTest():
            self.assertEqual(
                yadi.yadi._get_non_conflict_param_name(f, 'c_{}'),
                'c_1'
            )
        with self.subTest():
            self.assertEqual(
                yadi.yadi._get_non_conflict_param_name(f, 'd_{}'),
                'd_0'
            )
