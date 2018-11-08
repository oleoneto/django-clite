import unittest
import doctest


def square(x):
    """Return the square of xself.
    >>> square(2)
    4
    >>> square(-2)
    4
    """
    return x*x


def test_answer():
    assert square(4) == 16

