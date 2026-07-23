import json
import logging

from src.core.logging import SafeJsonFormatter


def test_formatter_redacts_secrets_and_dsn():
    record = logging.LogRecord(
        "test",
        logging.INFO,
        __file__,
        1,
        "DATABASE_URL=postgresql://user:password@db/private token=abc",
        (),
        None,
    )
    payload = json.loads(SafeJsonFormatter().format(record))
    assert "password" not in payload["message"]
    assert "abc" not in payload["message"]
    assert "[REDACTED]" in payload["message"]
