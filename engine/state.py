"""state"""

from typing import Optional


class State:
    """State of a workflow"""

    def __init__(self, state: Optional[str] = None) -> None:
        self._state = state

    def serialize_str(self) -> str:
        """serializes to string"""

        if self._state:
            return self._state
        return ""
