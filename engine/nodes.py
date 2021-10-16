"""Process nodes"""
from typing import Iterable, List


class Node:
    """Node, referencing child nodes"""

    def __init__(self, name: str) -> None:
        self._name = name
        self._children: List["Node"] = []

    @property
    def name(self) -> str:
        """Node name"""
        return self._name

    @property
    def children(self) -> Iterable["Node"]:
        """Node children"""
        return self._children

    def add_child(self, child: "Node") -> None:
        """Add a child"""
        self._children.append(child)

    def serialize(self) -> str:
        """serialize node and its children as string"""
        if self._children:
            (child, *rest) = self._children
            suffix = "," + child.name
            for child in rest:
                suffix += ",-," + child.name
            return self.name + suffix
        return self.name
