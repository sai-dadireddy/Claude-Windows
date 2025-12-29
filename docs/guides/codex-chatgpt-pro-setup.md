# Using Codex CLI with ChatGPT Pro Subscription (No API Costs!)

**Your ChatGPT Pro subscription ($200/month) includes Codex CLI usage - no additional API costs!**

---

## 🎯 Your Benefits

**ChatGPT Pro Subscription Limits**:
- ✅ **300-1,500 local messages** every 5 hours
- ✅ **50-400 cloud tasks** every 5 hours
- ✅ **Shared weekly limit** (resets weekly)
- ✅ **$50 in free API credits** (bonus when you sign in)
- ✅ **Code review doesn't count** toward limits (limited time)
- ✅ **Cloud tasks free until Oct 20, 2025** (grace period)

**Comparison** (for context):
- ChatGPT Plus ($20/month): 30-150 messages / 5-40 cloud tasks per 5 hours
- You have **10x more capacity** with Pro!

---

## 🚀 Setup: Use Your Pro Subscription (Not API)

### Step 1: Login with ChatGPT Account

Instead of using API keys, log in with your ChatGPT Pro account:

```bash
codex login
```

**This will**:
1. Open browser to ChatGPT login
2. Link Codex CLI to your Pro subscription
3. Give you access to Pro usage limits
4. Grant you $50 in bonus API credits

### Step 2: Verify Login Status

```bash
codex status
```

Should show:
```
✓ Logged in as: your@email.com
✓ Plan: ChatGPT Pro
✓ Usage: X/1500 messages (5-hour window)
✓ Cloud tasks: X/400 (5-hour window)
```

### Step 3: Use Codex with Pro Subscription

```bash
# Just use it normally - no API key needed!
codex
```

**All usage counts against your Pro subscription limits, not API billing!**

---

## 💡 Maximizing Your Pro Subscription

### 1. **Prefer Local Tasks** (Higher Limits)

```bash
# Local mode (300-1,500 per 5 hours)
codex

# In Codex session:
> Edit this file locally
```

**Local tasks** have 3-10x higher limits than cloud tasks!

### 2. **Use Cloud Tasks for Heavy Lifting**

```bash
# Cloud mode (50-400 per 5 hours)
codex --cloud

# Or in session:
> /cloud Run this complex analysis
```

**Cloud tasks** = More powerful but lower limits

### 3. **Free Code Reviews** (Limited Time)

```bash
# These DON'T count toward limits!
codex review pr
codex review commit
```

**GitHub PR reviews** are free (for now)!

### 4. **Monitor Your Usage**

```bash
codex usage
```

Shows:
- Messages used / limit
- Cloud tasks used / limit
- Weekly limit progress
- When limits reset

---

## 🔄 When You Hit Limits

**Option 1: Wait for Reset**
- Local messages: Reset every 5 hours
- Cloud tasks: Reset every 5 hours
- Weekly limit: Resets weekly

**Option 2: Use API Key as Fallback**
```bash
# Only if you hit subscription limits
export OPENAI_API_KEY="your-api-key"
codex --api-mode
```

**This bills at standard API rates** - only use if urgent!

---

## ⚙️ Recommended Configuration

**File**: `~/.codex/config.toml`

```toml
[auth]
use_subscription = true  # Use ChatGPT Pro, not API
fallback_to_api = false  # Don't auto-fallback to paid API

[limits]
warn_at_percentage = 80  # Warn at 80% usage
pause_at_limit = true    # Stop when limit hit

[preferences]
prefer_local = true      # Use local mode (higher limits)
model = "gpt-5-codex"    # Best model for coding
reasoning_effort = "high" # Maximum quality
```

---

## 🎯 Best Practices

### 1. **Track Your Usage**

```bash
# Check before starting big tasks
codex usage

# If close to limit, wait for reset
# OR switch to Claude Code for that task
```

### 2. **Use Right Tool for Right Job**

| Task | Best AI | Why |
|------|---------|-----|
| Large codebase reading | Gemini CLI | 2M context, doesn't use Pro limits |
| Implementation | Claude Code | Fastest, doesn't use Pro limits |
| Deep review/debugging | Codex | Best debugging, uses Pro limits strategically |
| Architecture | Codex | Deep reasoning, worth using Pro limits |

### 3. **Combine with Claude Code**

**Perfect workflow**:
1. **Claude Code** implements (doesn't use your Pro limits)
2. **Codex** reviews (uses Pro limits strategically)
3. **Claude Code** applies feedback (doesn't use Pro limits)
4. **Gemini CLI** analyzes large context (doesn't use Pro limits)

**Result**: Maximize value of Pro subscription!

---

## 🔧 Integrating with Claude Code

### Add Codex as MCP Server

```bash
claude mcp add codex --scope user -- codex -m gpt-5-codex -c model_reasoning_effort="high" mcp-server
```

**Now Claude Code can call Codex directly!**

**Claude Code session**:
```
"Review this code using Codex for architectural insights"
```

**I (Claude Code) will**:
1. Call Codex MCP (uses your Pro subscription)
2. Get deep review
3. Implement fixes
4. Report back

---

## 📊 Usage Monitoring Dashboard

**Check usage regularly**:

```bash
# Quick status
codex status

# Detailed usage
codex usage --detailed

# Usage history
codex usage --history
```

**Example output**:
```
ChatGPT Pro Usage (5-hour window):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Local messages:  450 / 1500 (30%)  ✓
Cloud tasks:     12 / 400   (3%)   ✓
Weekly limit:    2850 / 10000 (28%) ✓

Next reset: 2h 35m

Bonus API credits: $42.50 / $50 remaining
```

---

## 🚨 Common Issues & Solutions

### Issue: "You've reached your usage limit"

**Solution**:
```bash
# Check when limit resets
codex usage

# Wait for reset, OR
# Switch to Claude Code for this task, OR
# Use API key (if urgent and OK with paying)
```

### Issue: "Can't use Codex CLI with subscription login"

**Solution**:
```bash
# Logout and re-login
codex logout
codex login

# Verify
codex status
```

### Issue: "Codex using API key instead of subscription"

**Solution**:
```bash
# Remove API key from environment
unset OPENAI_API_KEY

# Or in config.toml:
use_subscription = true
```

---

## 💰 Cost Comparison

**Without this setup** (using API):
- GPT-5 API: ~$30-100/day for heavy usage
- Your cost: $900-3000/month

**With ChatGPT Pro subscription**:
- Codex CLI: Included in $200/month
- Bonus credits: $50/month free
- Your cost: $200/month (fixed)

**Savings**: $700-2800/month! 🎉

---

## 🎯 Pro Tips

1. **Use Codex for what it's best at**:
   - Deep code reviews
   - Architecture planning
   - Debugging complex issues
   - Edge case analysis

2. **Don't waste limits on**:
   - Reading large files (use Gemini CLI)
   - Simple implementations (use Claude Code)
   - Repetitive tasks (use Claude Code)

3. **Strategic usage**:
   - Save Codex for complex problems
   - Use other AIs for simple tasks
   - Monitor usage daily
   - Plan heavy Codex usage for start of 5-hour window

---

## 📚 Resources

**Official Docs**: https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
**Codex GitHub**: https://github.com/openai/codex
**Usage Limits**: https://developers.openai.com/codex/pricing

---

## Bottom Line

✅ **You have Codex CLI included with your Pro subscription**
✅ **No API costs for up to 1,500 messages per 5 hours**
✅ **$50 bonus API credits per month**
✅ **Perfect for code reviews and deep analysis**
✅ **Combine with Claude Code & Gemini for optimal workflow**

**Total AI Arsenal** (all using subscriptions, not APIs):
- Claude Code (me): Implementation
- Codex CLI: Review & debugging
- Gemini CLI: Large context analysis

**Zero additional API costs!** 🚀
