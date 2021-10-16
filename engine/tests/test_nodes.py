"""tests for nodes.py"""

from unittest import TestCase

from ..nodes import Node


class TestNode(TestCase):
    """Test Node"""

    def test_name(self) -> None:
        """has set name"""

        node = Node("my node")

        self.assertEqual("my node", node.name)

        node = Node("other node")

        self.assertEqual("other node", node.name)

    def test_children(self) -> None:
        """add children to node"""

        fst = Node("1st")
        snd = Node("2nd")
        trd = Node("3rd")

        fst.add_child(snd)
        fst.add_child(trd)

        self.assertIn(snd, fst.children)
        self.assertIn(trd, fst.children)
