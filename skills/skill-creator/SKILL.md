---
name: skill-creator
description: Meta skill that creates new Claude Skills from plain English descriptions using best practices and proper structure
tags: [meta, skill-creation, automation, templates]
---

# Skill Creator - Meta Skill

## Overview

This skill helps create new Claude Skills from plain English descriptions. It follows Anthropic's best practices and community patterns to generate production-ready skill files.

## When to Use

Use this skill when:
- User requests "Create a skill for [task]"
- Need to document a new capability as a skill
- Want to standardize a workflow into a reusable skill
- Converting documentation into skill format

## Skill Structure Template

```markdown
---
name: skill-name-lowercase
description: One clear sentence that Claude uses to decide when to load this skill (be specific about use cases)
tags: [relevant, searchable, tags, for, categorization]
---

# Skill Title (Descriptive Name)

## Overview

Brief description of what this skill helps with (2-3 sentences).
Include the main value proposition and key capabilities.

## When to Use

Clear bullet points of specific use cases:
- Use case 1 (be specific)
- Use case 2 (with examples)
- Use case 3 (concrete scenarios)

## When NOT to Use

Clarify boundaries (avoid scope creep):
- What this skill doesn't cover
- Related but different use cases
- Alternative skills to use instead

## How to Use

### Step-by-Step Instructions

1. **First Step**
   - Details
   - Examples
   - Expected outcome

2. **Second Step**
   - Details
   - Code examples with comments
   - Expected outcome

3. **Final Step**
   - Validation
   - Quality checks
   - Next steps

## Examples

### Example 1: [Scenario Name]
```language
// Well-commented code example
// showing proper usage
```

**Context**: When to use this pattern
**Result**: What you get

### Example 2: [Another Scenario]
```language
// Different use case
// with clear comments
```

## Best Practices

✅ DO:
- Practice 1 with reasoning
- Practice 2 with reasoning
- Practice 3 with reasoning

❌ DON'T:
- Anti-pattern 1 and why
- Anti-pattern 2 and why
- Anti-pattern 3 and why

## Common Pitfalls

### Pitfall 1: [Name]
**Problem**: Description of the issue
**Solution**: How to avoid or fix it
**Example**: Code example

### Pitfall 2: [Name]
**Problem**: Description
**Solution**: Fix approach
**Example**: Demonstration

## Decision Trees (if applicable)

```
┌─────────────────────┐
│ Start Condition     │
└──────┬──────────────┘
       │
       ▼
  [Decision Point?]
   /            \
  YES           NO
  /              \
[Action A]    [Action B]
```

## Checklists (if applicable)

### Pre-Implementation Checklist:
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

### Post-Implementation Checklist:
- [ ] Validation 1
- [ ] Validation 2
- [ ] Validation 3

## Tools & Resources

### MCP Tools (if applicable):
- Tool 1: What it does
- Tool 2: How to use it
- Tool 3: When to use it

### External Resources:
- Link 1: Description
- Link 2: Purpose
- Link 3: When to reference

## Integration with Other Skills

This skill works well with:
- **Related Skill 1**: How they complement each other
- **Related Skill 2**: When to use together
- **Related Skill 3**: Integration patterns

## Troubleshooting

### Issue 1: [Common Problem]
**Symptoms**: What you see
**Cause**: Why it happens
**Solution**: Step-by-step fix

### Issue 2: [Another Problem]
**Symptoms**: Description
**Cause**: Root cause
**Solution**: Resolution steps

## Advanced Usage (optional)

For complex skills, include:
- Advanced patterns
- Edge cases
- Performance optimization
- Integration patterns
- Scaling considerations

## Code Examples (if skill involves coding)

### Helper Script Pattern:
```python
#!/usr/bin/env python3
"""
Helper script for this skill.
Located in: core/helper.py
"""

import sys
import os

# Add skill directory to path
sys.path.insert(0, '/mnt/skills/skill-name')

def main():
    # Implementation
    pass

if __name__ == "__main__":
    main()
```

## Quality Checklist

Before considering skill complete:

**Structure**:
- [ ] YAML frontmatter with name, description, tags
- [ ] Clear overview and value proposition
- [ ] Specific "When to Use" section
- [ ] "When NOT to Use" for boundaries
- [ ] Step-by-step instructions

**Content**:
- [ ] At least 2 concrete examples
- [ ] Best practices with reasoning
- [ ] Common pitfalls with solutions
- [ ] Integration with other skills
- [ ] Troubleshooting section

**Code Quality** (if applicable):
- [ ] All code examples are runnable
- [ ] Code is well-commented
- [ ] Examples cover common use cases
- [ ] Error handling demonstrated

**Clarity**:
- [ ] Instructions are unambiguous
- [ ] Technical terms are explained
- [ ] Examples are realistic
- [ ] Checklists are actionable

---

**Status**: ✅ PRODUCTION READY
**Version**: 1.0.0
**Last Updated**: 2025-10-18
