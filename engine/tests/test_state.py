"""state tests"""

from unittest import TestCase

from ..state import State


class TestState(TestCase):
    """test State"""

    @staticmethod
    def test_init_empty() -> None:
        """init empty State"""

        _ = State()

    def test_unpack_empty(self) -> None:
        """empty State unpacks to empty Tuple"""

        state = State()
        self.assertEqual("", state.serialize_str())

    def test_unpack_single(self) -> None:
        """single elem unpack to one elem Tuple"""

        state = State("start")
        self.assertEqual("start", state.serialize_str())
