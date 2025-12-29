
## [2025-12-28 21:06:48]
decision_reminder.py hook was crashing on Windows due to emoji encoding (cp1252). Fixed by replacing Unicode emojis with ASCII text. Line 121 print statement was the culprit.

## [2025-12-28 21:16:11]
Fixed Windows cp1252 encoding issue in 31+ hooks. Python print() statements with emojis crash on Windows. Solution: Replace all emojis with ASCII equivalents like [FAST], [OK], [WARN], etc. Used Python script to batch-replace since sed failed with multi-byte chars.

## [2025-12-28 21:21:47]
Pilot + Beads workflow: Beads (bd) is dependency-aware task tracker. Pilot is autonomous agent that picks up tickets with --labels pilot. Delegate to Pilot when task touches >3 files, is scaffolding, or hazardous. Creates via bd create + workmux spawn. Use for multi-session, complex features.

## [2025-12-28 21:30:43]
Beads (bd) is project-specific by default - creates .beads/beads.db per project. For global db: use --db flag (bd --db ~/.beads/global.db) or create wrapper script 'gbd'. Hybrid approach recommended: global for cross-cutting tasks, project-specific for feature work.
