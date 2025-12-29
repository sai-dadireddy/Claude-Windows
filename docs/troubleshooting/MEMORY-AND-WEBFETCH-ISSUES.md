# Memory System & WebFetch Issues - Troubleshooting Guide

**Date**: 2025-10-17
**Issues Identified**: Project-based memory storage failures, WebFetch not auto-falling back to Playwright

---

## Issue 1: Project Not Found in Auto Memory

### Problem Statement
When attempting to store memories using `mcp__memory-auto__store_project_memory` with project name "aws-chatbot", the memory system returns:

```
❌ Project not found: 'aws-chatbot'
```

Even though the project exists in the filesystem at `C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\projects\aws-chatbot\`.

### Root Cause Analysis

**Verified Facts:**
1. ✅ Project directory exists in filesystem
2. ✅ Global memory storage works perfectly
3. ❌ Project "aws-chatbot" NOT registered in memory system
4. ✅ Only 7 projects registered (list from `list_projects`):
   - PeopleSoft-RAG
   - active-genie-nginx
   - aarp
   - smart-mcp
   - langchain-learning
   - claude-productivity-tools
   - claude-global-config

**Root Cause:**
The memory system maintains a separate registry of projects in `PROJECTS_INDEX` database. This is NOT automatically synced with the filesystem directory structure.

### Current Workaround (What Works)

**Use Global Memory Instead:**
```python
mcp__memory-auto__store_global_memory({
    "entity_name": "AWS Multi-Agent RAG Chatbot - Feature Name",
    "entity_type": "feature",
    "content": "...",
    "importance": 3,
    "tags": "aws-chatbot, tag2, tag3"
})
```

**Pros:**
- ✅ Works reliably
- ✅ Searchable via `search_global_memory`
- ✅ Can tag with project name for filtering
- ✅ No project registration required

**Cons:**
- ❌ Not isolated to project (global namespace)
- ❌ No automatic project context
- ❌ Manual tagging required

### Retrieval Pattern (Best Practice)

**Search by Tags:**
```python
# Search specifically for aws-chatbot content
mcp__memory-auto__search_global_memory({
    "query": "aws-chatbot presentation multi-agent",
    "limit": 10
})

# Search by specific feature
mcp__memory-auto__search_global_memory({
    "query": "ERPA AWS Multi-Agent",
    "limit": 10
})
```

**Results:**
- ✅ Successfully retrieved 3 stored memories for aws-chatbot
- ✅ Proper filtering by entity name and tags
- ✅ Importance-based ranking (3⭐ = high priority)

### Potential Solutions (For Future Implementation)

**Option 1: Register Project in Memory System**
```python
# Hypothetical - if project registration API exists
mcp__memory-auto__register_project({
    "project_id": "aws-chatbot",
    "project_name": "AWS Multi-Agent RAG Chatbot",
    "path": "C:\\Users\\...\\projects\\aws-chatbot",
    "status": "active"
})
```

**Status**: API not currently exposed, would require memory server enhancement

**Option 2: Auto-Register on First Project Memory Store**
- Memory server could auto-create project entry if directory exists
- Would require checking filesystem on each store operation
- Performance impact unclear

**Option 3: Claude Code Project Sync**
- Add global instruction to auto-register projects
- Run on session start or when switching projects
- Would maintain registry automatically

### Recommendations

**Immediate (Current Sessions):**
1. ✅ Use `store_global_memory` for all aws-chatbot content
2. ✅ Tag with "aws-chatbot" for filtering
3. ✅ Use descriptive entity names for searchability
4. ✅ Set `importance: 3` for critical information

**Long-term (System Enhancement):**
1. Investigate memory server source code
2. Request project auto-registration feature
3. Add project sync to global instructions
4. Consider filesystem-backed project discovery

---

## Issue 2: WebFetch Didn't Auto-Fallback to Playwright

### Problem Statement
When WebFetch failed on www.wired.com (Imprompter article), Claude did not automatically attempt to use Playwright as a fallback, despite having Playwright available and working.

**Error Received:**
```
<error>Claude Code is unable to fetch from www.wired.com</error>
```

**User's Correct Observation:**
> "question if you are unable to do webfecth why you didnt use playwright"

### Root Cause Analysis

**What Happened:**
1. ❌ WebFetch attempted www.wired.com
2. ❌ WebFetch failed (likely blocked by Cloudflare/privacy modals)
3. ❌ Claude did NOT automatically try Playwright
4. ✅ When user pointed it out, Claude attempted Playwright
5. ❌ Playwright also failed (privacy modals blocking content)
6. ✅ Fallback to WebSearch succeeded (found research paper + analysis)

**Why This Occurred:**

**Reason 1: Tool Selection Logic**
Claude's tool selection is based on:
- User's explicit request
- Task requirements
- Tool availability
- **NOT automatic fallback chains**

There is no built-in rule: "If WebFetch fails, automatically try Playwright"

**Reason 2: Global Instructions**
While we have:
- `auto-web-fetch-orchestration.md` (smart web fetching)
- `auto-playwright-web-access.md` (Playwright awareness)

These do NOT specify automatic fallback behavior when WebFetch fails.

**Reason 3: Error Handling**
WebFetch failure returns an error, but Claude treats it as:
- "This specific tool doesn't work for this URL"
- NOT: "Try alternative web access methods"

### Current Workflow (Manual Fallback)

**What Happened This Session:**
1. WebFetch failed → Error returned
2. User intervention → Suggested Playwright
3. Claude attempted Playwright → Also failed (privacy modal)
4. Claude pivoted → WebSearch (successful)

**Issue**: Required user intervention to suggest Playwright

### Correct Behavior (What Should Happen)

**Automatic Fallback Chain:**
```
User Request: "Fetch content from www.wired.com/article"
↓
Step 1: Try WebFetch
├─ Success → Return content
└─ Failure → Log reason, proceed to Step 2

Step 2: Try Playwright (browser automation)
├─ Success → Return content
├─ Partial (privacy modal) → Extract what's available OR proceed to Step 3
└─ Failure → Log reason, proceed to Step 3

Step 3: Try WebSearch (as research fallback)
├─ Success → Return search results + analysis
└─ Failure → Inform user, suggest manual access
```

### Solution: Enhanced Global Instructions

**Create New File:** `global-instructions/auto-web-access-fallback.md`

```markdown
# Auto Web Access Fallback Chain

When fetching web content, ALWAYS follow this fallback order:

## Primary: WebFetch
Use WebFetch first for standard web pages.

## Fallback 1: Playwright (If WebFetch Fails)
If WebFetch returns error, IMMEDIATELY attempt Playwright:
- Navigate to URL
- Wait for page load
- Extract visible HTML/text
- Take screenshot if helpful

## Fallback 2: WebSearch (If Playwright Fails)
If Playwright also fails (privacy modals, Cloudflare, etc.):
- Use WebSearch with specific query
- Look for alternative sources (research papers, analysis, summaries)
- Combine multiple search results for comprehensive answer

## Implementation
NEVER stop after first tool failure. ALWAYS try all three methods before informing user of complete failure.

**Example:**
User: "Fetch article from www.wired.com/imprompter-attack"

Attempt 1: WebFetch → ❌ Blocked
Attempt 2: Playwright → ❌ Privacy modal
Attempt 3: WebSearch "Imprompter attack research paper 2024" → ✅ Found arxiv.org + analysis

Return: Combined information from successful method
```

**Include in CLAUDE.md:**
```markdown
## Auto Web Access Fallback (CRITICAL - ALWAYS ENFORCE)
{{include: global-instructions/auto-web-access-fallback.md}}
```

### Testing the Fix

**Test Case 1: Blocked Website**
```
User: "Fetch content from www.wired.com/some-article"

Expected:
1. Try WebFetch → Fail
2. Try Playwright → Attempt
3. Try WebSearch → Success
4. Return combined results WITHOUT user intervention
```

**Test Case 2: Cloudflare Protected**
```
User: "Fetch pricing from www.some-saas-site.com/pricing"

Expected:
1. Try WebFetch → Cloudflare block
2. Try Playwright → Success (JS rendering bypasses)
3. Return pricing information
```

**Test Case 3: Complete Failure**
```
User: "Fetch content from internal-intranet.erpa.edu"

Expected:
1. Try WebFetch → Network unreachable
2. Try Playwright → Network unreachable
3. Try WebSearch → No public results
4. Inform user: "Cannot access internal site, requires VPN/authentication"
```

### Recommendations

**Immediate Actions:**
1. ✅ Create `auto-web-access-fallback.md` global instruction
2. ✅ Add to CLAUDE.md include list
3. ✅ Test with known problematic URLs
4. ✅ Document in session notes for future reference

**Long-term Enhancements:**
1. Add retry logic with exponential backoff
2. Cache successful method per domain (e.g., "wired.com always needs Playwright")
3. Detect Cloudflare/bot protection and skip straight to Playwright
4. Parallel attempts (WebFetch + Playwright simultaneously, use fastest)

---

## Summary of Findings

### Issue 1: Project Memory
**Status**: ✅ WORKAROUND AVAILABLE
**Solution**: Use `store_global_memory` with project tags
**Next Steps**: Request project auto-registration feature

### Issue 2: WebFetch Fallback
**Status**: ⚠️ BEHAVIOR GAP IDENTIFIED
**Solution**: Add auto-fallback global instruction
**Next Steps**: Create fallback chain instruction file

### Impact Assessment
- **Issue 1**: Low impact (workaround is reliable)
- **Issue 2**: Medium impact (required user intervention, reduces autonomy)

### Priority
1. **High**: Implement WebFetch fallback chain (improves autonomy)
2. **Medium**: Document project memory workaround (already functional)
3. **Low**: Request memory server enhancement (long-term improvement)

---

## Appendix: Memory System Deep Dive

### How Memory System Works

**Architecture:**
```
Global Memory (SQLite)
├── memories table
│   ├── id (primary key)
│   ├── entity_name
│   ├── entity_type
│   ├── content (full text)
│   ├── importance (0-3)
│   ├── tags (comma-separated)
│   └── created_at
└── Full-text search index

Projects Index (SQLite)
├── projects table
│   ├── project_id (primary key)
│   ├── project_name
│   ├── status (active/archived)
│   └── updated_at
└── Project-specific memories (separate table)
```

**Storage Locations:**
- Global DB: `C:\Users\...\OneDrive - ERPA\Claude\projects\unified-memory\databases\global.db`
- Projects Index: `C:\Users\...\OneDrive - ERPA\Claude\projects\unified-memory\databases\projects-index.db`

### Search Behavior

**Global Search:**
- Uses full-text search on `content` field
- Filters by tags (optional)
- Ranks by importance (3⭐ highest)
- Returns up to `limit` results

**Project Search:**
- Requires project to exist in projects table
- Searches within project-specific memories only
- Same ranking algorithm as global

### Auto-Classification

**AUTO_CLASSIFY=true** (enabled in config):
- Analyzes content to determine entity_type
- Suggests appropriate tags
- Sets importance based on content criticality

**Current Session Results:**
- ✅ Auto-classified as "feature" (correct)
- ✅ Auto-tagged with relevant keywords
- ✅ Set importance to 3 (high priority content)

---

## End of Document

**Last Updated**: 2025-10-17
**Issues**: 2 identified, 1 workaround, 1 solution pending
**Next Review**: After implementing WebFetch fallback chain
