
import unittest

from openinput.actions import ActionType
from openinput.dispatcher import (
    ActionDispatcher,
    DryRunExecutor,
)


class TestActionDispatcher(unittest.TestCase):

    def setUp(self):
        self.dispatcher = ActionDispatcher(
            DryRunExecutor()
        )

    def test_copy(self):
        result = self.dispatcher.dispatch(
            ActionType.COPY
        )
        self.assertEqual(result, "copy")

    def test_scroll_down(self):
        result = self.dispatcher.dispatch(
            ActionType.SCROLL_DOWN
        )
        self.assertEqual(result, "scroll_down")

    def test_invalid_action(self):
        with self.assertRaises(ValueError):
            self.dispatcher.dispatch("delete_everything")


if __name__ == "__main__":
    unittest.main()
