
from .actions import ActionType


class ActionDispatcher:
    def __init__(self, executor):
        self.executor = executor

    def dispatch(self, action: ActionType):
        if not isinstance(action, ActionType):
            raise ValueError(
                f"Unsupported action: {action}"
            )

        return self.executor.execute(action)


class DryRunExecutor:
    def execute(self, action: ActionType):
        print(f"[DRY RUN] Executing: {action.value}")
        return action.value
