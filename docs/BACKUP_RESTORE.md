# Backup and Restore

Foundation implements a local logical backup drill only. It does not schedule
production backups or provision storage.

```bash
./scripts/backup_db.sh ./tmp/foundation.dump
RESTORE_DATABASE_NAME=kan_restore_test \
  ./scripts/restore_db.sh ./tmp/foundation.dump
```

The backup is PostgreSQL custom format with a SHA-256 sidecar. The script will
not overwrite an existing dump. Restore verifies the checksum and refuses any
database whose name lacks `test` or `local`; it then recreates the guarded
target and runs `SELECT 1`.

Production policy will require provider-native PITR plus an independent,
encrypted off-provider logical copy and a scheduled restore drill. Provider,
retention, encryption keys and schedule require separate approval.
