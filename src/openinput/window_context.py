
import ctypes
from ctypes import wintypes
from dataclasses import dataclass


@dataclass(frozen=True)
class WindowContext:
    hwnd: int
    title: str


class WindowsWindowManager:

    def __init__(self):
        self.user32 = ctypes.WinDLL(
            "user32", use_last_error=True
        )

        self.user32.GetForegroundWindow.restype = (
            wintypes.HWND
        )

        self.user32.GetWindowTextW.argtypes = [
            wintypes.HWND,
            wintypes.LPWSTR,
            ctypes.c_int,
        ]
        self.user32.GetWindowTextW.restype = (
            ctypes.c_int
        )

    def capture(self):
        hwnd = self.user32.GetForegroundWindow()

        if not hwnd:
            raise RuntimeError(
                "No foreground window found"
            )

        title = ctypes.create_unicode_buffer(256)

        self.user32.GetWindowTextW(
            hwnd, title, len(title)
        )

        return WindowContext(
            hwnd=hwnd,
            title=title.value,
        )

    def is_still_focused(self, context):
        current_hwnd = (
            self.user32.GetForegroundWindow()
        )

        return current_hwnd == context.hwnd
