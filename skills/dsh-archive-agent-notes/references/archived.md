# AGENTS.md — Archived Agent Notes

Archived Agent Note records under the kind directories are frozen historical snapshots, not current authority. Never edit, reformat, translate, repair, delete, or move a sealed artifact; use an active Agent Note or current documentation for new decisions and facts.

The archival change may only relocate a complete note and its existing companions, insert the identical `Archived: YYYY-MM-DD` line below `Status: implemented` in the note and any companion translations, re-record any existing consistency sidecar, and repair or delete inbound links. Do not inspect, verify, or repair links out of archived notes.

Run the [`dsh-archive-agent-notes`](../SKILL.md) workflow. Use the project's existing archive verifier and, if it maintains a manifest, append only new artifact hashes after verifying all existing seals. Validation must reject changed or missing sealed artifacts, incomplete associated records, unknown kind folders, and invalid archive metadata. If no verifier exists, manually inspect the diff against the applicable base revision for these invariants and report the checks and their limits; do not create a new manifest or validation framework merely to use this workflow.
