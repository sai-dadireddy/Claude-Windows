# Night Shift Agent Launcher

**Description:** Launch agents for overnight development (24/7 coding!)
**Allowed Tools:** bash, read, write, grep

---

## Usage

```bash
/night-shift             # Interactive mode
/night-shift auto        # Auto-suggest tasks
```

---

## Prompt

When user runs `/night-shift`:

### **Phase 1: ASSESS CURRENT STATE**

```bash
echo "🌙 Night Shift Agent Launcher"
echo "================================"
echo ""
echo "📊 Analyzing current project state..."
echo ""

# Check git status
git status --short

# Check open PRs
echo ""
echo "📋 Open Pull Requests:"
gh pr list --state open 2>/dev/null || echo "  (No open PRs)"

# Check recent commits
echo ""
echo "📝 Recent Activity:"
git log --oneline -5

echo ""
```

### **Phase 2: ANALYZE FOR SMALL TASKS**

Analyze the codebase and suggest **3-5 independent tasks** that are:

✅ **Good for Overnight:**
- Small, isolated features (< 4 hours)
- No dependencies on other work
- Clear acceptance criteria
- Easy to test independently
- Low merge conflict risk

❌ **Avoid Overnight:**
- Large, complex features
- Multiple file dependencies
- Architecture changes
- Database migrations
- Critical security updates

### **Phase 3: SUGGEST TASKS**

```
🎯 Suggested Overnight Tasks:

1. 📱 UI Enhancement
   Task: Add loading spinners to all async operations
   Files: src/components/*.tsx
   Estimate: 2 hours
   Risk: Low
   Conflict Risk: Low

2. 📝 Documentation
   Task: Update API documentation for recent endpoints
   Files: docs/api/*.md
   Estimate: 1 hour
   Risk: None
   Conflict Risk: None

3. 🧪 Test Coverage
   Task: Add unit tests for utility functions
   Files: tests/utils/*.test.ts
   Estimate: 3 hours
   Risk: Low
   Conflict Risk: Low

4. ⚡ Performance
   Task: Optimize image loading with lazy loading
   Files: src/components/Image.tsx
   Estimate: 2 hours
   Risk: Low
   Conflict Risk: Low

5. 🔧 Maintenance
   Task: Update dependencies (patch versions only)
   Files: package.json, package-lock.json
   Estimate: 1 hour
   Risk: Low
   Conflict Risk: Low

Which tasks would you like to launch? (enter numbers: 1 3 5)
```

### **Phase 4: USER SELECTION**

Wait for user input, then for each selected task:

```
✅ Selected Tasks: 1, 3, 5

🚀 Launching Agents...

Task 1: UI Enhancement
  📱 Mobile Agent: https://claude.ai/code?task=ui-enhancement
  📋 Instructions:
     1. Open Claude mobile app
     2. Tap "Code" tab
     3. Select current repository
     4. Paste: "Add loading spinners to all async operations in src/components/*.tsx"
     5. Enable notifications

  Expected PR: feature/ui-loading-spinners
  Estimated completion: 2 hours

Task 3: Test Coverage
  🌐 Web Agent: https://claude.ai/code?task=test-coverage
  📋 Instructions:
     1. Open claude.ai in browser
     2. Go to "Code" section
     3. Select current repository
     4. Paste: "Add comprehensive unit tests for utility functions in tests/utils/"
     5. Enable notifications

  Expected PR: feature/utility-tests
  Estimated completion: 3 hours

Task 5: Maintenance
  💻 CLI Agent: Can run locally if you're still awake
  📋 Instructions:
     cd project-root
     claude
     > "Update all patch version dependencies safely"

  Expected PR: chore/dependency-updates
  Estimated completion: 1 hour

═══════════════════════════════════════

🌙 Good night! Your agents are working...

📅 Expected Completion: Tomorrow 6:00 AM
🔔 Notifications: Enabled
📧 Morning Summary: Will be generated

💤 Sleep well! Wake up to completed features!
```

### **Phase 5: DOCUMENT PLAN**

Save overnight plan to `.claude/night-shift/YYYY-MM-DD.md`:

```markdown
# Night Shift - October 22, 2025

## Tasks Launched

### Task 1: UI Enhancement
- **Agent:** Mobile
- **Branch:** feature/ui-loading-spinners
- **Description:** Add loading spinners to async operations
- **Files:** src/components/*.tsx
- **Estimate:** 2 hours
- **Status:** In Progress

### Task 3: Test Coverage
- **Agent:** Web
- **Branch:** feature/utility-tests
- **Description:** Unit tests for utility functions
- **Files:** tests/utils/*.test.ts
- **Estimate:** 3 hours
- **Status:** In Progress

### Task 5: Maintenance
- **Agent:** CLI (optional)
- **Branch:** chore/dependency-updates
- **Description:** Patch version updates
- **Files:** package.json
- **Estimate:** 1 hour
- **Status:** Scheduled

## Morning Checklist

- [ ] Check PR status: `gh pr list --author @me`
- [ ] Review completed PRs
- [ ] Test locally
- [ ] Merge approved changes
- [ ] Handle any conflicts
- [ ] Deploy if ready

## Expected Results

**Total Hours:** 6 hours of development
**Your Time:** 0 hours (sleeping!)
**ROI:** Infinite! 😴

---

**Launched:** 10:00 PM
**Expected Completion:** 6:00 AM
**Status:** Agents working...
```

---

## Morning Review Command

Create companion command `/morning-review`:

```bash
/morning-review

# Output:
# ☀️ Good Morning! Night Shift Results:
#
# ✅ Completed (3/3):
#   - PR #123: UI Enhancement (merged)
#   - PR #124: Test Coverage (ready to review)
#   - PR #125: Dependency Updates (conflicts ⚠️)
#
# 📊 Summary:
#   - 6 hours of development completed
#   - 2 PRs ready to merge
#   - 1 requires conflict resolution
#
# 🎯 Next Steps:
#   1. Review PR #124
#   2. Resolve conflicts in PR #125
#   3. Start today's sprint!
```

---

## Task Selection Criteria

### **✅ Perfect for Overnight**
- UI polish & styling
- Documentation updates
- Test additions
- Performance optimizations
- Dependency updates (patches)
- Bug fixes (isolated)
- Code formatting
- Refactoring (small scope)

### **⚠️ Proceed with Caution**
- New features (small only)
- API changes (additive)
- Database queries (read-only)

### **❌ Never Overnight**
- Authentication changes
- Database migrations
- Critical security fixes
- Breaking API changes
- Large refactors
- Production deployments

---

## Best Practices

1. **Start Small** - First night, try 1-2 tasks
2. **Review Mornings** - Check all PRs before merging
3. **Test Locally** - Don't blindly merge
4. **Document Issues** - Note what didn't work
5. **Iterate** - Improve task selection over time

---

## Safety Features

### **Automatic Safeguards:**
- All work done in feature branches
- No direct commits to main
- PRs require review
- Tests must pass
- Conflicts flagged for manual resolution

### **Notification Strategy:**
- Enable mobile notifications
- Get alerts when PRs ready
- Morning summary email
- Conflict warnings

---

## Advanced Usage

### **Weekly Night Shift Pattern**
```
Monday Night: Documentation + Tests
Tuesday Night: UI Polish + Performance
Wednesday Night: Bug Fixes + Refactoring
Thursday Night: Dependencies + Maintenance
Friday Night: Code Review Prep + Cleanup
```

### **Project-Specific Templates**
Create `.claude/night-shift-templates/`:
- `frontend.yaml` - UI-focused tasks
- `backend.yaml` - API-focused tasks
- `fullstack.yaml` - Mixed tasks
- `maintenance.yaml` - Housekeeping tasks

---

## Example Sessions

### **Example 1: First Time**
```bash
$ /night-shift

🌙 Night Shift Agent Launcher
================================

📊 Current state looks good!
🎯 Suggested tasks: 5 options

Selected: 1, 2 (start small!)

✅ Agents launched!
💤 Sleep well!
```

### **Example 2: Power User**
```bash
$ /night-shift auto

🌙 Auto-launching 5 optimal tasks...

✅ All agents launched!
📧 Morning summary scheduled
💤 See you at 6 AM!
```

### **Example 3: Custom Tasks**
```bash
$ /night-shift

[Suggests 5 tasks]

> Actually, can you add tests for the auth module?
> And update the deployment docs?

✅ Custom tasks added!
🚀 Launching 7 agents total...
```

---

## ROI Calculation

```
Traditional Development:
- 5 small tasks = 10 hours
- Done during work hours
- Blocks other work

Night Shift Development:
- 5 small tasks = 10 hours
- Done while sleeping
- Zero blocking time

Time Saved: 10 hours per night!
Weekly Savings: 50 hours!
Monthly Savings: 200 hours!

Cost: $100-200/month (Claude Max)
Value: 200 hours × $hourly_rate
```

---

## Tips

💡 **Productivity Hack:** Run night-shift Friday night, wake up Monday to completed features!

🎯 **Pro Tip:** Combine with `/worktree` for even more parallelism

🔔 **Must Do:** Enable notifications or you'll miss completion alerts

📊 **Track Results:** Keep log of overnight success rate

⚡ **Optimize:** Note which tasks work best overnight

---

**Remember:** This is 24/7 development! You sleep, agents work. Wake up to completed features! 😴→☀️→🚀
