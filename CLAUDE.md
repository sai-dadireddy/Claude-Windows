# Claude Manual Mode (Ultra-Minimal)

**Target**: ≤300 tokens | **Efficiency**: 98%

---

## Core Awareness (No Auto-Enforcement)

1. **RAG-First** - Query before reading
2. **PROJECT-TRACKER.md** - Single source of truth  
3. **Manual Commands** - Use `/command` explicitly

---

## Available Commands

**Session**: `/resume` `/session-save` `/status`
**Work**: `/plan` `/optimize` `/rag`
**Advanced**: `/spawn` `/mcp` `/consult`
**Memory**: `/memory`

---

## Rules

✅ Load ONLY when needed
✅ Use commands explicitly
✅ Query memory automatically
❌ NO auto-enforcement
❌ NO pre-loading

---

**Token Cost**: ~300 tokens (vs 2-3K LITE, 15-20K FULL)
**Resume**: Use `/resume` → 3.5-4.5K total
**Efficiency**: 98% (vs 30-40% before)
