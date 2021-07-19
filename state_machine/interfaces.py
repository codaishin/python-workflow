"""Interfaces"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TStateValue = TypeVar("TStateValue")


class BaseState(Generic[TStateValue], ABC):
    """Base state interface"""

    @property
    @abstractmethod
    def value(self) -> TStateValue:
        """State value"""

    @abstractmethod
    def transition(self, name: str) -> "BaseState[TStateValue]":
        """Run concrete transition"""
