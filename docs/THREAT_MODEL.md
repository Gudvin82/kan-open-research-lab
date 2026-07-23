# Модель угроз MVP

**Метод:** упрощённый STRIDE + abuse cases
**Граница:** публичный web, admin, PostgreSQL, worker, artifacts, CI/deploy

## Активы

- научный статус и неизменяемая история публикаций;
- admin account и MFA recovery;
- experiment definitions/configs/runs;
- исходные данные и лицензии;
- артефакты, checksums и environment manifests;
- secrets, backups и Git history;
- доступность сайта и ресурсы single-host сервера.

## Границы доверия

1. Интернет → reverse proxy/public web.
2. Admin browser → authenticated Django admin/control plane.
3. Web → PostgreSQL.
4. PostgreSQL queue → worker.
5. Worker → writable temp/artifact directories.
6. CI → registry/server deployment.
7. External datasets/repos → dependency and data intake.

## Ключевые угрозы и контрмеры

| Угроза | Риск | Обязательная мера |
|---|---|---|
| Публичный запуск кода/job | critical | deny by default; admin-only; CSRF; MFA; allowlist definition |
| Shell/Python payload через config | critical | typed schema; никаких command/source fields; fixed entrypoint |
| Компрометация worker → web secrets | critical | отдельные credentials/network/FS; no web secrets |
| Resource exhaustion | high | 1 job; cgroup CPU/RAM/PID/wall limits; disk watermark |
| Подмена научного статуса | high | state machine, audit event, role check, immutable revision |
| Подмена artifact/result | high | SHA-256, content-addressing, manifest, review before public |
| XSS через Markdown/формулы/SVG | high | safe renderer, sanitization allowlist, SVG/HTML disabled by default |
| Path traversal/upload polyglot | high | generated paths, MIME sniffing, size/type allowlist, no execute mount |
| CSRF/session theft/brute force | high | Django CSRF, secure cookies, CSP, rate limit, MFA, session rotation |
| SQL injection/IDOR | high | ORM/parameterization, object permissions, negative tests |
| Supply-chain compromise | high | pinned release/commit, hashes, license inventory, audit, regression suite |
| Secret leakage in logs/bundles | high | structured redaction, public serializer allowlist, secret scan |
| Backup theft or unusable backup | high | encryption/access control; restore drills; off-host copy |
| Stale RU/EN translation | medium | source revision link and automatic stale status |
| Misleading generated claim | high | human review; source locator; no autonomous publication |
| SSRF from source URL/RAG | medium now | no server-side arbitrary fetch in MVP; later egress allowlist |

## Worker security profile

- non-root UID, `no-new-privileges`, dropped capabilities;
- read-only root filesystem;
- explicit tmp/artifact mounts with quotas;
- outbound network disabled by default;
- fixed job dispatcher, signed/versioned adapter registry;
- database role limited to claim/heartbeat/result operations;
- heartbeat and hard timeout controlled outside experiment process;
- subprocess environment built from allowlist, not inherited wholesale;
- raw stdout/stderr sanitized before persistence.

## Security gates

### До merge Foundation

- dependency and secret scan;
- Django deployment check;
- negative permission and CSRF tests;
- threat-model mapping in tasks.

### До research worker

- config schema fuzz/negative tests;
- container escape hardening review;
- verified resource kill and orphan cleanup;
- proof that no shell/source field reaches execution.

### До production

- TLS/HSTS/CSP review;
- admin MFA and recovery drill;
- backup restore drill;
- least-privilege DB roles;
- external review auth/session/worker boundary;
- incident and rollback runbooks.

## Остаточный риск

Контейнеры на одном host не являются сильной границей против kernel exploit.
MVP снижает риск за счёт отсутствия недоверенного кода. Если когда-либо
появится пользовательский code execution, потребуется отдельный sandbox/VM
контур и новый threat model; текущая архитектура это не разрешает.
