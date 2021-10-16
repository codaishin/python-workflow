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

    def test_add_children(self) -> None:
        """add children to node"""

        fst = Node("1st")
        snd = Node("2nd")
        trd = Node("3rd")

        fst.add_child(snd)
        fst.add_child(trd)

        self.assertIn(snd, fst.children)
        self.assertIn(trd, fst.children)

    def test_serialize_name(self) -> None:
        """serialize name"""

        node = Node("foo")
        self.assertEqual("foo", node.serialize())

        node = Node("bar")
        self.assertEqual("bar", node.serialize())

    def test_serialize_name_and_child_name(self) -> None:
        """serialize name and child name"""

        node = Node("foo")
        node.add_child(Node("bar"))
        self.assertEqual("foo,bar", node.serialize())

    def test_serialize_name_and_children_names(self) -> None:
        """serialize name and children names"""
        node = Node("node")
        child_a = Node("childA")
        child_b = Node("childB")
        node.add_child(child_a)
        node.add_child(child_b)

        self.assertEqual("node,childA,-,childB", node.serialize())
