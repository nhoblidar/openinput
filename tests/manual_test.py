
import time

from openinput.actions import ActionType
from openinput.dispatcher import ActionDispatcher
from openinput.windows_executor import WindowsExecutor


dispatcher = ActionDispatcher(WindowsExecutor())

print("Switch to Notepad within 5 seconds...")
time.sleep(5)

dispatcher.dispatch(ActionType.SELECT_ALL)

print("Select All executed!")
