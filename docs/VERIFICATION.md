# Foundation Verification

**Date:** 2026-07-23

**Environment:** macOS, uv CPython 3.13.13, Colima 0.10.3, Docker CLI 29.6.2,
Docker Engine 29.5.2, Compose 5.3.1

**Verified commit:** `a1be6fad46a0fdd97588bb15dae9a513f72700b1`

## GitHub Actions evidence

| Workflow / job | Result | Run |
|---|---|---|
| Governance / `governance` | PASS | [30024471563](https://github.com/Gudvin82/kan-open-research-lab/actions/runs/30024471563) |
| Quality / `python` | PASS | [30024472074](https://github.com/Gudvin82/kan-open-research-lab/actions/runs/30024472074) |
| Quality / `secrets` | PASS | [30024472074](https://github.com/Gudvin82/kan-open-research-lab/actions/runs/30024472074) |

The earlier Governance run `30022711627` failed on `.env.example`; commit
`a1be6fa` corrected the overly broad path rule. The superseding run above is
green and is the evidence used for Foundation acceptance.

## Code and dependency gates

| Check | Result |
|---|---|
| `uv run ruff format --check .` | PASS, 26 files formatted |
| `uv run ruff check .` | PASS |
| `uv run mypy src` | PASS, 16 source files |
| `uv run pytest` | PASS, 14 tests |
| `manage.py makemigrations --check --dry-run` | PASS, no changes |
| `manage.py check` | PASS |
| production `manage.py check --deploy --fail-level WARNING` | PASS |
| `uv run pip-audit` | PASS, no known vulnerabilities |
| `uv lock --project research_engine --check` | PASS |

The first audit found `PYSEC-2026-1845` in pytest 8.4.2. The web lock was
updated to pytest 9.1.1; tests and audit then passed.

## Runtime contracts

- Pinned `python:3.13.5-slim-bookworm` web and worker images built.
- Pinned `postgres:17.5-alpine` started healthy.
- `/health/live/` and `/health/ready/` returned 200 with PostgreSQL available.
- With PostgreSQL stopped: liveness returned 200 and readiness returned 503.
- With worker stopped: the full web smoke check passed.
- Compute status returned typed HTTP 503 `compute_node_unavailable`.
- Worker log emitted only structured startup metadata and no secrets.
- Preview/Production database labels are fail-closed and covered by tests.

## Backup drill

`scripts/backup_db.sh` produced a custom-format dump and SHA-256 sidecar.
`scripts/restore_db.sh` verified the checksum, recreated
`kan_restore_test`, restored it and received `1` from its smoke query.
The unsafe target-name guard is covered by tests.

## Vercel inspection

- `vercel.json` parses as JSON and uses the official schema URL.
- Contract test validates the documented function fields, ASGI entrypoint and
  the absence of migration/deploy commands.
- The container build ran the same static collection boundary and copied 130
  static files; it did not run migrations during image build.
- No Vercel project was linked, no deploy was performed and no resource or
  secret was created.

The current official schema declares Draft 4 while containing newer numeric
`exclusiveMinimum` keywords, so generic Draft 4 validators cannot compile the
entire remote schema. The focused contract test covers every Vercel field used
by Foundation; provider-side build validation remains a later, separately
approved linking step.

## Secret and boundary checks

- Web dependency manifest contains no PyTorch, pykan or efficient-kan.
- Worker Compose receives neither `DJANGO_SECRET_KEY` nor database admin
  credentials and uses `network_mode: none`.
- Local Gitleaks 8.30.1 scanned the working tree (about 518 KB) and three Git
  commits with redaction enabled; no leaks were found.
- GitHub secret scanning/push protection remain enabled; PR CI adds Gitleaks.
- A plaintext database credential was found only in an external workspace
  `CLAUDE.md`. Its value was not copied to this repository, Git history, logs,
  issues or PRs. Rotation remains a mandatory blocker for connecting to that
  legacy database, worker integration and every production deployment to the
  research server. It does not block a database-free Vercel Preview or public
  shell when the credential is neither used nor supplied to Vercel.

---

# Design System + Bilingual Public Shell Verification

**Date:** 2026-07-24

**Verified implementation commit:**
`f18d07112a63f4833a94e3bd3034b778a8e0503d`

## Local gates

| Check | Result |
|---|---|
| `uv run ruff format --check .` | PASS, 37 files |
| `uv run ruff check .` | PASS |
| `uv run mypy src` | PASS, 23 source files |
| `uv run pytest` | PASS, 78 tests |
| `manage.py makemigrations --check --dry-run` | PASS, no changes |
| database-free production `manage.py check --deploy --fail-level WARNING` | PASS |
| database-free production `collectstatic` | PASS, 134 files copied and 400 post-processed |
| `uv run pip-audit` | PASS, no known vulnerabilities |
| `uv lock --project research_engine --check` | PASS |
| `npm audit --audit-level=high` | PASS, 0 vulnerabilities |
| `npm test` | PASS, 24 Chromium tests |
| local Gitleaks 8.30.1 | PASS, 19 commits and about 1.02 MB scanned |

The browser suite covers same-entity RU/EN switching, no-JavaScript navigation,
keyboard focus, ten axe scans, forced colors, reduced motion, 200% zoom and
320/1440 px layouts. Axe produced no critical or serious findings. The
completed manual scope and its limitation are recorded in the feature
accessibility checklist.

## GitHub Actions evidence

| Workflow / job | Result | Run |
|---|---|---|
| Governance / `governance` | PASS | [30046970282](https://github.com/Gudvin82/kan-open-research-lab/actions/runs/30046970282) |
| Quality / `python` | PASS | [30046970138](https://github.com/Gudvin82/kan-open-research-lab/actions/runs/30046970138) |
| Quality / `secrets` | PASS | [30046970138](https://github.com/Gudvin82/kan-open-research-lab/actions/runs/30046970138) |
| Quality / `ui` | PASS | [30046970138](https://github.com/Gudvin82/kan-open-research-lab/actions/runs/30046970138) |

The passing Quality run verifies commit
`78857bb6971e5f59bd2d330239645b9f58eef323`. Its
[seven-day UI evidence artifact](https://github.com/Gudvin82/kan-open-research-lab/actions/runs/30046970138/artifacts/8579521441)
contains the Playwright HTML report and sixteen RU/EN desktop/mobile
screenshots; it expires on 2026-07-30.

## Visual and copy evidence

The reproducible command `npm run capture:ui-evidence` created sixteen ignored
PNG files under `artifacts/ui-evidence/`:

- RU and EN Home, Research and Methods at 1440×1000 and 390×844;
- RU and EN footer crops at desktop and mobile sizes.

The captures were visually inspected for hierarchy, clipping, long strings,
locale consistency, warm-paper design, readable status fields and footer
content. The Research pages visibly separate known-result reproduction from
open questions. Every open demonstration says that the problem remains open
and that a numerical result or low error is not proof.

The sorted SHA-256 manifest aggregate for the sixteen PNG files is
`a8f3b7fa1bcf9ff0f8ba2b9dce981532530b5b2e4c1163f7aa5e54c75b0a3d15`.
Screenshots and Playwright traces are intentionally excluded from Git. CI
uploads the HTML report and sixteen evidence screenshots as a seven-day
GitHub Actions artifact.

## Font evidence

Golos Text was taken from the official `googlefonts/golos-text` repository at
commit `cf2e27222937d97c2d858fff0499bcc667a64e9d`, converted without subsetting to
one variable WOFF2, and stored with SIL Open Font License 1.1. Coverage was
checked for Cyrillic and Latin; the `wght` axis covers 400–900. The file is
76,540 bytes with SHA-256
`177af0794fb0c2308b2edc76d8744549b5b390b30c67436892578c5f07c0bf00`.
`font-display: swap` and a complete system fallback keep the site usable
without the custom font.

## Deployment and resource boundary

- Public pages and production static collection work without PostgreSQL.
- The public footer and compute API retain `compute_node_unavailable`.
- No DB, publication model, migration, KAN/ML worker or server integration was
  added.
- Vercel build/startup contains no migration command; Preview cannot use a
  production-labelled DB through the settings contract.
- Node, Chromium and Playwright are development/CI-only and excluded from the
  Python image and Vercel source bundle.
- The free Vercel project is linked only to the local checkout. Git integration,
  Production auto-deploy, custom domains and paid resources are not configured.
- No PostgreSQL, `DATABASE_URL`, worker/server credential or production secret
  exists in the Vercel project.

## Real Vercel Preview

| Field | Evidence |
|---|---|
| Deployment | `dpl_3Rm1hjK9h1geGp4k4GhEnL8cfWLB` |
| Immutable URL | <https://kan-open-research-ddjjfrf0h-gudvin82s-projects.vercel.app> |
| Vercel target | `preview`, Ready |
| Source commit | `f18d07112a63f4833a94e3bd3034b778a8e0503d` |
| Verified at | 2026-07-24 00:27–00:33 Europe/Moscow |
| Region/runtime | `iad1`, Python 3.13 ASGI function |

Preview environment parameters, with secret values intentionally omitted:

- `VERCEL_ENV=preview` from Vercel system environment;
- `DEBUG=False` from `src.config.settings.preview`;
- one encrypted, random Preview-only `DJANGO_SECRET_KEY`;
- no `DATABASE_URL`, `DATABASE_ENV`, worker credential, server credential or
  Production-scoped application secret.

Real-URL checks:

| Check | Result |
|---|---|
| `/` → `/ru/`; RU/EN primary and KAN/MLP/PINN/comparison routes | PASS |
| localized RU/EN 404 | PASS |
| `/health/live/` | PASS, HTTP 200 |
| `/health/ready/` without DB | PASS, honest HTTP 503 |
| `/api/v1/system/compute-status/` | PASS, HTTP 503 `compute_node_unavailable` |
| CSS and Golos Text WOFF2 from static CDN | PASS, HTTP 200 |
| HTTPS canonical and reciprocal RU/EN `hreflang` | PASS |
| Preview `noindex, nofollow` meta and `X-Robots-Tag` | PASS |
| HSTS, frame, MIME, referrer and opener headers | PASS |
| sensitive-value scan of HTML/headers | PASS |
| Playwright/axe against Preview | PASS, 24/24 |
| keyboard, no-JavaScript, forced colors, reduced motion and 200% zoom | PASS |
| 320 px and 1440 px responsive checks | PASS, no horizontal overflow |
| browser console on RU desktop and EN 320 px | PASS, no errors/warnings |
| runtime log search for HTTP 500, migrations, PostgreSQL and worker | PASS, no matches |

Vercel Authentication protects the Preview. `vercel curl` and an automation
bypass value held only in process memory were used for automated checks.
Playwright disables trace capture while that value is present. No bypass value
was written to Git, PR text, logs or retained browser artifacts.

Spec Kit T051 convergence checked 26 functional requirements, 10 success
criteria, 15 acceptance scenarios, eight plan decisions and eight constitution
principles. It found zero missing, partial, contradictory or unrequested
implementation gaps, so no Convergence phase or remediation tasks were
appended.

### Deployment corrections and limitations

- Vercel CLI 53.3.2 treated an initial `vercel deploy --yes` invocation as a
  Production target even though `--prod` was not supplied. Deployment
  `dpl_DRbR6AZwZ29MMk4SH66xzeLa5A1z` failed during configuration validation,
  produced no application build and never served the site. Every later command
  used explicit `--target preview`; no usable Production deployment was made.
- Two explicit Preview attempts (`dpl_51whDjbTWyt4Uf8ev63qzsM5RsVP` and
  `dpl_HwLFpehnA1TMTqXZjoEQPYqEys2f`) exposed a Vercel Python-runtime packaging
  conflict with the internal `src/public` path. They returned HTTP 500 and are
  retained only as diagnostic evidence. Renaming the internal package to
  `src/webapp` and its template namespace to `lab` fixed the bundle; the final
  immutable Preview above returns the expected responses.
- Deployment Protection requires the project owner to sign in to the immutable
  URL or use a separately generated, short-lived share link.
- Cold/warm sampled time-to-first-byte was about 0.33–0.74 seconds during the
  verification window; this is evidence from one region, not an SLA.

## Known limitations

- Demonstration research entries are reviewable static fixtures, not published
  experimental results.
- English copy is checked in and reviewed as project copy, but no general
  editorial translation workflow exists yet.
- Publication models, search, admin editorial workflow, analytics, legal
  documents and public email are intentionally absent.
- Production deployment, GitHub–Vercel auto-deploy, custom domain, database and
  worker integration remain intentionally unverified and separately gated.

---

# Production Release Blocker Remediation

**Date:** 2026-07-24

**Branch:** `codex/003-production-release-blockers`

**Base commit:** `a1f69fe1dfe37dd30f9bb7deda6720289811a7ef`

**Scope:** T005–T010 only. The earlier Production authorization for the base
commit is revoked. No Vercel environment, secret, deployment, alias, domain,
Git integration, database or worker state was changed.

## Security contracts

Production host configuration now:

1. requires the exact current immutable hostname from `VERCEL_URL`;
2. selects the canonical base from a validated `PUBLIC_BASE_URL`, otherwise
   from `VERCEL_PROJECT_PRODUCTION_URL`;
3. adds only exact validated hostnames from those sources;
4. accepts `DJANGO_ALLOWED_HOSTS` only as an optional, strictly validated
   exact-host extension;
5. strips accepted scheme, path and port before allowlisting;
6. rejects wildcard, userinfo, query, fragment, unsupported scheme, malformed
   hostname, control characters and ambiguous ports;
7. fails closed when the immutable or stable Production host is absent.

Neither `*` nor `.vercel.app` is present in the allowlist. An arbitrary sibling
such as `evil.vercel.app` receives HTTP 400.

Canonical and reciprocal RU/EN `hreflang` values use the stable configured
HTTPS origin and never `request.get_host()` or the immutable staged hostname.
For the first release this resolves to
`https://kan-open-research-lab.vercel.app`.

Indexing control is no longer Preview-specific. Preview and Production both
emit HTML `noindex, nofollow` and the matching `X-Robots-Tag` by default.
There is no environment mutation or first-release toggle that enables
indexing.

## Test-first evidence

The new Production contracts were added as failing tests before the
implementation. The initial targeted run failed in eight expected places:
mandatory legacy `DJANGO_ALLOWED_HOSTS`, wildcard acceptance, missing
Production robots controls and request-Host-derived canonical metadata. The
same targeted suite passed after implementation.

## Local gates

| Check | Result |
|---|---|
| `ruff format --check .` | PASS, 38 files |
| `ruff check .` | PASS |
| `mypy src` | PASS, 24 source files |
| full `pytest` | PASS, 88 tests |
| Production `check --deploy --fail-level WARNING` with an ephemeral random test secret | PASS |
| Production `makemigrations --check --dry-run` | PASS, no changes |
| `pip-audit` | PASS, no known vulnerabilities |
| `npm audit --audit-level=high` | PASS, 0 vulnerabilities |
| Playwright/axe | PASS, 24/24 |
| worker lock check | PASS |
| Gitleaks Git history | PASS, 10 commits |
| Gitleaks intended tracked diff and new source | PASS, no leaks |

Blocker-scope Spec Kit convergence checked 10 relevant functional
requirements, two measurable success criteria, three plan decisions and
Constitution principles V, VII and VIII. It found zero missing, partial,
contradictory or unrequested gaps for T005–T010, so no convergence tasks were
appended. T011+ remain intentionally gated release execution, not gaps in this
PR.

The Production simulation used `VERCEL_ENV=production`, the test-only exact
immutable hostname
`kan-open-research-immutable-test.vercel.app`, stable hostname
`kan-open-research-lab.vercel.app`, no `DJANGO_ALLOWED_HOSTS`, no database
variables and an ephemeral random secret held only for the command lifetime.
Its value was neither printed nor written.

A raw scan of the entire local working directory correctly detected an ignored
provider credential inside `.vercel/`. No value was displayed or copied. The
directory remains excluded from Git; history, intended diff and new-source
scans are clean.

## Remaining gates

- GitHub `governance`, `python`, `secrets` and `ui` results belong to the draft
  blocker-remediation PR and must be green before merge.
- Production secret creation, staged deployment, promotion and evidence remain
  T011+ and require a new owner authorization for the future merged SHA.
