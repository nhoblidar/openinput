
from enum import Enum


class ActionType(str, Enum):
    COPY = "copy"
    PASTE = "paste"
    UNDO = "undo"
    SELECT_ALL = "select_all"
    NEXT_TAB = "next_tab"
    SCROLL_UP = "scroll_up"
    SCROLL_DOWN = "scroll_down"
