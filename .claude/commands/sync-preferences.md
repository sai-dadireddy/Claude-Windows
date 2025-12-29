Sync your **claude.ai preferences and memory** to Claude Code's local memory system.

## Why This Exists

Claude Code and claude.ai don't share memory (yet - see issue #14228). This command bridges that gap manually.

## How to Use

### Step 1: Export from claude.ai

Go to claude.ai → Settings → scroll to "Claude's Memory" section, then:

1. Click "Manage Memory" or view your saved preferences
2. Copy all the memory items/preferences shown
3. Paste them below when prompted

### Step 2: Paste Your Preferences

Paste your claude.ai memory content here. Format can be:
- Raw text from the memory panel
- Bullet points
- Key-value pairs

Example input:
```
- Prefers TypeScript over JavaScript
- Uses Vim keybindings
- Working on project called "ActiveGenie"
- Likes concise responses without fluff
- Senior developer, 10+ years experience
- Timezone: PST
```

### Step 3: Parse and Save

I'll parse your preferences into categories:

```markdown
## Parsed Preferences

### Communication Style
- [Extracted preferences about how you like responses]

### Technical Preferences
- [Languages, frameworks, tools you prefer]

### Work Context
- [Projects, role, experience level]

### Personal
- [Name, timezone, other personal context]
```

### Step 4: Confirm and Save

After review, I'll save to:
- `~/.claude/memory/long-term/global/preferences.md` - Communication/personal prefs
- `~/.claude/memory/long-term/global/technical.md` - Tech stack preferences
- Semantic memory database for search

## What Gets Synced

| From claude.ai | To Claude Code |
|----------------|----------------|
| Communication preferences | `preferences.md` |
| Technical stack choices | `technical.md` |
| Project context | Project-specific memory |
| Personal info (name, role) | `preferences.md` |

## Reverse Sync (Claude Code → claude.ai)

To sync learnings BACK to claude.ai:
1. Run `/memory-status` to see what Claude Code has learned
2. Copy relevant items
3. Paste into claude.ai conversation: "Please remember: [items]"

## Automatic Updates

After initial sync, important preferences are auto-captured by the `auto_capture_memory.py` hook when you:
- Make technology decisions
- Express preferences
- Correct Claude's behavior

---

**Paste your claude.ai memory/preferences below:**

$ARGUMENTS
