"""Test runner"""
from functools import wraps
from typing import Callable
from unittest import TestCase

TestFunc = Callable[[TestCase], None]
TestDecorator = Callable[[TestFunc], TestFunc]


def _wrap_name_and_docstring(func: TestFunc, name: str, doc: str) -> TestFunc:
    wrapped = wraps(func)(func)
    wrapped.__doc__ = doc
    wrapped.__name__ = name
    return wrapped


class UnitTests(TestCase):
    """Test collection to run tests on

    It wraps unittests Testcase but provides a test classmethod.

    Use like:

    ```python

    class SumTests(UnitTests):
        \"\"\"sum() tests\"\"\"

    @SumTests.describe("1 + 1 == 2")
    def _(test: TestCase) -> None:
        test.assertEqual(2, sum(1, 1))
    ```
    """

    _count = 0

    @classmethod
    def describe(cls, docstring: str) -> TestDecorator:
        """add test with docstring"""

        def decorator(func: TestFunc) -> TestFunc:
            cls._count += 1
            name = f"test_{cls._count}"
            wrapped = _wrap_name_and_docstring(func, name, docstring)
            setattr(cls, name, wrapped)
            return func

        return decorator
