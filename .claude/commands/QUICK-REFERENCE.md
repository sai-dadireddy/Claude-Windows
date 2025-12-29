---
Title: Mega-Commands Quick Reference
Type: Cheat Sheet
Size: 50-100 tokens
Updated: 2025-10-28
---

# Mega-Commands Quick Reference

## Session Management
```bash
/session save           # Save & cleanup (340K tokens freed)
/session continue       # Resume (optimized, 550-1K tokens)
/session status         # Check metrics
/session kill           # Terminate cleanly
```

## AI Operations
```bash
/ai orchestrate "task"         # Multi-AI coordination
/ai review @src/auth/          # Code review consensus
/ai consult "strategy Q"       # AI panel advice
/ai delegate @security-auditor "scan API"
```

## Code Optimization
```bash
/optimize code src/            # Clean code
/optimize performance api      # Speed up
/optimize refactor safe        # Refactor safely
/optimize all src/             # Everything (5-10 min)
```

## Testing
```bash
/test generate @src/auth.ts    # Create tests
/test heal tests/auth.test.ts  # Fix failing tests
/test coverage 90              # 90% coverage
/test e2e tests/checkout.spec.ts  # E2E tests
```

## Security
```bash
/security scan src/            # Quick scan (<2 min)
/security audit api            # Deep audit (5-15 min)
/security penetrate api        # Pen testing
/security compliance gdpr      # Compliance check
```

## Token Management
```bash
/tokens monitor 60s            # Live tracking
/tokens profile                # Usage analysis
/tokens optimize               # Recommendations
/tokens compact                # Emergency cleanup
```

## Knowledge Management
```bash
/knowledge query "useState" --tech react    # RAG query (97% savings!)
/knowledge search "auth patterns"           # Semantic search
/knowledge status                           # Check health
/knowledge add docs/guides/                 # Index new docs
```

---

## Most Common Patterns

### Start of Work Session
```bash
/session continue              # Resume (1K tokens)
/tokens monitor 60s            # Monitor tokens
/knowledge status              # Check RAG health
```

### Development Iteration
```bash
/test generate @src/component.ts    # Create tests
/optimize code src/                 # Clean code
/security scan src/                 # Quick check
/tokens profile                     # Usage check
```

### Code Review
```bash
/ai review @src/auth/               # Multi-AI review
/security review @src/auth.ts       # Security focus
/optimize refactor safe             # Structural improvements
```

### Before Session End
```bash
/test coverage 90                   # Check coverage
/security audit api                 # Full security
/optimize all src/                  # Final polish
/session save                       # Save & cleanup
```

### Emergency Cleanup
```bash
/tokens compact                     # Free 10-50K tokens
/session kill                       # Clean termination
```

---

## Pro Tips

### Token Savings
- Use `/knowledge` instead of reading large docs (97% savings!)
- Use `/tokens monitor` to watch burn rate
- Use `/session save` regularly (340K tokens freed per session)

### Speed Improvements
- Use `/optimize all` instead of individual optimizations
- Use `/ai orchestrate` for complex tasks (parallel execution)
- Use `/test coverage` instead of manual test review

### Quality Improvements
- Use `/ai review` for multi-perspective feedback
- Use `/security audit` before deployment
- Use `/test e2e` for user flow validation

### Smart Delegation
- Security → `/ai delegate @security-auditor`
- Performance → `/ai delegate @performance-engineer`
- Testing → `/ai delegate @test-automator`

---

## Quick Stats

| Operation | Tokens | Speed | Result |
|-----------|--------|-------|--------|
| `/knowledge query` | 50 | <500ms | 97% savings vs reading |
| `/session save` | 300 | 6 min | 340K tokens freed |
| `/test generate` | 200 | <1 min | Full test suite |
| `/security scan` | 100 | 2 min | Vulnerability report |
| `/optimize all` | 500 | 10 min | Complete optimization |

---

## Default Behaviors

- No action? → Defaults to `status` or `list`
- No target? → Uses current directory
- No options? → Uses sensible defaults
- Errors? → Shows helpful suggestions

---

## Integration Points

- **RAG**: `/knowledge` uses 12+ doc collections
- **Multi-AI**: `/ai` uses Claude, GPT-4, Gemini
- **Agents**: `/ai delegate` uses specialized agents
- **Git**: `/session save` commits + pushes
- **Tracking**: All operations update ROADMAP.md

---

## Model Selection

- **haiku** (fast): `/tokens`, `/knowledge`
- **sonnet** (balanced): `/session`, `/optimize`, `/test`
- **custom**: `security` (complex), `ai` (coordination)

---

Remember: These 7 commands replace 40+ specialized commands. Master them for 10x productivity!
