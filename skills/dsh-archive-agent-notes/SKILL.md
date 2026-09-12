---
name: dsh-archive-agent-notes
description: Use when adding, auditing, pruning, archiving, restoring, or reviewing Agent Notes in a project using Agent Notes; checks every new note for superseded active records, classifies implemented notes by future decision value, deletes rejected notes that no longer prevent a tempting fallacy, and applies the frozen archived/{kind} record rules and any existing manifest checks.
---

# Archive DeepSeek Harness Agent Notes

Reduce the active decision corpus without erasing history that can still guide work. Judge every note semantically; word count and age are discovery aids, never archive criteria.

## Read the contracts

Read [the Agent Note rules](references/agent-notes.md), [the archive instructions](references/archived.md), and the [implemented-note instructions](references/implemented.md) when applicable before classifying. Use current code, configuration, package docs, generated catalogs, newer Agent Notes, and inbound links to establish whether a rationale still owns or constrains anything.

A record is an Agent Note plus any companion translations or consistency files already required by the project. Handle that associated set together; this workflow does not require a project to introduce translations or sidecars. Apply these rules within the current task scope and existing project permissions.

## Check supersession when adding a note

Every new Agent Note triggers a scoped audit of active notes covering the same decision, mechanism, or rejected alternative. Classify each full or partial supersession while writing the new note: archive qualifying implemented records in the same PR, retain and cross-link partial supersessions or independently useful rationale, reject obsolete proposals, and delete rejected notes that no longer prevent a plausible mistake. Apply the Agent Note consolidation rule when the new owner absorbs every unique proposition; do not defer a known match to a later corpus audit.

## Classify by future value

Apply these lifecycle-specific outcomes:

- **Implemented — keep active:** retain a note when its rationale, alternatives, negative guarantees, durable/wire semantics, ownership boundary, security rule, or reintroduction condition is likely to guide a future change. Length does not matter.
- **Implemented — archive:** archive a note when the shipped decision is complete and its body is unlikely to guide future work, such as one-off UI chrome, a narrow adapter, a minor closed bug, superseded implementation detail, or process history whose current behavior is obvious elsewhere.
- **Proposed — never archive:** keep a live proposal active; if it is no longer worth pursuing, reject it with an honest reason and satisfy the rejected lifecycle format.
- **Rejected — keep only as a guardrail:** retain a rejection only when the losing proposal remains a tempting, meaningful mistake and the note explains why it loses.
- **Rejected — delete:** delete the whole record when the rejected idea is obsolete, superseded, no longer plausible, or unlikely to prevent re-litigation. Repair or delete inbound links.

Do not archive toward a quota. Inspect every note in scope, classify analogous groups under one principle, use best judgment for close cases, and record genuinely borderline decisions for the handoff.

## Calibrated examples

These upstream DeepSeek Harness examples set the bar; the word counts demonstrate that size is not the test.

Archive implemented notes such as:

- collapsed sidebar control rail — 533 words: closed, minor UI behavior;
- Commander argument adapter — 1,498 words: substantial implementation detail with little future design leverage;
- documentation graph atlas — 920 words: completed documentation machinery whose current generators are authoritative.

Keep implemented notes such as:

- event-sourced sessions — 248 words: foundational authority and durability boundary;
- single Harness-home resolver — 596 words: cross-product ownership rule;
- project session directories — 628 words: durable storage and identity policy;
- parallel pre-push gates — 400 words: borderline, but still guides gate scheduling and resource tuning;
- dropped image content block — 334 words: keep until multimodal support lands, because it states the coordinated reintroduction condition.

For rejected notes:

- keep folding the compaction package split — 426 words: the temptation to merge the packages remains meaningful;
- delete streaming workflow progress through tool calls — 972 words: its ACP/UI premise is obsolete;
- delete dropping ACP terminal metadata — 362 words: the later automation-only ACP decision resolved the question.

## Archive one implemented record

1. Move the complete note and its existing companion files from `implemented/<kind>/` to `archived/<kind>/`; `implemented` is deliberately absent from the archive path. For a project using the upstream convention, these are `foo.md`, `foo.zh.md`, and `foo.i18n.yaml`; a project without companions moves only `foo.md`.
2. Make no body edits. Insert only `Archived: YYYY-MM-DD` immediately below `Status: implemented` in the note and any companion translations, using the archival date and the same value in each.
3. If the project uses consistency sidecars, re-record them mechanically for the metadata-only edits using its existing tooling. Do not translate, reformat, update facts, or repair links inside the note.
4. Search for inbound links from active prose. Redirect them to current authority, retarget them to the archived path only when the historical snapshot is intentionally cited, or delete them. Never verify or repair links out of the archived note.
5. Use the project's existing archive verifier. If it maintains a manifest, first prove every existing seal still matches, then append only the new record hashes and run its normal verifier afterward. If no verifier exists, inspect the diff against the applicable base revision: existing archived records must remain unchanged, and new archives may contain only the permitted archival changes. Report that verification was manual and any limits; do not introduce a new manifest or validation framework merely to use this skill.

After the record is sealed, never edit, move, translate, reformat, or delete it. Archived notes remain valid inbound-link targets but are historical snapshots, not authority for current behavior.

## Validate and report

Run the project's existing archive verifier and its focused test, documentation checks, lint, and `git diff --check`, where available; select any additional evidence through the project's applicable pre-push checks. Where a checker is absent, review the relevant diff against these rules and report the manual checks and their limits rather than claiming that an unavailable gate passed.

Report active implemented notes kept, implemented notes archived, rejected notes kept/deleted, proposed notes rejected if any, and every genuinely borderline case with its word count and chosen outcome. Do not claim archived outbound links are valid: this workflow intentionally never checks them.
