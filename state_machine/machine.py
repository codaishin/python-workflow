"""Core statemachine module"""
from typing import Callable, Dict, Generic, Mapping, Optional, Tuple, TypeVar

from .interfaces import BaseState

TStateValue = TypeVar("TStateValue")


class Node(Generic[TStateValue]):
    """State machine node"""

    def __init__(
        self,
        name: str,
        func: Callable[[], TStateValue],
    ) -> None:
        self._name = name
        self._func = func
        self._next_nodes: Dict[str, "Node[TStateValue]"] = {}

    @property
    def next_nodes(self) -> Mapping[str, "Node[TStateValue]"]:
        """Next nodes"""
        return self._next_nodes

    @property
    def name(self) -> str:
        """Node name"""
        return self._name

    def func(self) -> TStateValue:
        """Node function"""
        return self._func()

    def next(
        self,
        **transitions: Callable[[TStateValue], TStateValue],
    ) -> Tuple["Node[TStateValue]", ...]:
        """Connect next nodes"""

        return_nodes: Tuple[Node, ...] = ()
        for name, transition in transitions.items():
            node = Node(name, self._apply(transition))
            self._next_nodes[name] = node
            return_nodes += (node,)
        return return_nodes

    def _apply(
        self,
        transtion: Callable[[TStateValue], TStateValue],
    ) -> Callable[[], TStateValue]:
        def apply_transtion() -> TStateValue:
            return transtion(self.func())

        return apply_transtion


class State(BaseState[TStateValue]):
    """State machine state"""

    def __init__(
        self,
        value: TStateValue,
        nodes: Mapping[str, Node[TStateValue]],
    ):
        self._value = value
        self._nodes = nodes

    @property
    def value(self) -> TStateValue:
        return self._value

    def transition(self, name: str) -> "BaseState[TStateValue]":
        node = self._nodes[name]
        self._value = node.func()
        return State(self._value, node.next_nodes)


class StartState(BaseState[TStateValue]):
    """Start state"""

    def __init__(
        self,
        start_nodes: Mapping[str, Node[TStateValue]],
    ) -> None:
        self._value: Optional[TStateValue] = None
        self._start_nodes = start_nodes

    @property
    def value(self) -> TStateValue:
        assert self._value
        return self._value

    def transition(self, name: str) -> "BaseState[TStateValue]":
        node = self._start_nodes[name]
        self._value = node.func()
        return State(self._value, node.next_nodes)


class StateMachine(Generic[TStateValue]):
    """State machine"""

    def __init__(self) -> None:
        self._start_nodes: Dict[str, Node[TStateValue]] = {}

    def start(
        self,
        **transitions: Callable[[], TStateValue],
    ) -> Tuple[Node[TStateValue], ...]:
        """Connect start nodes"""

        return_nodes: Tuple[Node, ...] = ()
        for name, transition in transitions.items():
            start_node = Node(name, transition)
            self._start_nodes[name] = start_node
            return_nodes += (start_node,)
        return return_nodes

    def run(self) -> BaseState[TStateValue]:
        """Run machine with concrete states"""

        return StartState(self._start_nodes)
