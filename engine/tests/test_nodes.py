"""tests for nodes.py"""
from unittest import TestCase

from tools import UnitTests

from ..nodes import Node


class NodeTests(UnitTests):
    """Test Node"""


@NodeTests.describe("node has a name")
def _(test: TestCase) -> None:
    node = Node("my node")

    test.assertEqual("my node", node.name)

    node = Node("other node")

    test.assertEqual("other node", node.name)


@NodeTests.describe("add children to node")
def _(test: TestCase) -> None:
    node = Node("node")
    fst_child = Node("1st child")
    snd_child = Node("2nd child")
    node.add_child(fst_child)
    node.add_child(snd_child)

    test.assertIn(fst_child, node.children)
    test.assertIn(snd_child, node.children)


@NodeTests.describe("serialize name")
def _(test: TestCase) -> None:
    node = Node("foo")

    test.assertEqual("foo", node.serialize())

    node = Node("bar")

    test.assertEqual("bar", node.serialize())


@NodeTests.describe("serialize name and child name")
def _(test: TestCase) -> None:
    node = Node("foo")
    node.add_child(Node("bar"))

    test.assertEqual("foo,bar", node.serialize())


@NodeTests.describe("serialize name and children names")
def _(test: TestCase) -> None:
    node = Node("node")
    fst_child = Node("1st child")
    snd_child = Node("2nd child")
    node.add_child(fst_child)
    node.add_child(snd_child)

    test.assertEqual("node,1st child,-,2nd child", node.serialize())
