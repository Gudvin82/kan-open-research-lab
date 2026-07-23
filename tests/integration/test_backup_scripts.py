import os
import subprocess
from pathlib import Path


def test_backup_requires_target():
    result = subprocess.run(  # noqa: S603
        ["/bin/bash", "scripts/backup_db.sh"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 64


def test_restore_rejects_unsafe_database_name(tmp_path: Path):
    dump = tmp_path / "safe.dump"
    dump.write_bytes(b"not-used")
    env = os.environ.copy()
    env["RESTORE_DATABASE_NAME"] = "production"
    result = subprocess.run(  # noqa: S603
        ["/bin/bash", "scripts/restore_db.sh", str(dump)],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 77
    assert "Refusing restore" in result.stderr
