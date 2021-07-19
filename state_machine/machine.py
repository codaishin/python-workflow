"""Core statemachine module"""
from typing import (
    Callable,
    Dict,
    Generic,
    Iterable,
    Mapping,
    Optional,
    TypeVar,
)

from .interfaces import BaseState

TVal = TypeVar("TVal")


class Node(Generic[TVal]):
    """State machine node"""

    def __init__(self, name: str, func: Callable[[], TVal]) -> None:
        self._name = name
        self._func = func
        self._next_nodes: Dict[str, "Node[TVal]"] = {}

    @property
    def next_nodes(self) -> Mapping[str, "Node[TVal]"]:
        """Next nodes"""
        return self._next_nodes

    @property
    def name(self) -> str:
        """Node name"""
        return self._name

    def func(self) -> TVal:
        """Node function"""
        return self._func()

    def next(self, **funcs: Callable[[TVal], TVal]) -> Iterable["Node[TVal]"]:
        """Connect next nodes"""

        def generate() -> Iterable[Node[TVal]]:
            for name, func in funcs.items():
                yield self._next(name, func)

        return tuple(generate())

    def _next(self, name: str, func: Callable[[TVal], TVal]) -> "Node[TVal]":
        node = Node(name, self._apply(func))
        self._next_nodes[name] = node
        return node

    def _apply(self, wrapper: Callable[[TVal], TVal]) -> Callable[[], TVal]:
        def apply_func() -> TVal:
            return wrapper(self.func())

        return apply_func


class State(BaseState[TVal]):
    """State machine state"""

    def __init__(self, value: TVal, nodes: Mapping[str, Node[TVal]]) -> None:
        self._value = value
        self._nodes = nodes

    @property
    def value(self) -> TVal:
        return self._value

    def transition(self, name: str) -> "BaseState[TVal]":
        node = self._nodes[name]
        self._value = node.func()
        return State(self._value, node.next_nodes)


class StartState(BaseState[TVal]):
    """Start state"""

    def __init__(self, start_nodes: Mapping[str, Node[TVal]]) -> None:
        self._value: Optional[TVal] = None
        self._start_nodes = start_nodes

    @property
    def value(self) -> TVal:
        assert self._value
        return self._value

    def transition(self, name: str) -> "BaseState[TVal]":
        node = self._start_nodes[name]
        self._value = node.func()
        return State(self._value, node.next_nodes)


class StateMachine(Generic[TVal]):
    """State machine"""

    def __init__(self) -> None:
        self._next_nodes: Dict[str, Node[TVal]] = {}

    def start(self, **funcs: Callable[[], TVal]) -> Iterable[Node[TVal]]:
        """Connect start nodes"""

        def generate() -> Iterable[Node[TVal]]:
            for name, func in funcs.items():
                yield self._next(name, func)

        return tuple(generate())

    def _next(self, name: str, func: Callable[[], TVal]) -> "Node[TVal]":
        node = Node(name, func)
        self._next_nodes[name] = node
        return node

    def run(self) -> BaseState[TVal]:
        """Run machine with concrete states"""

        return StartState(self._next_nodes)
