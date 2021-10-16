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
