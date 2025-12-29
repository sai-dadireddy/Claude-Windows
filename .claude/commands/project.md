# Smart Project Switcher

**Usage**: `/project <project-name>`

**Examples**:
- `/project active-genie-nginx`
- `/project PeopleSoft-RAG`
- `/project aarp`

**Purpose**: Intelligently switch to a project and auto-setup missing infrastructure

---

## What This Does

<task>
Switch to project, check for essential infrastructure (memory, vectors, documentation),
and auto-implement anything missing. Smart detection and setup.
</task>

---

## Execution Sequence

<sequence>

### Step 1: Navigate to Project
```
Action: Change working directory to project
Path: claude/projects/<project-name>

If not found:
  - Search for project in known locations
  - Ask user for path
  - Create new project if requested
```

### Step 2: Quick Project Scan (Parallel)
```
Check simultaneously:
✓ README.md exists?
✓ CLAUDE.md or .claude-project.md exists?
✓ package.json / requirements.txt / go.mod exists?
✓ .git directory exists?
✓ Tests directory exists?
```

### Step 2.5: Load Important Project Files (NEW!)
```
Read key files in parallel (if they exist):

1. README.md
   Purpose: Project overview, goals, setup instructions
   Display: First 50 lines or key sections

2. CLAUDE.md or .claude-project.md
   Purpose: Project-specific Claude instructions
   Display: Full content (project overrides)

3. package.json OR requirements.txt OR go.mod
   Purpose: Tech stack, dependencies, scripts
   Extract:
   - Project name
   - Version
   - Main dependencies
   - Available scripts/commands

4. .gitignore (first 20 lines)
   Purpose: Understand what's excluded
   Quick scan for important patterns

5. CONTRIBUTING.md (if exists)
   Purpose: Development guidelines
   Display: Key sections

Time: <3 seconds (parallel reads)
Benefit: Full project context loaded immediately!

**Display after loading:**
```

📖 **Project Files Loaded:**

README.md:
  Project: [name from README]
  Description: [first paragraph]
  Setup: [key command s if listed]

Tech Stack (from package.json):
  Name: [project name]
  Version: [version]
  Main deps: [top 3-5 dependencies]
  Scripts: [list npm scripts]

Claude Config (CLAUDE.md):
  ✅ Project-specific instructions found
  Key overrides: [list main sections]
  OR
  ❌ No project-specific Claude instructions

**Context Summary:**
- Project type: [detected]
- Language: [TypeScript/Python/Go/etc]
- Framework: [Angular/React/FastAPI/etc]
- Key commands: [npm start, npm test, etc]
```

This gives you FULL context immediately! 🎯
```

### Step 3: Memory System Check
```
Tool: memory-auto → search_project_memory(project-name)

If no memory found:
  ❌ Memory: Not initialized
  Action: Create first memory entry

If memory exists:
  ✅ Memory: X entries found
  Display: Last activity, recent decisions
```

### Step 4: Vector Store Check
```
Tool: langchain → semantic_search(project_name)

If no vectors:
  ❌ Vectors: Not indexed
  Action: Offer to index project docs

If vectors exist:
  ✅ Vectors: Y documents indexed
  Check: Last indexed date
```

### Step 5: Auto-Implementation (Missing Features)

**If Memory Missing:**
```
🔧 Setting up memory system for <project-name>...

Action:
1. Create memory entry: "Project initialized on [date]"
2. Store project type: [detected from files]
3. Store tech stack: [from package.json etc]

✅ Memory initialized!
💡 Tip: I'll auto-store decisions as we work
```

**If Vectors Missing:**
```
🔧 No vector index found. Want me to index your docs?

If user says yes:
  Tool: langchain → index_directory()
  Patterns: ["*.md", "README*", "*.txt"]

  Progress:
  📄 Indexing README.md...
  📄 Indexing docs/*.md...
  📄 Indexing API docs...

  ✅ Indexed Z documents!
  💡 Now you can semantic search your project
```

**If Documentation Missing:**
```
❌ No README.md or CLAUDE.md found

Action: Offer to create basic project documentation
- README.md: Project overview, setup, usage
- CLAUDE.md: Project-specific Claude instructions
```

**If Tests Missing:**
```
❌ No tests directory found

Action: Offer to set up testing framework
- Detect language (TS/JS/Python/Go)
- Suggest appropriate framework (Jest/pytest/etc)
- Create basic test structure
```

### Step 6: Git Integration Check
```
If .git exists:
  ✅ Git: Initialized
  Show: Current branch, last commit, uncommitted changes

If no .git:
  ❌ Git: Not initialized
  Action: Offer to initialize repo
```

### Step 7: Project Context Summary (Enhanced with File Content!)
```
Display comprehensive project state:

📂 **Project: <project-name>**
📍 Path: <full-path>
🏷️ Type: [Web App / API / Library / Tool]
⚙️ Stack: [TypeScript/Angular / Python/FastAPI / etc]

📚 **Files Loaded:**
✅ README.md - [brief description from file]
✅ package.json - [name, version, main deps]
✅ CLAUDE.md - [project-specific instructions]
✅ .gitignore - [key patterns]

🏗️ **Infrastructure Status:**
✅ Memory: X entries, last: [date]
✅ Vectors: Y docs indexed, last: [date]
✅ Git: Branch [name], [clean/dirty]
✅ Tests: [framework] configured

📝 **Project Overview (from README):**
[First 2-3 sentences from README describing the project]

🛠️ **Available Commands (from package.json):**
- npm start → [description from scripts]
- npm test → [description from scripts]
- npm build → [description from scripts]
- [other key scripts]

📋 **Recent Activity (from memory):**
- [Last decision from memory]
- [Last commit message]
- [Last worked: date]

💡 **Project-Specific Notes (from CLAUDE.md):**
- [Key instruction #1]
- [Key instruction #2]
- [Special workflows or patterns]

🎯 **Ready to work!** Full context loaded. What should we tackle?

**Pro Tip**: All project details are now in my context - ask me anything about setup, dependencies, or workflows!
```

</sequence>

---

## Auto-Implementation Logic

### Decision Tree

```
For each missing feature:

Memory Missing?
  → Priority: HIGH
  → Auto-create: YES (just one entry)
  → Time: <5 seconds

Vectors Missing?
  → Priority: MEDIUM
  → Auto-create: ASK FIRST (might be large)
  → Time: 10-60 seconds depending on size

Documentation Missing?
  → Priority: MEDIUM
  → Auto-create: ASK FIRST
  → Time: 30-120 seconds

Tests Missing?
  → Priority: LOW
  → Auto-create: SUGGEST ONLY
  → Time: N/A (user decides)

Git Missing?
  → Priority: MEDIUM
  → Auto-create: ASK FIRST
  → Time: <5 seconds
```

---

## Smart Defaults

### Auto-Detect Project Type

```yaml
If finds package.json + Angular:
  Type: "Angular Web Application"
  Stack: "TypeScript, Angular, RxJS"
  Suggest: Component testing with Jest

If finds requirements.txt + FastAPI:
  Type: "Python API"
  Stack: "Python, FastAPI, Pydantic"
  Suggest: API testing with pytest

If finds go.mod:
  Type: "Go Application"
  Stack: "Go, [detected modules]"
  Suggest: Testing with built-in testing package
```

### Auto-Configure Based on Type

```yaml
For Web App:
  Index: *.md, *.ts, *.html, *.css
  Memory: UI decisions, component patterns
  Tests: Unit + E2E

For API:
  Index: *.md, *.py, *.yaml (OpenAPI)
  Memory: Endpoint decisions, data models
  Tests: Unit + Integration

For Library:
  Index: *.md, README, examples
  Memory: API design decisions
  Tests: Unit + Usage examples
```

---

## Entertainment During Setup

### While Indexing Documents:
```
📊 Indexing your docs...

💡 Did you know? Vector embeddings convert your docs into
math so AI can understand them. It's like giving me glasses
to read your code! 👓

⏳ Processing... (10 files done)

🤓 Fun fact: The average technical doc is 80% examples,
20% explanation. Yours looks well-documented!

✅ Done! 25 documents now searchable.
```

### While Creating Memory Entries:
```
🧠 Setting up project memory...

📝 Pro tip: I'll auto-store your decisions as we work.
Think of me as your project historian! 📚

✅ Memory initialized! First entry created.

💪 Motivational moment: "The best way to predict the
future is to create it." - Peter Drucker

Let's build something awesome!
```

---

## Project Templates (Future Enhancement)

```
Optional: /project <name> --template <type>

Templates:
- web-app: Full web app setup (Next.js/Angular/React)
- api: REST/GraphQL API setup
- cli: Command-line tool setup
- library: Reusable library setup
- ml: Machine learning project setup

Auto-creates:
- Proper folder structure
- Essential configs
- Testing setup
- Documentation templates
- Memory + vector setup
```

---

## Quick Project Switching

```
User: /project active-genie-nginx

Claude:
🔄 Switching to active-genie-nginx...

✓ Found project at: claude/projects/active-genie-nginx
✓ Memory loaded: 23 entries, last: 2025-10-10
✓ Vectors ready: 45 docs indexed
✓ Git: branch 'master', 3 uncommitted changes
✓ Stack: TypeScript, Angular 20, Nginx

📌 Last decision: "Upgraded Angular 8→20, fixed CORS issues"

🎯 Ready! What's next for active-genie-nginx?

---

User: /project PeopleSoft-RAG

Claude:
🔄 Switching to PeopleSoft-RAG...

✓ Found project
❌ No memory entries found
❌ No vector index found

🔧 Auto-setup initiated...
  ✓ Created memory entry (Project: PeopleSoft-RAG initialized)
  📊 Indexing docs... (found 12 .md files)
  ✓ Vector index created: 12 documents

📌 New project setup complete!

🎯 Fresh start! What should we build?
```

---

## Error Handling

### Project Not Found
```
❌ Project "xyz" not found

Searching in:
- claude/projects/xyz
- ./xyz
- ../xyz

🔍 Did you mean:
1. active-genie-nginx
2. PeopleSoft-RAG
3. aarp

Or create new project? (yes/no)
```

### Permission Issues
```
❌ Cannot access project directory

Possible issues:
- OneDrive sync pending
- Folder permissions
- Path doesn't exist

💡 Tip: Check if folder exists and is accessible
```

---

## Success Criteria

- ✅ Project switched in <5 seconds
- ✅ All checks completed (memory, vectors, git, docs)
- ✅ Missing features auto-detected
- ✅ User offered solutions (not auto-forced)
- ✅ Clear project state summary presented
- ✅ Ready to work immediately

---

## Performance Optimization

**Parallel Checks**: All 7 checks run simultaneously = 3-5 seconds total
**Smart Caching**: Project state cached for session
**Lazy Loading**: Heavy operations (indexing) only if needed

---

**Time Saved**: Manual project setup = 10-15 minutes
With `/project`: 5-10 seconds + auto-setup of missing features! ⚡

---

**Pro Tip**: Combine with `/load-global` at startup:
```
/load-global
/project active-genie-nginx
```
Total startup time: <10 seconds, fully configured! 🚀
