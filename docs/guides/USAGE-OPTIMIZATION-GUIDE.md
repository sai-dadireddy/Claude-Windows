# Claude Code Usage Optimization Guide
**For Max 5x Plan ($100/month)**

---

## 🎯 Goal: Stay Under Weekly Limits

**Your Plan**:
- Max 5x = $100/month
- ~2 hours intensive Opus usage
- Good Sonnet 4.5 allocation
- Weekly reset every 7 days

**Problem Identified**:
- Global instructions: 19,474 lines (47 files)
- ~15-20K tokens loaded at EVERY session start
- 10% of context window used before you begin

---

## 🚀 Immediate Actions (Do This Now)

### 1. Switch to CLAUDE-LITE.md for Most Work

**Instead of opening with full CLAUDE.md:**
```bash
# In Claude Code settings, change:
Project Instructions: CLAUDE-LITE.md (not CLAUDE.md)
```

**Savings**: 85% reduction in startup tokens (15K → 2K)

---

### 2. Use Slash Commands to Monitor Usage

```bash
/usage          # Check current usage and reset times
/compact        # Compress conversation (use every 10 messages)
/clear          # Start fresh session (use when switching projects)
```

**When to use /compact**:
- After 10+ messages
- Before starting new task
- When context feels "heavy"

**When to use /clear**:
- Switching projects
- After completing a task
- When you don't need previous context

---

### 3. Model Selection Strategy

**Use Sonnet 4.5 (Default) for**:
✅ Normal coding tasks (99% of work)
✅ File edits and refactoring
✅ Debugging and testing
✅ Documentation writing
✅ Command execution
✅ Code reviews

**Use Opus ONLY for**:
⚠️ Critical architecture decisions
⚠️ Complex algorithm design
⚠️ Production-critical debugging
⚠️ Security-sensitive analysis

**In settings:**
```
Default Model: Sonnet 4.5
Plan Mode: OFF (uses too much Opus)
```

---

## 📊 Context Window Management

### Strategy: Keep Context Under 50K Tokens

**How to Monitor**:
```bash
# Token usage shows in status bar
# Aim to stay under 50K for efficiency
```

**Reduction Techniques**:

**1. File Reading Strategy**
```
❌ Don't: Read entire codebase
✅ Do: Use Grep to find specific code

Example:
Instead of: "Read all controllers"
Use: Grep for specific function/pattern
```

**2. Selective History**
```
❌ Don't: Keep entire conversation history
✅ Do: Use /compact to summarize old messages
✅ Do: Use /clear when context not needed
```

**3. Batch Operations**
```
❌ Don't: Make 10 separate file edits
✅ Do: List all changes, make in one go
```

---

## 🔧 Optimize Your Global Instructions

### Current Problem:
- 47 files in global-instructions/
- Many loaded automatically
- Most not needed for every task

### Solution: Conditional Loading

**Create category-specific instruction sets:**

**CLAUDE-LITE.md** (2K tokens)
- Core behavior only
- For 80% of tasks

**CLAUDE-CODING.md** (5K tokens)
- Core + coding best practices
- For development work

**CLAUDE-SECURITY.md** (6K tokens)
- Core + security frameworks
- For security analysis

**CLAUDE-FULL.md** (15K tokens)
- Everything
- For complex projects only

---

## 🎮 Usage Patterns by Task Type

### Quick Tasks (Use LITE)
- File edits
- Simple debugging
- Command execution
- Documentation updates

**Estimated usage**: 5-10K tokens/session

---

### Medium Tasks (Use CODING)
- Feature implementation
- Refactoring
- Test creation
- Code review

**Estimated usage**: 20-30K tokens/session

---

### Complex Tasks (Use FULL)
- Architecture design
- Multi-file refactoring
- Production debugging
- Security audits

**Estimated usage**: 50-100K tokens/session

---

## 📅 Weekly Limit Strategy

### Understanding Your Limits

**Max 5x Plan**:
- Resets every 7 days (weekly)
- Mini-resets every 5 hours (for rate limits)
- Shared across all Claude platforms

**Track Usage**:
```bash
/usage    # Shows: Weekly usage %, Time to reset
```

---

### Weekly Planning

**Monday-Wednesday (60% of usage)**:
- Heavy development work
- Complex problem solving
- Architecture decisions
- Use full context when needed

**Thursday-Friday (30% of usage)**:
- Lighter tasks
- Documentation
- Code reviews
- Testing

**Weekend (10% reserve)**:
- Emergency work only
- Keep reserve for urgent issues

---

## 🛠️ Practical Optimization Techniques

### 1. Agent vs Direct Work

**Use Task tool (agents) for**:
- Independent research
- Code search across large codebase
- Long-running analysis
- Parallel tasks

**Benefits**: Agents use their own context, don't bloat main session

---

### 2. Strategic Session Management

**Multiple Short Sessions > One Long Session**
```
❌ One 4-hour session (100K tokens)
✅ Four 1-hour sessions (25K tokens each)
   Use /clear between sessions
```

**Why**: Fresh context = more efficient processing

---

### 3. File Reading Optimization

**Before Reading Files**:
1. Use Glob to find files first
2. Use Grep to check content
3. Read only necessary files
4. Read specific sections (offset/limit)

**Example**:
```
❌ "Read all files in src/"
✅ "Grep for 'function handlePayment' in src/"
✅ "Read src/payment.js lines 50-100"
```

---

### 4. Response Optimization

**In your CLAUDE-LITE.md, add**:
```
Response Style:
- Be concise by default
- Explain only when asked
- Use bullet points over paragraphs
- Code over explanation
```

**Savings**: 20-30% per response

---

## 🎯 Project-Specific Strategies

### For n8n Work

**Instead of loading full n8n knowledge base**:
```
Load on-demand:
"Search n8n knowledge base for [topic]"

Rather than:
Loading all 7 documents at session start
```

**Savings**: 10-15K tokens

---

### For Coding Projects

**Use .claude-project.md instead of global instructions**:
```
Project-specific context:
- Only loaded for that project
- Doesn't affect other work
- More targeted, less bloat
```

---

## 📈 Success Metrics

### Track These Weekly

1. **Average session size**: Aim for <50K tokens
2. **Sessions per week**: More shorter sessions is better
3. **/compact usage**: Use 2-3x per session
4. **/clear usage**: Use when switching contexts
5. **Weekly limit**: Stay under 80% (save 20% for emergencies)

---

## 🚨 Warning Signs You're Using Too Much

1. **Hitting weekly limit before Friday**
2. **Regular "context window full" errors**
3. **Session tokens >100K regularly**
4. **Using Opus for routine tasks**
5. **Not using /compact or /clear**

---

## 💡 Advanced Optimization

### 1. MCP Server Optimization

**Current MCPs loaded**: 13 servers
**Each adds**: ~500-1000 tokens

**Optimize**:
```json
// In claude-code-mcp-config.json
// Disable unused MCPs:
{
  "mcpServers": {
    "essential-only": "enabled",
    "rarely-used": "disabled"
  }
}
```

---

### 2. Auto-Cleanup Script

**Create cleanup workflow**:
```bash
# Run weekly to clean old sessions
claude-cleanup.sh:
- Delete conversations >30 days old
- Clear .claude/session/ cache
- Optimize project configs
```

**One user reported**: "Usage barely moved after cleanup!"

---

### 3. Gemini Fallback for Trivial Tasks

**For simple tasks**:
- Use Gemini for grep/search operations
- Use Gemini for file reading
- Use Claude for actual coding

**Setup in settings**: Enable Gemini MCP

---

## 🎓 Learning from Community

### What Works (from r/ClaudeAI)

1. **"I cleaned up old conversations, usage barely moved for 4 hours!"**
   - Delete old session data regularly

2. **"Disabled Playwright MCP, consumption dropped significantly"**
   - Audit your MCP servers

3. **"Using Sonnet 4.5, rarely hit limits now"**
   - Trust the recommended model

4. **"Set cronjob to keep only last 30 conversations"**
   - Automate cleanup

---

### What Doesn't Work

1. ❌ Using Opus for everything (burns limits fast)
2. ❌ Never using /compact or /clear
3. ❌ Loading massive global instructions
4. ❌ Reading entire codebases into context
5. ❌ Long single sessions without breaks

---

## 📋 Daily Checklist

### Morning (Session Start)
- [ ] Check usage with /usage command
- [ ] Use CLAUDE-LITE.md for first tasks
- [ ] Plan which tasks need full context
- [ ] Set expectations for the day

### During Work
- [ ] Use /compact every 10 messages
- [ ] Switch to /clear when changing projects
- [ ] Monitor token usage in status bar
- [ ] Use Grep before Read operations

### End of Day
- [ ] Check weekly usage status
- [ ] Clean up unnecessary conversations
- [ ] Plan tomorrow's priority tasks
- [ ] Save any important context

---

## 🔄 Weekly Reset Strategy

### Monday (Reset Day)
- Fresh weekly limit
- Plan heavy tasks for early week
- Front-load complex work

### Tuesday-Wednesday
- Continue intensive work
- Monitor usage (should be ~40% by Wed)

### Thursday-Friday
- Lighter tasks
- Reserve capacity
- Use efficient patterns

### Weekend
- Emergency reserve only
- Avoid non-critical usage
- Let weekly limit reset Monday

---

## 🎯 Your Custom Optimization Plan

### Week 1: Measure Baseline
1. Use normal patterns
2. Track usage with /usage daily
3. Note which tasks use most tokens
4. Identify optimization opportunities

### Week 2: Implement Lite Mode
1. Switch to CLAUDE-LITE.md
2. Use /compact regularly
3. Measure improvement
4. Adjust as needed

### Week 3: Optimize Further
1. Clean up global instructions
2. Audit MCP servers
3. Implement project-specific configs
4. Refine workflow

### Week 4: Maintain & Monitor
1. Continue optimized patterns
2. Track weekly usage
3. Should stay under 70% weekly limit
4. Adjust if needed

---

## 📊 Expected Results

**Before Optimization**:
- Hitting weekly limit by Thursday
- 100K+ token sessions
- Context window errors
- Rushed weekend work

**After Optimization**:
- 60-70% weekly usage maximum
- 30-50K token sessions
- Rare context issues
- 20% emergency reserve maintained

**Time to implement**: 30 minutes
**Savings**: 30-50% reduction in usage

---

## 🆘 Emergency Procedures

### If You Hit Weekly Limit

**Immediate actions**:
1. Check /usage for reset time
2. Switch to Gemini for non-critical tasks
3. Use API key for urgent work (if available)
4. Plan backlog for post-reset

**Prevention for next week**:
1. Implement all optimizations above
2. Front-load critical work
3. Keep 20% reserve
4. Monitor daily usage

---

## 🎓 Key Takeaways

1. **Your global instructions (19K lines) are the main problem**
2. **Use CLAUDE-LITE.md for 80% of tasks**
3. **Sonnet 4.5 is perfect for coding (use it!)**
4. **/compact and /clear are your friends**
5. **Monitor usage daily, not weekly**
6. **Save 20% for emergencies**
7. **Shorter sessions > longer sessions**
8. **Grep before Read, always**

---

## 📞 Next Steps

1. ✅ Created CLAUDE-LITE.md (done)
2. Switch Claude Code to use CLAUDE-LITE.md
3. Run /usage to see current status
4. Implement daily checklist
5. Monitor improvement over next week

---

**Questions?**
- How much have I used this week? → /usage
- Should I use /compact? → Every 10 messages
- When to use full CLAUDE.md? → Complex projects only
- Model to use? → Sonnet 4.5 (default)

---

**This guide will help you get 30-50% more usage from your Max 5x plan!**

Save this file for reference: `USAGE-OPTIMIZATION-GUIDE.md`
