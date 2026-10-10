
import time
from dataclasses import dataclass

from .dispatcher import ActionDispatcher


@dataclass(frozen=True)
class ActionResult:
    action: str
    status: str
    latency_ms: float
    message: str


class SafeActionDispatcher:

    def __init__(self, executor, window_manager):
        self.dispatcher = ActionDispatcher(executor)
        self.window_manager = window_manager

    def dispatch(self, action, target_context):
        start = time.perf_counter_ns()

        if not self.window_manager.is_still_focused(
            target_context
        ):
            elapsed_ms = (
                time.perf_counter_ns() - start
            ) / 1_000_000

            return ActionResult(
                action=action.value,
                status="cancelled",
                latency_ms=elapsed_ms,
                message="Foreground window changed",
            )

        try:
            self.dispatcher.dispatch(action)
            status = "sent"
            message = "Input submitted to Windows"

        except Exception as exc:
            status = "failed"
            message = str(exc)

        elapsed_ms = (
            time.perf_counter_ns() - start
        ) / 1_000_000

        return ActionResult(
            action=action.value,
            status=status,
            latency_ms=elapsed_ms,
            message=message,
        )
