"""core"""

from typing import Dict, Optional, Tuple

from .exceptions import TaskError

State = Tuple[str, ...]


class Task:
    """Flow Task"""

    def __init__(self, name: str, previous: Optional["Task"] = None) -> None:
        self._next: Dict[str, Task] = {}
        if previous:
            previous.next(name, self)

    def run(self, name: str, state: State = ()) -> State:
        """Run task"""

        if name in self._next:
            return state + (name,)

        if not state:
            raise TaskError()

        return self._run_next(name, state)

    def _run_next(self, name: str, state: State) -> State:
        (state_first, *state_rest) = state
        if next_task := self._next.get(state_first, None):
            return (state_first,) + next_task.run(name, tuple(state_rest))

        raise TaskError()

    def next(self, name: str, task: "Task") -> None:
        """Add a follower Task"""

        self._next[name] = task
