"""state tests"""

from unittest import TestCase

from ..state import State


class TestState(TestCase):
    """test State"""

    def test_unpack_start(self) -> None:
        """as "start" """

        state = State("start")
        self.assertEqual("start", state.serialize_str())

    def test_unpack_start_then_end(self) -> None:
        """as "start,end" """

        state = State("start").chain_root(State("end"))
        self.assertEqual("start,end", state.serialize_str())

    def test_unpack_start_then_two_ends(self) -> None:
        """as "start,end_a,-,end_b" """

        state = (
            State("start")
            .chain_root(State("end_a"))
            .chain_root(State("end_b"))
        )
        self.assertEqual("start,end_a,-,end_b", state.serialize_str())

    def test_unpack_start_then_two_longer_chains(self) -> None:
        """as "start,start_a,end_a,--,start_b,end_b" """

        start = State("start")
        chain_a = State("start_a").chain_root(State("end_a"))
        chain_b = State("start_b").chain_root(State("end_b"))
        start = start.chain_root(chain_a).chain_root(chain_b)
        self.assertEqual(
            "start,start_a,end_a,--,start_b,end_b",
            start.serialize_str(),
        )

    def test_unpack_start_then_two_even_longer_chains(self) -> None:
        """as "start,start_a,middle_a,end_a,---,start_b,middle_b,end_b" """

        start = State("start")
        chain_a = State("start_a").chain_root(
            State("middle_a").chain_root(State("end_a"))
        )
        chain_b = State("start_b").chain_root(
            State("middle_b").chain_root(State("end_b"))
        )
        start = start.chain_root(chain_a).chain_root(chain_b)
        self.assertEqual(
            "start,start_amiddle_a,end_a,---,start_b,middle_b,end_b",
            start.serialize_str(),
        )
