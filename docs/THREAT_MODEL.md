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
- независимая доступность web и research node;
- Vercel/managed PostgreSQL/object-storage credentials.

## Границы доверия

1. Интернет → Vercel edge/Django function.
2. Admin browser → authenticated Django admin/control plane.
3. Vercel web-role → managed PostgreSQL over TLS.
4. Research server worker-role → managed PostgreSQL over TLS.
5. Worker → private temp/artifact storage.
6. Review boundary → public object storage.
7. GitHub/Vercel integration → Preview/production deployments.
8. External datasets/repos → dependency and data intake.

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
| Preview получает production DB | critical | distinct Preview DB/role; scoped Vercel env; fail closed |
| Migration из Preview/build | critical | migrations only in separate gated release job |
| Stolen Vercel/storage credential | high | environment scoping, least privilege, rotation, no Git/worker copy |
| Worker offline interpreted as running | high | heartbeat, typed unavailable state, no Vercel fallback |
| Public exposure of private artifact | high | review gate, separate buckets, private-by-default object ACL |

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
- no Vercel token, Django secret or public-storage write credential.

## Hybrid deployment controls

- Vercel Preview and Production have separate environment scopes.
- Preview never receives production `DATABASE_URL` or object-storage keys.
- Django liveness does not require DB; readiness accurately reports DB state.
- Web stays read-only/available when worker is offline.
- Object storage uses separate public-publisher and private-worker roles.
- Production migrations require backup evidence and an explicit release gate.

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
- confirmation that Preview is isolated from production data.

## Остаточный риск

Контейнеры на research host не являются сильной границей против kernel exploit.
Hybrid deployment также добавляет third-party control planes и сетевой DB
доступ. MVP снижает риск отсутствием недоверенного кода и раздельными ролями.
Если появится пользовательский code execution, потребуется отдельный sandbox/VM
и новый threat model; текущая архитектура это не разрешает.
