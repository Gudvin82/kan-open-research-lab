# Feature Specification: Design System + Bilingual Public Shell

**Feature Branch**: `codex/design-bilingual-shell`

**Created**: 2026-07-23

**Status**: Draft — planning checkpoint, implementation not started

**Input**: Create a light, accessible RU/EN public shell for the KAN Open
Research Lab, with honest scientific-status communication and no ML execution.

## User Scenarios & Testing

### User Story 1 - Read and navigate in Russian or English (Priority: P1)

A public reader can enter the site in Russian by default, reach every primary
section, switch to English without losing the current page, and retain the
selected language on later navigation.

**Why this priority**: The shell is not usable as a bilingual public product
unless navigation, page identity and language behavior are coherent first.

**Independent Test**: Open each primary Russian page, switch languages and
confirm that the equivalent English page opens with the same semantic purpose;
repeat navigation without client-side scripting.

**Acceptance Scenarios**:

1. **Given** a first-time reader opens the root URL, **When** the page is
   displayed, **Then** Russian content is the default and both language options
   remain visible.
2. **Given** a reader is on any primary RU or EN page, **When** they switch
   language, **Then** the equivalent page opens rather than the home page.
3. **Given** a reader chose English, **When** they follow internal navigation,
   **Then** the English locale remains selected.

---

### User Story 2 - Distinguish reproduced knowledge from open research (Priority: P1)

A reader can immediately distinguish known solutions that the laboratory
independently reproduces from open problems where only experiments, partial
results and progress are reported.

**Why this priority**: This distinction is the central scientific-honesty
promise and must shape the interface before publication workflows exist.

**Independent Test**: Review the home and research pages using only headings,
card labels and disclaimers; a reader can classify every example as reproduced
knowledge or open research without relying on color.

**Acceptance Scenarios**:

1. **Given** the research overview is open, **When** a reader scans the page,
   **Then** reproduced work and open problems appear in separate named regions.
2. **Given** an open-problem card is shown, **When** it is read, **Then** a
   visible disclaimer states that the problem remains open.
3. **Given** any research card is shown, **When** assistive technology reads it,
   **Then** status, method, evidence level and reproducibility are available as
   text.

---

### User Story 3 - Choose an explanation depth (Priority: P2)

A reader can view demonstration material at human, technical or scientific
depth and understand when a level is not yet available.

**Why this priority**: The three-level model is the educational identity of the
laboratory, but it can be built after the bilingual navigation and honesty
boundary are established.

**Independent Test**: On a demonstration method page, select each explanation
level and confirm the same topic and reading position are preserved; missing
levels are explicitly labelled.

**Acceptance Scenarios**:

1. **Given** a method summary is open, **When** the reader changes explanation
   level, **Then** the topic and nearest section remain stable.
2. **Given** a level has no reviewed content, **When** it is selected or listed,
   **Then** it is identified as unavailable rather than silently substituted.
3. **Given** JavaScript is unavailable, **When** the page is read, **Then** all
   published explanation sections remain reachable through ordinary links.

---

### User Story 4 - Explore methods and project context (Priority: P2)

A reader can visit the home, Research, Methods, Knowledge Base and About pages,
including introductory shells for KAN, MLP, PINN and comparative experiments.

**Why this priority**: These destinations establish a stable information
architecture that later content and research features can extend.

**Independent Test**: Traverse all primary navigation and footer links in both
languages; no route is empty, misleading or disconnected.

**Acceptance Scenarios**:

1. **Given** the Methods page is open, **When** a reader reviews the starting
   method set, **Then** KAN, MLP, PINN and comparative experiments are present
   with neutral, non-promotional summaries.
2. **Given** a shell page lacks substantive publications, **When** it is opened,
   **Then** a useful scope explanation and honest empty state are shown.
3. **Given** any primary page is open, **When** the footer is reached, **Then**
   mission, research/knowledge/project navigation, GitHub, language control and
   scientific disclaimer are available.

---

### User Story 5 - Use the shell across devices and abilities (Priority: P2)

A keyboard, screen-reader or small-screen user can navigate and understand the
same primary information without loss of meaning.

**Why this priority**: Accessibility and responsive behavior are constitutional
requirements, not later visual polish.

**Independent Test**: Complete the primary navigation, language switch and
explanation-level journey at 320 px and desktop width using keyboard only and
with reduced motion enabled.

**Acceptance Scenarios**:

1. **Given** keyboard-only navigation, **When** focus moves through the page,
   **Then** a skip link, logical order and visible focus are present.
2. **Given** a 320 px viewport, **When** a page includes long labels or a wide
   comparison, **Then** content remains readable without page-level horizontal
   scrolling.
3. **Given** reduced-motion preference, **When** interactive states change,
   **Then** non-essential motion is absent.

### Edge Cases

- A translated counterpart is missing or explicitly stale.
- A locale-prefixed URL is unknown or a reader enters an unsupported locale.
- Long Russian and English labels exceed the expected navigation width.
- A research card has no code, result or reproducibility package yet.
- A scientific status is unfamiliar, withdrawn or cannot be represented by a
  short label.
- One or two explanation levels exist, but the third is unavailable.
- The compute node is reachable as a server but not connected to the web
  control plane.
- JavaScript, custom fonts or decorative icons fail to load.
- A footer contact email, legal link or analytics policy is not yet approved.

## Requirements

### Functional Requirements

- **FR-001**: The public root MUST default to Russian without forcing a
  browser-language redirect.
- **FR-002**: Every primary public destination MUST have `/ru/` and `/en/`
  routes representing the same semantic entity.
- **FR-003**: Language switching MUST preserve the current entity and MUST NOT
  fall back to the home page when a counterpart exists.
- **FR-004**: The selected locale MUST persist across internal navigation while
  URL locale remains the shareable source of truth.
- **FR-005**: Primary navigation MUST include Home, Research, Methods,
  Knowledge Base and About in both languages.
- **FR-006**: The research overview MUST visibly separate independently
  reproduced known solutions from open problems.
- **FR-007**: Every open-problem representation MUST state that the problem
  remains open and MUST NOT imply a solution from numerical evidence.
- **FR-008**: Research cards MUST expose scientific status, method, evidence
  level and reproducibility state as text, not color alone.
- **FR-009**: Scientific status language MUST follow the centralized status
  vocabulary and MUST distinguish education, reproduction, experiment,
  empirical pattern, hypothesis and proof-related claims.
- **FR-010**: Demonstration material MUST expose Human, Technical and
  Scientific explanation levels, with explicit completeness state.
- **FR-011**: Switching explanation level MUST preserve the topic and nearest
  reading position; ordinary links MUST provide a no-script alternative.
- **FR-012**: The Methods shell MUST include neutral foundations for KAN, MLP,
  PINN and comparative experiments without performance claims.
- **FR-013**: Empty shell sections MUST explain their intended scope and next
  expected content rather than generate empty SEO pages.
- **FR-014**: The global footer MUST include project mission, research,
  knowledge and project navigation, GitHub, scientific disclaimer and RU/EN
  control.
- **FR-015**: Unapproved contact, legal, cookie or analytics links MUST be
  omitted or labelled unavailable; invented owner details are forbidden.
- **FR-016**: Core content and navigation MUST remain usable without
  client-side scripting.
- **FR-017**: The shell MUST meet WCAG 2.2 AA targets, including keyboard
  access, skip link, visible focus, semantic landmarks, contrast, language
  metadata and reduced-motion support.
- **FR-018**: Layouts MUST remain readable from 320 px through large desktop
  widths and MUST handle long RU/EN text.
- **FR-019**: Status MUST never be communicated by color or icon alone.
- **FR-020**: Pages MUST provide localized titles/descriptions, canonical and
  alternate-language relationships without automatically publishing
  unreviewed translation text.
- **FR-021**: The public shell MUST continue to work when the compute node is
  disconnected and MUST display `compute_node_unavailable` honestly wherever
  compute state is surfaced.
- **FR-022**: This feature MUST NOT execute KAN, MLP, PINN or other ML workloads
  and MUST NOT add model libraries to the public web environment.
- **FR-023**: Preview delivery MUST use non-production configuration and MUST
  never run schema migrations automatically.
- **FR-024**: A real minimal Preview is a completion gate, but project linking,
  external databases, storage and paid resources require separate owner
  approval before creation.
- **FR-025**: The production release path MUST originate only from protected
  `main`; Pull Requests MUST remain Preview-only.
- **FR-026**: Basic UI, bilingual-linking, accessibility and responsive
  regression coverage MUST exist before the feature is accepted.

### Key Entities

- **Localized Page**: A primary destination with stable identity, locale,
  localized title/summary, counterpart link and translation state.
- **Research Card**: A concise representation of a known-solution
  reproduction or open problem with method, scientific status, evidence level,
  reproducibility state and optional destination.
- **Explanation Level**: Human, Technical or Scientific presentation of the
  same topic with availability and section identity.
- **Method Summary**: Neutral introduction to a method, its purpose,
  limitations and comparison context.
- **Scientific Status**: Central text label and explanation defining the
  epistemic strength of displayed material.

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100% of primary destinations are reachable under both `/ru/` and
  `/en/`, and every language switch preserves semantic page identity.
- **SC-002**: In a structured review, every sample research card can be
  classified as reproduced knowledge or open research using text alone.
- **SC-003**: All primary journeys complete at 320 px and desktop width without
  page-level horizontal scrolling or loss of navigation.
- **SC-004**: Keyboard-only review completes skip-to-content, primary
  navigation, language switch and explanation-level selection with visible
  focus and logical order.
- **SC-005**: Automated accessibility checks report no critical or serious
  violations on the five primary pages in both languages.
- **SC-006**: All primary pages remain readable and navigable when client-side
  scripting, custom fonts and decorative icons are unavailable.
- **SC-007**: No open-problem sample or method introduction contains an
  unqualified statement that a scientific problem has been solved.
- **SC-008**: A first-time reader can find Research, Methods, Knowledge Base and
  About from the header or footer within one navigation action.
- **SC-009**: A minimal Preview is reviewed from a Pull Request with no
  production database credential, automatic migration or worker execution.
- **SC-010**: Public-page visual review confirms the approved warm-paper,
  editorial hierarchy in both Cyrillic and Latin text at all target widths.

## Assumptions

- `KAN Open Research Lab` remains the working public name until the owner
  approves a final name and domain.
- Public contact email and optional legal/analytics links are omitted until
  explicitly supplied and approved.
- Shell content is curated demonstration copy stored without introducing
  publication, knowledge-graph or experiment database models in this feature.
- Russian is the source language. English demonstration copy is human-reviewed
  for this shell; no machine translation is auto-published.
- URL locale is authoritative. A first-party essential preference may improve
  navigation but never overrides an explicit locale URL.
- The research server is currently reachable, but the worker remains
  disconnected until a separate worker-integration specification and credential
  rotation are complete.
- Managed PostgreSQL selection, database connection and migrations are deferred
  behind an ADR and separate owner approval.
- A minimal real Preview is required before feature completion, but this
  planning checkpoint creates no Vercel project or external resource.
