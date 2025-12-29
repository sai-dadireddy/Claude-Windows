---
description: Complete project optimization with 6 parallel agents - structure, RAG, cleanup, token efficiency
argument-hint: [project-path]
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
model: sonnet
---

# Complete Project Optimization (6 Parallel Agents)

Target: $ARGUMENTS (defaults to current project)

## Parallel Agent Execution Strategy

### Phase 1: Analysis (6 Agents - 45 seconds)
```
Agent 1 (@docs-architect): Document analysis
Agent 2 (@code-reviewer): Code file analysis
Agent 3 (@devops-troubleshooter): Config analysis
Agent 4 (@ui-ux-designer): Media/asset analysis
Agent 5 (@full-stack-developer): Archive analysis
Agent 6 (@ai-engineer): RAG integration planning

Time: 45 seconds (vs 5+ minutes sequential)
Speedup: 6-8x faster
```

### Phase 2: Cleanup (6 Agents - 2 minutes)
```
Agent 1: Document cleanup + RAG indexing
Agent 2: Code optimization + archiving
Agent 3: Config consolidation
Agent 4: Media compression
Agent 5: Archive deletion
Agent 6: Verification + reporting

Time: 2 minutes (vs 10+ minutes sequential)
Speedup: 5x faster
```

### Phase 3: Configuration (2 Agents - 1 minute)
```
Agent 1: Settings + agents + commands
Agent 2: ROADMAP + token tracker + structure

Time: 1 minute (parallel setup)
```

**Total Time**: ~4 minutes (vs 15+ sequential)
**Overall Speedup**: 3-4x faster

## What This Does (All-in-One)

### 1. Project Structure Analysis
✅ Scans current folder structure
✅ Identifies optimization opportunities
✅ Compares against optimal template

### 2. Token Protection
✅ Creates/updates .claudeignore (saves 100K+ tokens)
✅ Blocks node_modules/, dist/, build/, .cache/
✅ Adds OS files, logs, sensitive files

### 3. File Organization
✅ Creates .claude/ directory structure
✅ Separates core (CLAUDE.md) from context files
✅ Moves detailed docs to .claude/context/
✅ Deletes duplicate/outdated files

### 4. ROADMAP.md Setup
✅ Creates ROADMAP.md if missing
✅ Migrates existing tasks
✅ Adds cleanup rules (max 5 completed items)
✅ Archives old completed tasks

### 5. Settings Optimization
✅ Creates .claude/settings.json (500 tokens)
✅ Disables built-in agents
✅ Enables token monitoring
✅ Adds agent enforcement rules

### 6. Context Files
✅ Creates .claude/context/ directory
✅ Moves architecture docs there
✅ Creates api-spec.md if API exists
✅ Creates conventions.md for code standards
✅ Creates token-tracker.json

### 7. Agent Setup
✅ Identifies which agents needed for project
✅ Copies relevant agents from root
✅ Creates agent enforcement rules in CLAUDE.md

### 8. Command Setup
✅ Copies mega-commands from root
✅ Creates project-specific commands if needed
✅ Archives old redundant commands

### 9. Skills Activation
✅ Identifies which skills useful for project
✅ Documents skill triggers in CLAUDE.md

### 10. MCP Configuration
✅ Determines optimal MCP profile (minimal/dev/aws-work)
✅ Configures MCPs for project needs
✅ Documents in .claude/settings.json

### 11. RAG Integration (if applicable)
✅ Checks for RAG documentation collections
✅ Adds RAG query instructions to CLAUDE.md
✅ Creates .claude/context/rag-collections.md

### 12. Cleanup & Validation
✅ Removes duplicate files
✅ Archives old documentation
✅ Validates .gitignore includes .claude/epics/
✅ Checks for common token bloat sources
✅ Reports savings and improvements

---

## Execution Plan

### Pre-Flight Checks
```bash
!git status
```
Ensures clean working directory

### Phase 1: Analysis (1 min)
1. Scan project structure
2. Identify file types, sizes
3. Find optimization opportunities
4. Report findings

### Phase 2: Structure (2 min)
1. Create .claude/ directories
2. Create .claudeignore
3. Move docs to context/
4. Create ROADMAP.md

### Phase 3: Configuration (2 min)
1. Create/update settings.json
2. Set up token-tracker.json
3. Configure agent rules
4. Set up MCP profile

### Phase 4: Cleanup (1 min)
1. Archive old files
2. Remove duplicates
3. Update .gitignore
4. Validate structure

### Phase 5: Verification (1 min)
1. Check .claudeignore working
2. Verify CLAUDE.md < 300 tokens
3. Confirm ROADMAP.md created
4. Test token reduction

**Total Time**: ~7 minutes

---

## Usage Examples

### Basic Usage
```bash
/optimize-all
```
Optimizes current project directory

### Specific Project
```bash
/optimize-all C:/path/to/project
```

### With Options
```bash
/optimize-all --full
```
Includes deep analysis and aggressive cleanup

---

## Before/After Report

Automatically generates report showing:

```markdown
## Optimization Report: [Project Name]

### Token Savings
Before: 205,000 tokens
After: 1,400 tokens
Saved: 203,600 tokens (99.3% reduction)

### Files Optimized
- Created .claudeignore (blocks 150K tokens)
- Split CLAUDE.md (5,000 → 300 tokens)
- Archived 47 files
- Deleted 12 duplicates
- Organized 8 context files

### Structure Created
✅ .claude/CLAUDE.md (300 tokens)
✅ .claude/ROADMAP.md (200 tokens)
✅ .claude/context/ (3 files, load on demand)
✅ .claude/settings.json (500 tokens)
✅ .claudeignore (critical)

### Agent Configuration
✅ 5 agents configured for project
✅ Enforcement rules added
✅ Keyword triggers set

### Next Steps
1. Review CLAUDE.md and customize
2. Add current tasks to ROADMAP.md
3. Start working - all optimizations active!
```

---

## Safety Features

### Backup Before Changes
```bash
# Auto-creates backup
.claude/backups/pre-optimization-2025-10-28/
```

### Dry-Run Mode
```bash
/optimize-all --dry-run
```
Shows what would be changed without making changes

### Selective Optimization
```bash
/optimize-all --only structure,cleanup
```
Run only specific phases

---

## Integration with Other Commands

### Combines
- `/optimize tokens` - Token optimization
- `/optimize code` - Code structure
- File organization best practices
- Agent setup automation
- Settings configuration
- Cleanup operations

### One Command to Rule Them All
Instead of running 10+ separate commands, run one:
```bash
/optimize-all
```

**Result**: Complete project optimization in 7 minutes

---

## Post-Optimization Checklist

Automatically verifies:
- [x] .claudeignore exists and working
- [x] CLAUDE.md under 300 tokens
- [x] ROADMAP.md created
- [x] Context files separated
- [x] Settings optimized
- [x] Agent rules enforced
- [x] Token tracker configured
- [x] Backup created
- [x] .gitignore updated
- [x] No duplicate files

---

## Usage Frequency

**New project**: Run once during setup
**Existing project**: Run quarterly or when:
- Project feels slow/bloated
- Token usage high
- Files disorganized
- Need fresh start

---

**Token Cost**: ~50 tokens (command activation)
**Time**: 7 minutes automated
**Savings**: 200K+ tokens typically
**ROI**: 4,000:1 (token savings vs cost)
