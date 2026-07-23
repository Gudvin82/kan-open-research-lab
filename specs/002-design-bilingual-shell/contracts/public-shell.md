# Contract: Bilingual Public Shell

## Route contract

| Entity | Russian | English |
|---|---|---|
| Root | `/` → `/ru/` | Not browser-negotiated |
| Home | `/ru/` | `/en/` |
| Research | `/ru/research/` | `/en/research/` |
| Methods | `/ru/methods/` | `/en/methods/` |
| Knowledge Base | `/ru/knowledge/` | `/en/knowledge/` |
| About | `/ru/about/` | `/en/about/` |
| KAN | `/ru/methods/kan/` | `/en/methods/kan/` |
| MLP | `/ru/methods/mlp/` | `/en/methods/mlp/` |
| PINN | `/ru/methods/pinn/` | `/en/methods/pinn/` |
| Comparison | `/ru/methods/comparison/` | `/en/methods/comparison/` |

Unsupported locale prefixes and unknown pages return the normal localized-safe
404; they do not silently redirect to a different entity.

## Per-page HTML contract

Every public response includes:

- `<html lang="ru">` or `<html lang="en">`;
- one skip link targeting the primary `<main>`;
- semantic `header`, `nav`, `main` and `footer` landmarks;
- one visible page-level heading;
- canonical URL;
- reciprocal `hreflang="ru"` and `hreflang="en"` links;
- localized title and description;
- a same-entity language link;
- no required JavaScript for content/navigation;
- text equivalents for status and decorative icon suppression.

## Research contract

The Research page exposes two labelled sections:

1. independently reproduced known solutions;
2. open problems and verifiable progress.

Every card exposes, as text:

- collection;
- scientific status;
- method;
- evidence level;
- reproducibility state.

Every open-problem card includes an explicit sentence that the problem remains
open. The page includes a global statement that numerical evidence is not a
proof.

## Explanation-level contract

Human, Technical and Scientific levels are ordinary links to stable anchors or
stable level URLs/query state. The selected level has a programmatically
identifiable current state. Missing content is labelled `unavailable`; another
level is never substituted silently.

## UI state contract

- Header navigation remains operable at 320 px without page-level overflow.
- Focus is visible and ordered.
- Reduced-motion preference disables non-essential motion.
- Status meaning survives grayscale/high-contrast review.
- `compute_node_unavailable` is the only displayed compute state in this stage.

## Deployment contract

- `vercel.json` and build metadata contain no `migrate`, worker or ML command.
- `DATABASE_ENV=preview` is required for Preview if a DB is ever supplied.
- Production DB secrets are not scoped to Preview.
- Production branch is `main`; all feature branches remain Preview.
- No external project/resource is created without owner approval.
