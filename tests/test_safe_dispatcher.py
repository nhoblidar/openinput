
import unittest
from unittest.mock import Mock

from openinput.actions import ActionType
from openinput.safe_dispatcher import (
    SafeActionDispatcher,
)
from openinput.window_context import WindowContext


class TestSafeActionDispatcher(unittest.TestCase):

    def setUp(self):
        self.executor = Mock()
        self.window_manager = Mock()

        self.dispatcher = SafeActionDispatcher(
            self.executor,
            self.window_manager,
        )

        self.context = WindowContext(
            hwnd=12345,
            title="Notepad",
        )

    def test_action_sent_when_focus_matches(self):
        self.window_manager.is_still_focused.return_value = True

        result = self.dispatcher.dispatch(
            ActionType.COPY,
            self.context,
        )

        self.assertEqual(result.status, "sent")
        self.executor.execute.assert_called_once_with(
            ActionType.COPY
        )

    def test_action_cancelled_when_focus_changes(self):
        self.window_manager.is_still_focused.return_value = False

        result = self.dispatcher.dispatch(
            ActionType.COPY,
            self.context,
        )

        self.assertEqual(result.status, "cancelled")
        self.executor.execute.assert_not_called()

    def test_execution_failure(self):
        self.window_manager.is_still_focused.return_value = True
        self.executor.execute.side_effect = RuntimeError(
            "Windows rejected input"
        )

        result = self.dispatcher.dispatch(
            ActionType.COPY,
            self.context,
        )

        self.assertEqual(result.status, "failed")

    def test_latency_recorded(self):
        self.window_manager.is_still_focused.return_value = True

        result = self.dispatcher.dispatch(
            ActionType.COPY,
            self.context,
        )

        self.assertGreaterEqual(
            result.latency_ms, 0
        )


if __name__ == "__main__":
    unittest.main()
