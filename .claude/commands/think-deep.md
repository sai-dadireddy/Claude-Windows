# Deep Thinking Planner

**Description:** Force ultrathink + planning mode for complex problems
**Allowed Tools:** bash, read, write, web_search, grep

---

## Usage

```bash
/think-deep "Your complex problem or feature"
```

---

## Prompt

When user runs `/think-deep`:

### **CRITICAL: Use Maximum Thinking Power**
- Use **ULTRATHINK** mode for maximum cognitive effort
- Spend significant time analyzing before responding
- Consider multiple perspectives and edge cases
- Think through implications deeply

### **Phase 1: RESEARCH** (If applicable)
1. Search web for best practices and patterns
2. Review similar implementations
3. Analyze current industry standards
4. Gather relevant examples

### **Phase 2: ANALYZE Current State**
1. Review existing codebase structure
2. Identify relevant files and dependencies
3. Understand current architecture
4. Note technical constraints
5. Document assumptions

### **Phase 3: DEEP THINKING**
Apply ultrathink mode to consider:
- **Technical feasibility** - Can we build this?
- **Architecture impact** - How does it fit?
- **Performance implications** - Will it scale?
- **Security considerations** - Is it safe?
- **Maintainability** - Can we support it?
- **Testing strategy** - How to verify?
- **Edge cases** - What could break?
- **Dependencies** - What do we need?

### **Phase 4: GENERATE OPTIONS**
Create **3 different approaches**:

#### **Option 1: Simple & Fast**
- Pros: Quick to implement, low risk
- Cons: May lack features, technical debt
- Time estimate: X hours
- Complexity: Low

#### **Option 2: Balanced**
- Pros: Good features, manageable complexity
- Cons: Moderate time investment
- Time estimate: X hours
- Complexity: Medium

#### **Option 3: Comprehensive**
- Pros: Full featured, future-proof
- Cons: High complexity, longer timeline
- Time estimate: X hours
- Complexity: High

### **Phase 5: RECOMMEND**
Based on ultrathink analysis:
- **Recommended approach:** Option X
- **Reasoning:** [Deep explanation]
- **Trade-offs:** [What we're accepting]
- **Risks:** [What could go wrong]
- **Mitigation:** [How to handle risks]

### **Phase 6: DETAILED PLAN**
For recommended approach:

1. **Prerequisites**
   - Dependencies to install
   - Environment setup
   - Required tools

2. **Architecture**
   - Component diagram
   - Data flow
   - Integration points

3. **Implementation Steps**
   ```
   Phase 1: Foundation (X hours)
   - Task 1
   - Task 2

   Phase 2: Core Features (X hours)
   - Task 3
   - Task 4

   Phase 3: Testing & Polish (X hours)
   - Task 5
   - Task 6
   ```

4. **Testing Strategy**
   - Unit tests
   - Integration tests
   - E2E tests
   - Manual QA checklist

5. **Success Criteria**
   - Feature complete when...
   - Performance metrics
   - User acceptance criteria

6. **Rollback Plan**
   - If things go wrong
   - How to revert safely
   - Data migration considerations

### **Phase 7: DOCUMENT**
Save comprehensive plan to:
```
docs/planning/<feature-name>-plan.md
```

Include:
- Executive summary
- All 3 options analyzed
- Recommended approach with reasoning
- Detailed implementation plan
- Architecture diagrams (text-based)
- Testing strategy
- Timeline estimate
- Risk assessment

---

## Output Format

```markdown
# Deep Thinking Analysis: [Feature Name]

**Date:** YYYY-MM-DD
**Thinking Mode:** ULTRATHINK
**Status:** Planning Complete

## 🎯 Executive Summary
[One paragraph overview]

## 🔍 Research Findings
[Key insights from research]

## 📊 Current State Analysis
[Codebase review findings]

## 💡 Three Approaches

### Option 1: Simple & Fast
**Pros:** ...
**Cons:** ...
**Estimate:** X hours
**Complexity:** Low

### Option 2: Balanced ⭐ RECOMMENDED
**Pros:** ...
**Cons:** ...
**Estimate:** X hours
**Complexity:** Medium

### Option 3: Comprehensive
**Pros:** ...
**Cons:** ...
**Estimate:** X hours
**Complexity:** High

## 🎯 Recommendation

**Chosen Approach:** Option 2 (Balanced)

**Reasoning:**
[Deep explanation of why this is best]

**Trade-offs Accepted:**
- [Trade-off 1]
- [Trade-off 2]

**Risks & Mitigation:**
- Risk: [What could go wrong]
  Mitigation: [How to handle]

## 📋 Implementation Plan

### Prerequisites
- [ ] Dependency 1
- [ ] Dependency 2

### Phase 1: Foundation (X hours)
- [ ] Task 1
- [ ] Task 2

### Phase 2: Core Features (X hours)
- [ ] Task 3
- [ ] Task 4

### Phase 3: Testing & Polish (X hours)
- [ ] Task 5
- [ ] Task 6

## 🏗️ Architecture

```
[Text-based architecture diagram]
```

**Key Components:**
1. Component A - Does X
2. Component B - Does Y

**Data Flow:**
Input → Processing → Output

## 🧪 Testing Strategy

**Unit Tests:**
- Test A
- Test B

**Integration Tests:**
- Test C
- Test D

**E2E Tests:**
- Scenario 1
- Scenario 2

## ✅ Success Criteria

Feature is complete when:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] All tests pass
- [ ] Performance meets benchmarks
- [ ] Documentation updated

## ⚠️ Rollback Plan

If deployment fails:
1. Step 1 to revert
2. Step 2 to restore
3. Communication plan

## 📈 Timeline

**Total Estimate:** X hours
- Planning: Y hours ✅
- Development: Z hours
- Testing: W hours

**Milestones:**
- Week 1: Foundation complete
- Week 2: Features complete
- Week 3: Testing complete

---

**Next Steps:**
1. Review this plan
2. Approve approach
3. Begin implementation
4. Create tasks in /worktree
```

---

## Examples

### **Example 1: Authentication System**
```bash
/think-deep "Add OAuth authentication with Cognito"

# Claude will:
# 1. Research OAuth best practices
# 2. Analyze current auth system
# 3. Generate 3 approaches
# 4. Recommend balanced option
# 5. Create detailed implementation plan
# 6. Save to docs/planning/oauth-auth-plan.md
```

### **Example 2: Performance Optimization**
```bash
/think-deep "Optimize database queries causing slow page loads"

# Claude will:
# 1. Analyze current query patterns
# 2. Research optimization techniques
# 3. Profile performance bottlenecks
# 4. Generate optimization strategies
# 5. Plan phased implementation
# 6. Document expected improvements
```

### **Example 3: Architecture Decision**
```bash
/think-deep "Choose between REST API vs GraphQL for new endpoints"

# Claude will:
# 1. Research REST vs GraphQL trade-offs
# 2. Analyze current API architecture
# 3. Consider team expertise
# 4. Evaluate future scalability
# 5. Provide detailed recommendation
# 6. Create migration plan if needed
```

---

## Best Practices

1. **Use for Complex Decisions** - Not simple tasks
2. **Review the Plan** - Don't skip the thinking
3. **Save the Document** - Reference later
4. **Iterate if Needed** - Re-run with feedback
5. **Share with Team** - Get input on approach

---

## When to Use

✅ **Use /think-deep for:**
- New feature planning
- Architecture decisions
- Complex bug fixes
- Performance optimizations
- Security implementations
- Major refactors

❌ **Don't use for:**
- Simple tasks
- Routine changes
- Documentation updates
- Minor bug fixes
- Quick experiments

---

**Remember:** The goal is DEEP THINKING before coding. Take time to plan, analyze trade-offs, and choose the best approach. This saves time in the long run!
