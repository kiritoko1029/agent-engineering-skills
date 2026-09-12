# AGENTS.md — Implemented Agent Notes

These Agent Notes describe shipped decisions. Follow the target project's applicable root instructions and documentation standard, and the [Agent Note format](agent-notes.md#the-file-format); check the lifecycle-specific structure with its existing validator or manual review when none exists.

## Keep an implemented Agent Note current with what actually shipped

Keep paths, symbols, defaults, and mechanisms current in the same change that alters them. Rewrite stale facts in place; do not append change history.

When a shipped note is unlikely to guide future work, archive the complete note and any existing companions through [`dsh-archive-agent-notes`](../SKILL.md) instead of continuing to maintain it.

### This is not a license to rewrite the *decision*

Update factual realization in place. A reversal of the decision or its rationale requires a new Agent Note and cross-link; a fully superseded old note may be deleted only through the consolidation rule in the [Agent Note rules](agent-notes.md).
