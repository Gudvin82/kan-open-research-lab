import json
import logging
import re
from datetime import UTC, datetime

_SECRET_PATTERN = re.compile(
    r"(?i)(password|secret|token|authorization|database_url)"
    r"([\"'=:\s]+)([^\s,;\"']+)"
)
_DSN_PATTERN = re.compile(r"(?i)postgres(?:ql)?://[^@\s]+@")


def redact(value: str) -> str:
    value = _SECRET_PATTERN.sub(r"\1\2[REDACTED]", value)
    return _DSN_PATTERN.sub("postgresql://[REDACTED]@", value)


class SafeJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": redact(record.getMessage()),
        }
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
