"""core tests"""

from unittest import TestCase

from ..exceptions import TaskError
from ..task import Task


class TestTask(TestCase):
    """test Task"""

    @staticmethod
    def test_init_empty() -> None:
        """init empty"""

        _ = Task("flow")

    def test_one_task(self) -> None:
        """run one task"""

        flow = Task("flow")
        _ = Task("end", flow)

        state = flow.run("end")

        self.assertEqual(("end",), state)

    def test_two_tasks_chain(self) -> None:
        """run two serial tasks"""

        flow = Task("flow")
        start = Task("start", flow)
        _ = Task("end", start)

        state = flow.run("start")
        state = flow.run("end", state)

        self.assertEqual(("start", "end"), state)

    def test_three_tasks_chain(self) -> None:
        """run two serial tasks"""

        flow = Task("flow")
        start = Task("start", flow)
        middle = Task("middle", start)
        _ = Task("end", middle)

        state = flow.run("start")
        state = flow.run("middle", state)
        state = flow.run("end", state)

        self.assertEqual(("start", "middle", "end"), state)

    def test_error_when_run_non_existing(self) -> None:
        """raise TaskError when running non existing task"""

        flow = Task("flow")
        _ = Task("start", flow)

        with self.assertRaises(TaskError):
            _ = flow.run("begin")
