---
description: Comprehensive security (scan|audit|review|analyze|penetrate|compliance)
argument-hint: <action> [target]
allowed-tools: Read, Grep, Glob, Bash, Task
model: sonnet
---

# Security Operations

Action: $ARGUMENTS

## Available Actions:

### scan [path]
Quick security scan for common vulnerabilities
- XSS, SQL injection, hardcoded secrets
- Insecure dependencies (npm audit, pip audit)
- Path: defaults to current directory
- Time: <2 minutes
- Format: JSON report saved to .claude/context/

### audit [component]
Deep security audit with compliance checks
- OWASP Top 10 analysis
- Authentication/authorization review
- Data protection (encryption, PII)
- Component: api|frontend|backend|full (default: full)
- Delegates to: @security-auditor
- Time: 5-15 minutes

### review [files]
Code review focused on security best practices
- Input validation, output encoding
- Secure coding patterns
- Cryptography review
- Error handling security
- Files: specific files or git diff

### analyze
Comprehensive security analysis
- Threat modeling
- Attack surface analysis
- Security architecture review
- Data flow analysis
- Delegates to: @security-architect
- Generates THREAT-MODEL.md

### penetrate [target]
Penetration testing
- target: api|frontend|backend (default: api)
- Authentication bypass attempts
- Authorization testing
- Injection testing
- Session management testing
- Delegates to: @penetration-tester

### compliance [standard]
Compliance verification
- standard: pci|hipaa|gdpr|sox|iso27001 (default: owasp)
- Regulatory checklist
- Audit trail requirements
- Data residency checks
- Delegates to: @compliance-auditor

### secrets
Hardcoded secrets detection
- Scans entire codebase
- Checks environment variables
- Checks config files
- Suggests secret rotation
- Integrates with git hooks

### dependencies
Dependency security analysis
- Vulnerability scanning (CVE, CVE-2024-*)
- License compliance
- Outdated package detection
- Supply chain analysis
- Auto-update suggestions

## Usage Examples:
```
/security scan src/
/security audit api
/security review @src/auth.ts
/security analyze
/security penetrate api
/security compliance gdpr
/security secrets
/security dependencies
```

## OWASP Top 10 Coverage:
1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable Components
7. Authentication Failures
8. Software Integrity
9. Logging & Monitoring
10. SSRF

## Key Features:
- Auto-detects tech stack
- Generates detailed reports
- Prioritizes findings by severity
- Provides remediation suggestions
- Tracks in ROADMAP.md
- CI/CD integration ready

## Integration:
- SAST tools (SonarQube, Snyk)
- DAST tools (OWASP ZAP)
- Dependency checkers
- Secret scanners
- Results saved to .claude/context/

## Delegates to Agents:
- @security-code-reviewer (code review)
- @security-auditor (audits)
- @penetration-tester (pen testing)
- @compliance-auditor (compliance)
- @security-architect (architecture)
