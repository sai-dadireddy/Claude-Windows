Run a **comprehensive security audit** including permission analysis with cc-safe.

## Security Audit Workflow

### Phase 1: Permission Analysis (cc-safe)

Check for risky approved commands:

```bash
# Install cc-safe if needed
npm install -g cc-safe

# Scan project for security issues
npx cc-safe .

# Or scan specific directory
npx cc-safe ~/projects/myproject
```

**cc-safe checks for:**
- `rm -rf` patterns
- `sudo` commands
- `curl | sh` (pipe to shell)
- Privileged Docker operations
- Overly broad file permissions

### Phase 2: Code Security Review

Use `/security-review` for code-level vulnerabilities:
- SQL injection
- Command injection
- XSS vulnerabilities
- Auth bypass
- Data exposure

### Phase 3: Dependency Audit

```bash
# Node.js
npm audit
npm audit fix

# Python
pip-audit
safety check

# Go
govulncheck ./...
```

### Phase 4: Secret Detection

```bash
# Check for committed secrets
git secrets --scan

# Or use truffleHog
trufflehog git file://. --only-verified
```

### Phase 5: Configuration Review

Check for:
- [ ] `.env` files not in `.gitignore`
- [ ] Hardcoded credentials
- [ ] Debug mode in production
- [ ] Verbose error messages exposed
- [ ] CORS misconfiguration
- [ ] Missing rate limiting

## Output Format

```markdown
## Security Audit Report

**Project:** [Name]
**Date:** [Date]
**Auditor:** Claude

### Executive Summary
[1-2 sentence overall assessment]

### Risk Level: [LOW/MEDIUM/HIGH/CRITICAL]

---

### 1. Permission Analysis (cc-safe)
**Status:** [PASS/WARN/FAIL]

| Finding | Severity | Location |
|---------|----------|----------|
| [Issue] | [Sev] | [Where] |

**Recommendations:**
- [ ] [Action item]

---

### 2. Code Vulnerabilities
**Status:** [PASS/WARN/FAIL]

[Results from /security-review or manual analysis]

---

### 3. Dependencies
**Status:** [PASS/WARN/FAIL]

| Package | Vulnerability | Severity | Fix |
|---------|---------------|----------|-----|
| [pkg] | [CVE] | [Sev] | [Version] |

---

### 4. Secrets
**Status:** [PASS/WARN/FAIL]

| Finding | File | Line |
|---------|------|------|
| [Type] | [Path] | [#] |

---

### 5. Configuration
**Status:** [PASS/WARN/FAIL]

| Check | Status | Notes |
|-------|--------|-------|
| .env in .gitignore | ✅/❌ | |
| Debug mode off | ✅/❌ | |
| HTTPS enforced | ✅/❌ | |

---

### Action Items (Priority Order)

1. **CRITICAL:** [Item]
2. **HIGH:** [Item]
3. **MEDIUM:** [Item]

### Next Audit
Recommended: [Date/trigger]
```

## Quick Commands

```bash
# Full audit
npx cc-safe . && npm audit && git secrets --scan

# Just permissions
npx cc-safe .

# Just dependencies
npm audit --audit-level=moderate
```

---

**Run security audit on:**

$ARGUMENTS
