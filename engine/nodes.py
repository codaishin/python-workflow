"""Process nodes"""


class Node:
    """Node, referencing child nodes"""

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        """Node name"""
        return self._name
