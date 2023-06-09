from __future__ import print_function, absolute_import

import itertools

import numpy

import numba.unittest_support as unittest
from numba.compiler import compile_isolated, Flags
from numba import types, typeof, njit
from numba import lowering
from .support import TestCase


def return_double_or_none(x):
    if x:
        ret = None
    else:
        ret = 1.2
    return ret


def return_different_statement(x):
    if x:
        return None
    else:
        return 1.2


def return_bool_optional_or_none(x, y):
    if y:
        z = False
    else:
        z = None
    if x == 2:
        # A boolean
        return True
    elif x == 1:
        # A runtime optional
        return z
    else:
        # None
        return None


def is_this_a_none(x):
    if x:
        val_or_none = None
    else:
        val_or_none = x

    if val_or_none is None:
        return x - 1

    if val_or_none is not None:
        return x + 1


def a_is_b(a, b):
    """
    Note in nopython mode, this operation does not make much sense.
    Because we don't have objects anymore.
    `a is b` is always False if not operating on None and Optional type
    """
    return a is b


def a_is_not_b(a, b):
    """
    This is `not (a is b)`
    """
    return a is not b


class TestOptional(TestCase):

    def test_return_double_or_none(self):
        pyfunc = return_double_or_none
        cres = compile_isolated(pyfunc, [types.boolean])
        cfunc = cres.entry_point

        for v in [True, False]:
            self.assertPreciseEqual(pyfunc(v), cfunc(v))

    def test_return_different_statement(self):
        pyfunc = return_different_statement
        cres = compile_isolated(pyfunc, [types.boolean])
        cfunc = cres.entry_point

        for v in [True, False]:
            self.assertPreciseEqual(pyfunc(v), cfunc(v))

    def test_return_bool_optional_or_none(self):
        pyfunc = return_bool_optional_or_none
        cres = compile_isolated(pyfunc, [types.int32, types.int32])
        cfunc = cres.entry_point

        for x, y in itertools.product((0, 1, 2), (0, 1)):
            self.assertPreciseEqual(pyfunc(x, y), cfunc(x, y))

    def test_is_this_a_none(self):
        pyfunc = is_this_a_none
        cres = compile_isolated(pyfunc, [types.intp])
        cfunc = cres.entry_point

        for v in [-1, 0, 1, 2]:
            self.assertPreciseEqual(pyfunc(v), cfunc(v))

    def test_is_this_a_none_objmode(self):
        pyfunc = is_this_a_none
        flags = Flags()
        flags.set('force_pyobject')
        cres = compile_isolated(pyfunc, [types.intp], flags=flags)
        cfunc = cres.entry_point
        self.assertTrue(cres.objectmode)
        for v in [-1, 0, 1, 2]:
            self.assertPreciseEqual(pyfunc(v), cfunc(v))

    def test_a_is_b_intp(self):
        pyfunc = a_is_b
        with self.assertRaises(lowering.LoweringError):
            cres = compile_isolated(pyfunc, [types.intp, types.intp])

    def test_a_is_not_b_intp(self):
        pyfunc = a_is_not_b
        with self.assertRaises(lowering.LoweringError):
            cres = compile_isolated(pyfunc, [types.intp, types.intp])

    def test_optional_float(self):
        def pyfunc(x, y):
            if y is None:
                return x
            else:
                return x + y

        cfunc = njit("(float64, optional(float64))")(pyfunc)
        self.assertAlmostEqual(pyfunc(1., 12.3), cfunc(1., 12.3))
        self.assertAlmostEqual(pyfunc(1., None), cfunc(1., None))

    def test_optional_array(self):
        def pyfunc(x, y):
            if y is None:
                return x
            else:
                y[0] += x
                return y[0]

        cfunc = njit("(float32, optional(float32[:]))")(pyfunc)
        cy = numpy.array([12.3], dtype=numpy.float32)
        py = cy.copy()
        self.assertAlmostEqual(pyfunc(1., py), cfunc(1., cy))
        numpy.testing.assert_almost_equal(py, cy)
        self.assertAlmostEqual(pyfunc(1., None), cfunc(1., None))

    def test_optional_array_error(self):
        def pyfunc(y):
            return y[0]

        cfunc = njit("(optional(int32[:]),)")(pyfunc)
        with self.assertRaises(TypeError) as raised:
            cfunc(None)
        self.assertIn('expected array(int32, 1d, A), got None',
                      str(raised.exception))

        y = numpy.array([0xabcd], dtype=numpy.int32)
        self.assertEqual(cfunc(y), pyfunc(y))

    def test_optional_array_attribute(self):
        """
        Check that we can access attribute of an optional
        """
        def pyfunc(arr, do_it):
            opt = None
            if do_it:  # forces `opt` to be an optional of arr
                opt = arr
            return opt.shape[0]

        cfunc = njit(pyfunc)
        arr = numpy.arange(5)
        self.assertEqual(pyfunc(arr, True), cfunc(arr, True))

    def test_assign_to_optional(self):
        """
        Check that we can assign to a variable of optional type
        """
        @njit
        def make_optional(val, get_none):
            if get_none:
                ret = None
            else:
                ret = val
            return ret

        @njit
        def foo(val, run_second):
            a = make_optional(val, True)
            if run_second:
                a = make_optional(val, False)
            return a

        self.assertIsNone(foo(123, False))
        self.assertEqual(foo(231, True), 231)


if __name__ == '__main__':
    unittest.main()
