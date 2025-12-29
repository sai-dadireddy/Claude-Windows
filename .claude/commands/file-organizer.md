---
description: Intelligent file decluttering with parallel agents (analyze|clean|rag|archive)
argument-hint: <action> [path]
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
model: sonnet
---

# File Organizer - Intelligent Decluttering

Action: $ARGUMENTS (defaults to current project)

## What This Does (Parallel Agent Execution)

### 6 Parallel Agents for Maximum Speed

**Agent 1: Document Analyzer**
- Scans all .md, .txt, .pdf, .docx files
- Identifies: duplicates, outdated, important, archive-worthy
- Suggests: Keep, RAG, Archive, Delete

**Agent 2: Code File Analyzer**
- Scans .js, .ts, .py, .java, etc.
- Identifies: unused, test files, generated code
- Suggests: Keep, Refactor, Archive, Delete

**Agent 3: Configuration Analyzer**
- Scans .json, .yaml, .env, .config files
- Identifies: duplicates, backups, outdated
- Suggests: Keep, Consolidate, Archive, Delete

**Agent 4: Media/Asset Analyzer**
- Scans .png, .jpg, .svg, .pdf, etc.
- Identifies: unused, duplicates, large files
- Suggests: Keep, Compress, Archive, Delete

**Agent 5: Archive/Backup Analyzer**
- Scans *.backup, *.old, *.copy, archive/ folders
- Identifies: safe to delete, need to keep
- Suggests: Delete, Keep (with reason)

**Agent 6: RAG Integration Manager**
- Takes important docs from other agents
- Adds to RAG collections
- Archives original after indexing
- Updates .claude/context/rag-collections.md

---

## Available Actions

### analyze
Scan files and generate recommendations (no changes)

**Execution**:
```bash
# Launches 6 parallel agents
Task 1: @docs-architect - Document analysis
Task 2: @code-reviewer - Code file analysis
Task 3: @devops-troubleshooter - Config analysis
Task 4: @ui-ux-designer - Media/asset analysis
Task 5: @full-stack-developer - Archive analysis
Task 6: @ai-engineer - RAG integration planning
```

**Output**:
```
File Organization Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total files: 1,247
Analyzed: 1,247 (100%)
Time: 45 seconds (6 parallel agents)

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Documents (347 files):
  ✅ Keep: 87 (important, recent)
  📚 RAG: 145 (add to collections)
  📦 Archive: 89 (old but keep)
  🗑️ Delete: 26 (duplicates, outdated)

Code (524 files):
  ✅ Keep: 498 (active code)
  📦 Archive: 18 (old versions)
  🗑️ Delete: 8 (generated, unused)

Config (147 files):
  ✅ Keep: 42 (active configs)
  🔀 Consolidate: 67 (merge duplicates)
  🗑️ Delete: 38 (backups, old)

Media (189 files):
  ✅ Keep: 124 (in use)
  💾 Compress: 41 (large files)
  🗑️ Delete: 24 (unused)

Archives (40 files):
  🗑️ Delete: 35 (safe to remove)
  ✅ Keep: 5 (important backups)

Token Impact:
  Current: 485,000 tokens (heavy file load)
  After cleanup: 45,000 tokens (90% reduction)
  Savings: 440,000 tokens per session
```

---

### clean
Execute recommended cleanup (with confirmation)

**Execution (6 Parallel Agents)**:
```bash
# Agent 1: Document cleanup
- Moves 145 docs to RAG indexing queue
- Archives 89 to .claude/archive/docs/
- Deletes 26 duplicates/outdated

# Agent 2: Code cleanup
- Archives 18 old versions to .claude/archive/code/
- Deletes 8 unused/generated files

# Agent 3: Config cleanup
- Consolidates 67 duplicate configs
- Deletes 38 old backups
- Updates .claudeignore

# Agent 4: Media cleanup
- Compresses 41 large images
- Deletes 24 unused assets
- Updates asset inventory

# Agent 5: Archive cleanup
- Deletes 35 safe-to-remove archives
- Preserves 5 important backups
- Reduces archive size by 95%

# Agent 6: RAG integration
- Indexes 145 docs to RAG collections
- Creates searchable index
- Archives originals
- Updates .claude/context/rag-collections.md
```

**Safety**:
```
Confirmation required before deleting:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Files to DELETE (131 total):
  Documents: 26 files (12.3 MB)
  Code: 8 files (2.1 MB)
  Config: 38 files (1.8 MB)
  Media: 24 files (15.7 MB)
  Archives: 35 files (89.4 MB)

Total to delete: 121.3 MB

Proceed? (yes/no/review)
```

---

### rag
Add documents to RAG collections (no deletion)

**Execution**:
```bash
# Analyzes docs, adds to RAG, archives originals
Agent 1-5: Identify important docs
Agent 6: Index to RAG + archive

Result:
  145 docs → RAG indexed
  Originals → .claude/archive/rag-indexed/
  Searchable via /knowledge query
  Token savings: ~8K tokens per doc query
```

---

### archive
Archive old files safely (no deletion)

**Execution**:
```bash
# Creates dated archive
.claude/archive/cleanup-2025-10-28.tar.gz

Includes:
  - Old docs (89 files)
  - Old code versions (18 files)
  - Old configs (38 files)
  - Unused media (24 files)

Can restore anytime:
tar -xzf .claude/archive/cleanup-2025-10-28.tar.gz
```

---

## Parallel Agent Strategy

### File Analysis Phase (6 Agents in Parallel)

```bash
# Launch 6 agents simultaneously
Task tool with 6 parallel agents:

Agent 1 (@docs-architect):
  Analyze: *.md, *.txt, *.pdf, *.docx
  Check: Last modified, size, references
  Classify: Keep, RAG, Archive, Delete

Agent 2 (@code-reviewer):
  Analyze: *.js, *.ts, *.py, *.java
  Check: Imports, usage, test coverage
  Classify: Keep, Archive, Delete

Agent 3 (@devops-troubleshooter):
  Analyze: *.json, *.yaml, *.env, .config
  Check: Active references, duplicates
  Classify: Keep, Consolidate, Delete

Agent 4 (@ui-ux-designer):
  Analyze: *.png, *.jpg, *.svg, *.pdf
  Check: Usage in code, size, duplicates
  Classify: Keep, Compress, Delete

Agent 5 (@full-stack-developer):
  Analyze: *.backup, *.old, archive/*
  Check: Age, importance, recoverability
  Classify: Delete, Keep

Agent 6 (@ai-engineer):
  Receive: Important docs from Agents 1-5
  Action: Index to RAG collections
  Update: .claude/context/rag-collections.md
```

**Time**: ~45 seconds (vs 5+ minutes sequential)
**Speedup**: 6-8x faster

---

### Cleanup Phase (6 Agents in Parallel)

```bash
Agent 1: Document cleanup
  - RAG indexing (145 docs)
  - Archiving (89 docs)
  - Deletion (26 docs)

Agent 2: Code cleanup
  - Archiving (18 files)
  - Deletion (8 files)

Agent 3: Config cleanup
  - Consolidation (67 configs)
  - Deletion (38 backups)

Agent 4: Media cleanup
  - Compression (41 images)
  - Deletion (24 unused)

Agent 5: Archive cleanup
  - Deletion (35 old archives)

Agent 6: Verification
  - Validates all changes
  - Updates .claudeignore
  - Generates report
```

**Time**: ~90 seconds (vs 10+ minutes sequential)

---

## Intelligent Decision Making

### RAG vs Delete Logic

**Add to RAG if**:
- ✅ Technical documentation (API refs, guides)
- ✅ Architectural decisions (ADRs, design docs)
- ✅ Important but rarely accessed
- ✅ >1KB and <100KB (sweet spot for RAG)

**Archive if**:
- ✅ Historical value but not searchable
- ✅ Legal/compliance need
- ✅ Large files (>100KB)

**Delete if**:
- ✅ Duplicates (exact copies)
- ✅ Outdated (>6 months, superseded)
- ✅ Temporary (*.tmp, *.backup, *.old)
- ✅ Generated (build outputs)
- ✅ No references (unreachable)

---

## Usage Examples

### Full Declutter (6 Parallel Agents)
```bash
/file-organizer clean

# Launches 6 agents in parallel
# Analyzes all files
# Shows recommendations
# Asks for confirmation
# Executes cleanup
# Generates report

Time: 2-3 minutes
Result: 90% token reduction
```

### Safe Analysis Only
```bash
/file-organizer analyze

# 6 agents analyze files
# Generates recommendations
# NO changes made
# Review before cleanup
```

### RAG Integration
```bash
/file-organizer rag

# Identifies important docs
# Adds to RAG collections
# Archives originals
# Updates search index

Result: 145 docs searchable via /knowledge
Saves: 8K tokens per doc query
```

### Archive Old Files
```bash
/file-organizer archive

# Creates dated .tar.gz
# Removes from workspace
# Restorable anytime

Result: Cleaner workspace
Backup: .claude/archive/cleanup-2025-10-28.tar.gz
```

---

## Pre-requisites (Auto-executed)

### Before Analysis
```bash
!git status  # Ensure clean working directory
!du -sh .    # Check current size
!find . -type f | wc -l  # Count files
```

### During Cleanup
```bash
# For each file to delete:
- Check if in git (preserve if tracked)
- Check if referenced (preserve if used)
- Check age (<7 days = recent, keep)
- Check size (>100MB = archive first)
```

---

## Safety Features

### Automatic Backups
```bash
# Before any deletion
.claude/archive/pre-cleanup-backup-2025-10-28.tar.gz

# Includes all files that will be deleted
# Restorable for 30 days
```

### Confirmation Prompts
```bash
Review recommendations:

Documents to DELETE (26 files, 12.3 MB):
  - old-design-v1.pdf (superseded by v4)
  - meeting-notes-2023-*.md (outdated)
  - duplicate-readme.md (exact copy)

Documents to RAG (145 files, 45.7 MB):
  - api-documentation.md (searchable)
  - architecture-decisions/*.md (reference)
  - user-guides/*.pdf (indexed)

Archives to DELETE (35 files, 89.4 MB):
  - backup-2023-*.tar.gz (>2 years old)
  - old-node-modules-*.zip (obsolete)

Proceed with:
1. Delete all (yes)
2. Delete specific categories (partial)
3. Review each file (review)
4. Cancel (no)
```

### Dry-Run Mode
```bash
/file-organizer clean --dry-run

# Shows what WOULD be done
# NO actual changes
# Perfect for testing
```

---

## Token Impact

### Before File Organization
```
Project with 1,247 files:
  - Documents: 347 files → 85,000 tokens
  - Code: 524 files → 120,000 tokens
  - Config: 147 files → 35,000 tokens
  - Media: 189 files → 195,000 tokens
  - Archives: 40 files → 50,000 tokens

Total: 485,000 tokens (exceeds limits frequently)
```

### After File Organization
```
Project with 387 files (69% reduction):
  - Documents: 87 files → 22,000 tokens
  - Code: 498 files → 115,000 tokens (cleaned)
  - Config: 42 files → 10,000 tokens
  - Media: 124 files → 95,000 tokens (compressed)
  - Archives: 0 files → 0 tokens (deleted)

Total: 45,000 tokens (90.7% reduction)
```

**Savings**: 440,000 tokens per session!

---

## Integration with /optimize-all

### Updated /optimize-all (Now Uses 6 Parallel Agents)

**Phase 1**: Structure Setup (1 agent)
- Creates .claude/ directories
- Deploys .claudeignore
- Sets up core files

**Phase 2**: File Analysis (6 agents in parallel)
```bash
/file-organizer analyze

Agent 1-6: Analyze all file types
Result: Recommendations in 45 seconds
```

**Phase 3**: Cleanup (6 agents in parallel)
```bash
/file-organizer clean

Agent 1-6: Execute cleanup concurrently
Result: 90% token reduction in 2 minutes
```

**Phase 4**: Optimization (2 agents in parallel)
```bash
Agent 1: Settings + agent configuration
Agent 2: ROADMAP + token tracker setup
```

**Phase 5**: Verification (1 agent)
- Validates all changes
- Generates report
- Updates documentation

**Total Time**: 5-7 minutes (vs 15+ minutes sequential)
**Speedup**: 2-3x faster

---

## Usage Workflow

### Step 1: Analyze
```bash
/file-organizer analyze

# 6 agents scan all files
# Generates recommendations
# Shows token impact
# NO changes yet
```

### Step 2: Review
```
# Review recommendations
# Adjust if needed
# Confirm categories
```

### Step 3: Execute
```bash
/file-organizer clean

# Confirms deletions
# Executes cleanup
# Updates RAG
# Archives important files
# Generates report
```

### Step 4: Verify
```bash
# Check token reduction
/session status

# Should show:
Tokens: 45K/1M (4.5%) ← Down from 485K (48.5%)
Savings: 440K tokens (90.7%)
```

---

## Smart Decluttering Rules

### Automatic Decisions (No Confirmation)

**Safe Deletes**:
- node_modules/ (if package.json exists - can restore)
- dist/, build/ (generated - can rebuild)
- .cache/, __pycache__/ (generated)
- *.log files >7 days old
- Exact duplicates (MD5 match)

**Auto-Archive**:
- Docs >6 months old but <2 years
- Config backups (*.json.backup)
- Old screenshots/images unused

**Auto-RAG**:
- Technical documentation (.md files >1KB)
- API specifications (swagger, openapi)
- Architecture decision records (ADR)
- Important PDFs (guides, references)

### Requires Confirmation

**Delete**:
- Files >100MB (show size impact)
- Files in git history
- Files referenced in code
- Recently modified (<7 days)

**RAG Index**:
- Files >100KB (large docs)
- Binary files (PDFs need OCR)
- Non-technical content

---

## Post-Cleanup Benefits

### Token Efficiency
```
Before: 485,000 tokens
After: 45,000 tokens
Savings: 440,000 tokens (90.7%)

Impact:
- Faster session loads (10x)
- More working space (440K tokens freed)
- Better context (no noise)
- Cheaper API costs (90% less)
```

### File Organization
```
Before: 1,247 files (cluttered)
After: 387 files (organized)

Structure:
├── Active code (clean)
├── Important docs (RAG-indexed)
├── Archives (.claude/archive/)
└── .claudeignore (protects from future bloat)
```

### Productivity
```
Before: 15 min to find files
After: 2 min to find files
Savings: 13 min per lookup

Search improvement:
- RAG query finds docs instantly
- No wading through duplicates
- Clear file structure
```

---

## Example: Full Project Declutter

```bash
cd projects/erpagpt

# Step 1: Analyze
/file-organizer analyze

# 6 agents analyze in parallel (45 sec)
# Output: Recommendations

# Step 2: Execute
/file-organizer clean

# Confirmation:
Delete 35 old archives (89 MB)?
RAG index 45 docs (12 MB)?
Archive 67 old configs (3 MB)?

yes

# Execution (2 min with 6 agents):
[Agent 1] RAG indexing 45 docs... Done
[Agent 2] Archiving code... Done
[Agent 3] Consolidating configs... Done
[Agent 4] Compressing media... Done
[Agent 5] Deleting archives... Done
[Agent 6] Updating indexes... Done

Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Files: 847 → 312 (63% reduction)
Size: 243 MB → 45 MB (81% reduction)
Tokens: 312,000 → 38,000 (88% reduction)

ERPAGPT plans: 100% PRESERVED
- PROJECT-TRACKER.md intact
- ROADMAP.md intact
- AGENT-ROUTING-RULES.md intact
```

---

## Session State Files

After file organization:

```json
// .claude/context/file-organization-state.json
{
  "last_cleanup": "2025-10-28T23:30:00Z",
  "files_before": 1247,
  "files_after": 387,
  "reduction": "69%",
  "token_savings": 440000,
  "rag_indexed": 145,
  "archived": 156,
  "deleted": 131,
  "next_cleanup_due": "2025-11-28"
}
```

---

## Usage:
```
/file-organizer analyze     # Scan and recommend
/file-organizer clean       # Execute cleanup
/file-organizer rag         # Add docs to RAG
/file-organizer archive     # Archive old files
```

## Auto-Detection:
If no action specified, defaults to "analyze" (safe, no changes)

## Files Created:
- `.claude/archive/` - Archived files
- `.claude/context/file-organization-state.json` - Cleanup tracking
- `.claude/context/rag-collections.md` - RAG indexed docs
- `.claude/archive/pre-cleanup-backup.tar.gz` - Safety backup
