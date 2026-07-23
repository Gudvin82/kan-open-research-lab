# UX and Accessibility Requirements Checklist

**Purpose:** Validate that the specification defines testable UX, bilingual and
accessibility requirements before implementation.

**Created:** 2026-07-23

**Feature:** [spec.md](../spec.md)

## Bilingual information architecture

- [x] CHK001 Are default-language and locale URL rules explicit? [Spec §FR-001–FR-004]
- [x] CHK002 Is same-entity language switching required and testable? [Spec §US1]
- [x] CHK003 Are missing/stale translation states defined? [Spec §Edge Cases; Data Model]
- [x] CHK004 Are localized canonical and alternate relationships required? [Spec §FR-020]

## Scientific communication

- [x] CHK005 Is reproduced knowledge separated from open research without relying on color? [Spec §US2; FR-006–FR-009]
- [x] CHK006 Must open problems remain explicitly labelled open? [Spec §FR-007]
- [x] CHK007 Are evidence and reproducibility represented independently? [Data Model]
- [x] CHK008 Are unsupported scientific claims excluded from acceptance? [Spec §SC-007]

## Inclusive interaction

- [x] CHK009 Are keyboard, focus, skip-link and landmark expectations stated? [Spec §FR-017; US5]
- [x] CHK010 Is the smallest supported viewport explicit? [Spec §FR-018; SC-003]
- [x] CHK011 Is reduced motion covered? [Spec §US5]
- [x] CHK012 Is no-JavaScript access required for core content and explanation levels? [Spec §FR-011; FR-016]
- [x] CHK013 Are automated checks paired with manual accessibility review? [Plan §Testing; Quickstart]

## Failure and deployment states

- [x] CHK014 Is compute unavailability honest even when the host is reachable? [Spec §FR-021; Assumptions]
- [x] CHK015 Are Preview/Production isolation and no-migration requirements testable? [Spec §FR-023–FR-025]
- [x] CHK016 Is real Preview verification separated from resource-creation approval? [Spec §FR-024]

## Notes

- Checklist validates requirement quality, not implementation.
- No unresolved requirement gap was found at this checkpoint.
