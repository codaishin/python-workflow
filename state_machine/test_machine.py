"""state machine tests"""

from unittest import TestCase

from .machine import StateMachine


class TestState(TestCase):
    """Test state machine"""

    def test_initial(self) -> None:
        """Generates initial state"""

        machine = StateMachine[int]()
        machine.start(start=lambda: 42)

        state = machine.run()
        state = state.transition("start")

        self.assertEqual(42, state.value)

    def test_multiple_initials(self) -> None:
        """Generates initial states"""

        machine = StateMachine[int]()
        machine.start(start_a=lambda: 42, start_b=lambda: 11)

        state = machine.run()
        state = state.transition("start_b")

        self.assertEqual(11, state.value)

    def test_always_transition_to_new_state(self) -> None:
        """Transition returns new state"""

        machine = StateMachine[int]()
        machine.start(start=lambda: 42)

        state_a = machine.run()
        state_b = state_a.transition("start")

        self.assertNotEqual(id(state_a), id(state_b))

    def test_linear_flow(self) -> None:
        """Linear flow with"""

        machine = StateMachine[int]()
        (start, *_) = machine.start(start=lambda: 3)
        (double, *_) = start.next(double=lambda v: v * 2)
        double.next(tripple=lambda v: v * 3)

        state = machine.run()
        state = state.transition("start")
        state = state.transition("double")
        state = state.transition("tripple")

        self.assertEqual(18, state.value)
