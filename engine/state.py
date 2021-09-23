"""state"""
from typing import Iterable, Iterator, Tuple


class State:
    """Serialized state of a workflow process"""

    @property
    def root(self) -> str:
        """Root lable of this state"""
        return self._root

    @property
    def children(self) -> Iterable["State"]:
        """Children of the state root"""
        return self._children

    def __init__(self, root: str, children: Tuple["State", ...] = ()) -> None:
        self._root = root
        self._children = children

    def chain_root(self, elem: "State") -> "State":
        """Return new state with elem chained to root"""

        return State(self._root, self._children + (elem,))

    def serialize_str(self) -> str:
        """serializes to string"""

        def children(state) -> Iterator[State]:
            for child in state.children:
                yield child

        if self.children:
            gen = children(self)
            count_up = 0
            result = self.root
            while child := next(gen, None):
                result += (
                    ","
                    + ("-" * count_up)
                    + ("," if count_up else "")
                    + child.root
                )
                count_up = 1
                child_gen = children(child)
                while child_child := next(child_gen, None):
                    result += "," + child_child.root
                    count_up = 2
            return result

        return self._root
