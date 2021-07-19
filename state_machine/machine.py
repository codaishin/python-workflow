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

    def resolve(self) -> TStateValue:
        """Resolve node value"""
        return self._func()

    def next(
        self,
        **nexts: Callable[[TStateValue], TStateValue],
    ) -> Tuple["Node[TStateValue]", ...]:
        """Connect next nodes

        Kwargs:
            (TStateValue) -> TStateValue: Declared node names and
                transition logic

        Returns:
            (Node[TStateValue], ...): Newly declared nodes
        """
        return_nodes: Tuple[Node, ...] = ()

        def apply(transition) -> Callable[[], TStateValue]:
            def apply_transition() -> TStateValue:
                return transition(self._func())

            return apply_transition

        for name, transition in nexts.items():
            start_node = Node(name, apply(transition))
            self._next_nodes[name] = start_node
            return_nodes += (start_node,)
        return return_nodes


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
        self._value = node.resolve()
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
        self._value = node.resolve()
        return State(self._value, node.next_nodes)


class StateMachine(Generic[TStateValue]):
    """State machine"""

    def __init__(self) -> None:
        self._start_nodes: Dict[str, Node[TStateValue]] = {}

    def start(
        self,
        **start_transitions: Callable[[], TStateValue],
    ) -> Tuple[Node[TStateValue], ...]:
        """Connect start nodes

        Kwargs:
            () -> TStateValue: Declared node names and transition logic

        Returns:
            (Node[TStateValue], ...): Newly declared nodes
        """
        return_nodes: Tuple[Node, ...] = ()
        for name, transition in start_transitions.items():
            start_node = Node(name, transition)
            self._start_nodes[name] = start_node
            return_nodes += (start_node,)
        return return_nodes

    def run(self) -> BaseState[TStateValue]:
        """Run machine with concrete states"""

        return StartState(self._start_nodes)
