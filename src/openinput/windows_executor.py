
import ctypes
import sys
from ctypes import wintypes

from .actions import ActionType


# Windows input constants
INPUT_KEYBOARD = 1
INPUT_MOUSE = 0

KEYEVENTF_KEYUP = 0x0002
MOUSEEVENTF_WHEEL = 0x0800

WHEEL_DELTA = 120

VK_CONTROL = 0x11
VK_A = 0x41
VK_C = 0x43
VK_V = 0x56
VK_Z = 0x5A
VK_TAB = 0x09


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_size_t),
    ]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_size_t),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]


class INPUTUNION(ctypes.Union):
    _fields_ = [
        ("ki", KEYBDINPUT),
        ("mi", MOUSEINPUT),
        ("hi", HARDWAREINPUT),
    ]


class INPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [
        ("type", wintypes.DWORD),
        ("u", INPUTUNION),
    ]


class WindowsExecutor:

    SHORTCUTS = {
        ActionType.COPY: [VK_CONTROL, VK_C],
        ActionType.PASTE: [VK_CONTROL, VK_V],
        ActionType.UNDO: [VK_CONTROL, VK_Z],
        ActionType.SELECT_ALL: [VK_CONTROL, VK_A],
        ActionType.NEXT_TAB: [VK_CONTROL, VK_TAB],
    }

    def __init__(self):
        if sys.platform != "win32":
            raise RuntimeError(
                "WindowsExecutor requires Windows"
            )

        self.user32 = ctypes.WinDLL(
            "user32", use_last_error=True
        )

        self.user32.SendInput.argtypes = [
            wintypes.UINT,
            ctypes.POINTER(INPUT),
            ctypes.c_int,
        ]
        self.user32.SendInput.restype = wintypes.UINT

    def execute(self, action: ActionType):
        if action in self.SHORTCUTS:
            self._send_shortcut(self.SHORTCUTS[action])

        elif action == ActionType.SCROLL_UP:
            self._scroll(WHEEL_DELTA)

        elif action == ActionType.SCROLL_DOWN:
            self._scroll(-WHEEL_DELTA)

        else:
            raise ValueError(
                f"Unsupported action: {action}"
            )

        return action.value

    def _send(self, events):
        batch = (INPUT * len(events))(*events)

        sent = self.user32.SendInput(
            len(batch),
            batch,
            ctypes.sizeof(INPUT),
        )

        if sent != len(batch):
            raise RuntimeError(
                f"SendInput sent {sent}/{len(batch)} events; "
                f"Windows error: {ctypes.get_last_error()}"
            )

    def _keyboard_event(self, key, key_up=False):
        return INPUT(
            type=INPUT_KEYBOARD,
            ki=KEYBDINPUT(
                wVk=key,
                wScan=0,
                dwFlags=KEYEVENTF_KEYUP if key_up else 0,
                time=0,
                dwExtraInfo=0,
            ),
        )

    def _send_shortcut(self, keys):
        events = []

        # Press keys in order
        for key in keys:
            events.append(
                self._keyboard_event(key)
            )

        # Release keys in reverse order
        for key in reversed(keys):
            events.append(
                self._keyboard_event(key, key_up=True)
            )

        self._send(events)

    def _scroll(self, amount):
        event = INPUT(
            type=INPUT_MOUSE,
            mi=MOUSEINPUT(
                dx=0,
                dy=0,
                mouseData=amount & 0xFFFFFFFF,
                dwFlags=MOUSEEVENTF_WHEEL,
                time=0,
                dwExtraInfo=0,
            ),
        )

        self._send([event])
