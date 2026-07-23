# Research: Design System + Bilingual Public Shell

## Decision 1 — Server-rendered Django, not a separate frontend

**Decision:** Extend the modular Django monolith with a `src.public` app,
templates and namespaced CSS. Use progressive enhancement only where it
preserves a fully functional link-based fallback.

**Rationale:** The public surface is content-led, must work without JavaScript
and does not need client state or an API. A separate frontend would duplicate
routing, localization, security and build concerns.

**Alternatives considered:**

- React/Next.js shell: rejected because it adds a second application and
  conflicts with the Django-first MVP without providing required value.
- Static-site generator: rejected because it would introduce a parallel content
  and routing system before publication workflows are designed.

## Decision 2 — Locale-prefixed URLs are authoritative

**Decision:** Use Django `LocaleMiddleware`, translation hooks and
`i18n_patterns(prefix_default_language=True)` for `/ru/` and `/en/`. `/`
redirects to `/ru/` without inspecting browser language. Named counterpart
routes preserve page identity. A first-party language preference may be stored,
but never overrides an explicit locale URL.

**Rationale:** Django provides the necessary translation and locale middleware
in the existing runtime. Stable locale-prefixed URLs are shareable, testable and
SEO-friendly, while avoiding surprising automatic redirects.

**Primary source:** [Django translation documentation](https://docs.djangoproject.com/en/6.0/topics/i18n/translation/)

**Alternatives considered:**

- Browser-language negotiation at `/`: rejected because Russian must be the
  deterministic default.
- Query parameters such as `?lang=en`: rejected as a canonical route because
  they weaken stable counterpart URLs.
- Database-backed translations: deferred until publication models exist.

## Decision 3 — Version-controlled demonstration content

**Decision:** Store the bounded shell content in typed immutable Python
structures and translated UI strings/templates. Do not add database tables or
migrations.

**Rationale:** This stage establishes information architecture and vocabulary,
not editorial workflows. Static content keeps Preview independent from any DB,
reduces failure modes and makes scientific wording reviewable in the PR.

**Alternatives considered:**

- Django models/admin: deferred because publication state, authorship and
  translation workflow need their own specification.
- JSON/YAML content files: not selected because typed Python gives validation
  without a new parser or schema tool.

## Decision 4 — CSS token system with resilient typography

**Decision:** Translate `docs/DESIGN.md` into CSS custom properties and a small
component vocabulary. Use a warm-paper palette, editorial serif headings,
neutral sans body text and mono metadata. The system-font fallback must remain
fully usable. Any bundled font requires an OFL/license file and performance
review.

**Rationale:** Tokens make the design auditable and reusable without importing a
component framework. Font failure is an explicit edge case.

**Alternatives considered:**

- Remote font CDN: rejected because it adds a privacy, availability and
  performance dependency.
- UI framework: rejected because the initial shell needs a small, bespoke set of
  semantic components.

## Decision 5 — Playwright plus axe for browser evidence

**Decision:** Add pinned `@playwright/test` and `@axe-core/playwright`
development dependencies. Use browser tests for bilingual journeys, keyboard
behavior, 320 px overflow and screenshot review. Scan all five primary pages in
both locales for critical/serious automatically detectable issues, then perform
manual keyboard, zoom, landmarks and reduced-motion review.

**Rationale:** pytest can validate routes and HTML contracts, but not layout,
focus behavior or rendered accessibility. Playwright's official guidance
integrates axe while explicitly stating that automation must be supplemented by
manual assessment.

**Primary source:** [Playwright accessibility testing](https://playwright.dev/docs/accessibility-testing)

**Alternatives considered:**

- pytest only: rejected because it cannot establish responsive/browser success.
- Screenshot testing only: rejected because pixels do not validate semantics,
  labels or keyboard use.

## Decision 6 — Vercel environments are isolated by policy and checks

**Decision:** Treat non-`main` branches as Preview and protected `main` as the
only Production branch. Scope variables independently per Vercel environment;
do not define a Production DB variable for Preview. Build remains
`collectstatic` only. Add tests that reject migration commands and enforce
fail-closed environment selection. A real Preview is a later acceptance gate,
not an action in this planning checkpoint.

**Rationale:** Vercel documents distinct Local, Preview and Production
environments with environment-specific variables, and Git integration maps
non-production branches to Preview. Explicit isolation is still enforced in
repository tests rather than trusted as an informal dashboard convention.

**Primary sources:**

- [Vercel environments](https://vercel.com/docs/deployments/environments)
- [Vercel Git deployments](https://vercel.com/docs/git)
- [Vercel system environment variables](https://vercel.com/docs/environment-variables/system-environment-variables)

**Alternatives considered:**

- Preview connected read-only to Production DB: rejected because read-only
  credentials still expose production data.
- Automatic migrations during build/startup: rejected because retries and
  concurrent deployments make migration ownership unsafe.
- Worker on Vercel: rejected by architecture and resource boundary.

## Decision 7 — Managed PostgreSQL remains an ADR-gated later choice

**Decision:** Shortlist Neon and Supabase for ADR-0003; do not select or create
either in this feature. Compare current cost, an EU region, backup/restore,
Preview/Production isolation, connection limits/pooling and controlled
migration workflow immediately before a DB-backed stage.

**Rationale:** Both offer managed PostgreSQL and EU placement, but their Preview
models and bundled product scope differ. Current provider terms are volatile
and must be rechecked when the decision is made.

**Current comparison snapshot (2026-07-23):**

| Criterion | Neon | Supabase |
|---|---|---|
| Cost model | Free tier and usage-based paid tiers; current pricing advertises a typical Launch spend around USD 15/month | Project/organization plans plus usage; exact project and branching costs must be captured in ADR |
| EU | Region availability must be verified for the chosen integration at ADR time | General Central EU (Frankfurt) and several specific EU AWS regions documented |
| Backups | Restore window/time travel varies by plan | Daily backups on Pro/Team/Enterprise; 7/14/30-day retention respectively; PITR is separately priced |
| Preview isolation | Database branches and a Vercel Preview integration are documented | Separate data-less Preview branches and credentials are documented |
| Product scope | PostgreSQL-focused | Dedicated PostgreSQL plus Auth, Storage, Realtime and other services that this MVP may not need |

**Primary sources:**

- [Neon pricing](https://neon.com/pricing)
- [Neon branching and Preview integration](https://neon.com/docs/guides/branching-intro)
- [Supabase regions](https://supabase.com/docs/guides/platform/regions)
- [Supabase database backups](https://supabase.com/docs/guides/platform/backups)
- [Supabase branching](https://supabase.com/docs/guides/deployment/branching)

**Alternatives considered:**

- Reusing the old server DB immediately: rejected until the exposed external
  credential is rotated and the server production gate is cleared.
- Self-hosting a new web DB on the research server: possible later, but it
  couples public-site availability to the compute host and needs its own
  operations/cost comparison.

## Decision 8 — Reachable server is not an integrated compute node

**Decision:** Keep the public state `compute_node_unavailable` until a separate
worker-integration specification defines authenticated connectivity, secret
rotation, isolation, observability and rollback. No server change occurs here.

**Rationale:** Network reachability proves host availability only; it does not
prove the worker control plane is safe or ready.
