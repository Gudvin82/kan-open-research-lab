# Content Model: Design System + Bilingual Public Shell

This feature introduces no database schema. The entities below are immutable,
version-controlled presentation contracts. They may later inform publication
models but must not be treated as those models.

## LocalizedPage

| Field | Type | Rules |
|---|---|---|
| `key` | stable enum/string | One of `home`, `research`, `methods`, `knowledge`, `about`, or a namespaced method key |
| `locale` | `ru` or `en` | Must match the locale URL |
| `route_name` | Django route name | Same semantic route name across locales |
| `title` | reviewed text | Non-empty; unique enough for navigation/SEO |
| `summary` | reviewed text | Bounded, claim-safe description |
| `translation_state` | enum | `source`, `reviewed`, `stale`, `unavailable` |
| `counterpart_key` | page key | Must resolve to the same entity in the other locale when available |

**Invariants**

- Russian is the source representation.
- An English page may be public only when its demonstration copy is reviewed.
- A missing/stale translation is labelled; it is never silently machine-filled.
- Canonical and `hreflang` links are derived from route identity, not free text.

## ResearchCard

| Field | Type | Rules |
|---|---|---|
| `slug` | stable string | Unique within shell fixtures |
| `collection` | enum | `reproduced_known_solution` or `open_problem` |
| `title` | localized text | Neutral wording |
| `summary` | localized text | Must not exceed declared evidence |
| `method` | enum/list | Initial values: `KAN`, `MLP`, `PINN`, `comparison` |
| `scientific_status` | ScientificStatus | Required text label |
| `evidence_level` | EvidenceLevel | Required text label |
| `reproducibility` | ReproducibilityState | Required text label |
| `destination` | optional route | Omitted until a useful page exists |

**Invariants**

- `open_problem` always renders a visible “remains open” statement.
- Style/color never supplies information absent from text.
- No card claims proof, discovery or superiority without a separately reviewed
  scientific publication state.

## ScientificStatus

Initial centralized vocabulary:

- `education`
- `independent_reproduction`
- `experiment`
- `empirical_pattern`
- `hypothesis`
- `proof_claim_not_present`

Each status has a short localized label and a longer “what this does/does not
show” explanation. Extending the vocabulary requires content review.

## EvidenceLevel

Initial vocabulary:

- `introductory_source_summary`
- `code_available`
- `result_available`
- `independently_reproduced`
- `formal_argument`
- `not_yet_available`

Evidence and scientific status are separate: code availability is not proof.

## ReproducibilityState

Initial vocabulary:

- `not_applicable`
- `planned`
- `partial`
- `package_available`
- `independently_verified`

The public-shell fixtures use only states supported by visible material.

## ExplanationSet

| Field | Type | Rules |
|---|---|---|
| `topic_key` | stable string | Same across levels/locales |
| `locale` | `ru` or `en` | Matches page |
| `levels` | map | Keys: `human`, `technical`, `scientific` |
| `default_level` | enum | `human` unless explicitly justified |

Each level includes:

- `availability`: `reviewed`, `stale` or `unavailable`
- `anchor`: stable section id shared conceptually across locales
- `heading`
- `body`

**State transitions:** `unavailable → reviewed`; `reviewed → stale` when the
Russian source changes materially; `stale → reviewed` after human review.

## MethodSummary

Initial keys: `kan`, `mlp`, `pinn`, `comparison`.

Required content:

- neutral purpose;
- appropriate use context;
- known limitations;
- relationship to comparison baselines;
- explanation set;
- explicit absence of performance claims in the shell.

## ComputeAvailability

The shell consumes no live worker state in this feature. If surfaced, the only
permitted value is `compute_node_unavailable`, even though the host is currently
reachable. A future integration spec owns any state transition.
