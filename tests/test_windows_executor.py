
import unittest
from unittest.mock import Mock

from openinput.actions import ActionType
from openinput.windows_executor import (
    WindowsExecutor,
    KEYEVENTF_KEYUP,
    MOUSEEVENTF_WHEEL,
    VK_CONTROL,
    VK_C,
)


class TestWindowsExecutor(unittest.TestCase):

    def setUp(self):
        self.executor = WindowsExecutor()

        # Replace real SendInput with a fake
        self.executor._send = Mock()

    def test_copy_shortcut(self):
        self.executor.execute(ActionType.COPY)

        self.executor._send.assert_called_once()

        events = self.executor._send.call_args.args[0]

        self.assertEqual(len(events), 4)

        # Ctrl down
        self.assertEqual(events[0].ki.wVk, VK_CONTROL)
        self.assertEqual(events[0].ki.dwFlags, 0)

        # C down
        self.assertEqual(events[1].ki.wVk, VK_C)
        self.assertEqual(events[1].ki.dwFlags, 0)

        # C up
        self.assertEqual(events[2].ki.wVk, VK_C)
        self.assertEqual(
            events[2].ki.dwFlags,
            KEYEVENTF_KEYUP,
        )

        # Ctrl up
        self.assertEqual(events[3].ki.wVk, VK_CONTROL)
        self.assertEqual(
            events[3].ki.dwFlags,
            KEYEVENTF_KEYUP,
        )

    def test_scroll_down(self):
        self.executor.execute(ActionType.SCROLL_DOWN)

        self.executor._send.assert_called_once()

        events = self.executor._send.call_args.args[0]

        self.assertEqual(len(events), 1)
        self.assertEqual(
            events[0].mi.dwFlags,
            MOUSEEVENTF_WHEEL,
        )

        # Signed -120 represented as unsigned 32-bit
        self.assertEqual(
            events[0].mi.mouseData,
            (-120) & 0xFFFFFFFF,
        )

    def test_unsupported_action(self):
        with self.assertRaises(ValueError):
            self.executor.execute("unknown")


if __name__ == "__main__":
    unittest.main()
