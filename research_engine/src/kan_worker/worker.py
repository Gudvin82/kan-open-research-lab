import json
import signal
import time
from datetime import UTC, datetime

_running = True


def stop(_signum: int, _frame: object) -> None:
    global _running
    _running = False


def emit(event: str) -> None:
    print(
        json.dumps(
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "level": "INFO",
                "component": "research_worker",
                "event": event,
            },
            separators=(",", ":"),
        ),
        flush=True,
    )


def main() -> None:
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    emit("skeleton_started")
    while _running:
        time.sleep(5)
    emit("skeleton_stopped")


if __name__ == "__main__":
    main()
