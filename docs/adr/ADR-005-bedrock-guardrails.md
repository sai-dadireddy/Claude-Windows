# ADR-005: Bedrock Guardrails for Content Safety

## Status

**Accepted** - January 2025

## Context

Sherpa processes diverse content including:
- User queries and code
- Scraped documentation from Workday and Oracle
- Generated responses and code
- Knowledge base content

Enterprise deployment requires content safety controls for:
1. **PII Protection**: Prevent exposure of SSNs, credit cards, personal data
2. **Toxic Content**: Block harmful, offensive, or inappropriate content
3. **Compliance**: Meet enterprise security and privacy requirements
4. **Prompt Injection**: Detect attempts to manipulate AI behavior

Options considered:

| Solution | Pros | Cons |
|----------|------|------|
| Custom regex | Simple, fast | Incomplete, maintenance burden |
| Third-party API | Comprehensive | Additional vendor, latency |
| **Bedrock Guardrails** | Native AWS, enterprise-grade | AWS-only, cost |
| Client-side filters | No latency | Bypassable, limited |

## Decision

Implement AWS Bedrock Guardrails as the primary content safety layer for all Sherpa API interactions.

### Guardrail Configuration

```
+------------------+     +-------------------+     +------------------+
|   User Input     | --> | Bedrock Guardrail | --> |   Claude/Model   |
+------------------+     | (Input Filter)    |     +------------------+
                         +-------------------+              |
                                                           v
+------------------+     +-------------------+     +------------------+
|   User Output    | <-- | Bedrock Guardrail | <-- |   Model Response |
+------------------+     | (Output Filter)   |     +------------------+
```

### Filter Categories

#### 1. PII Blocking (Deny)

| PII Type | Action | Rationale |
|----------|--------|-----------|
| SSN | Block | Legal requirement |
| Credit Card | Block | PCI compliance |
| Bank Account | Block | Financial data protection |
| AWS Keys | Block | Security |
| Passwords | Block | Security |

#### 2. PII Masking (Allow with redaction)

| PII Type | Action | Example |
|----------|--------|---------|
| Email | Mask | user@example.com -> [EMAIL] |
| Phone | Mask | 555-123-4567 -> [PHONE] |
| Name | Mask (configurable) | Context-dependent |
| Address | Mask | 123 Main St -> [ADDRESS] |

#### 3. Toxic Content Filters

| Category | Threshold | Action |
|----------|-----------|--------|
| Hate speech | Low | Block |
| Violence | Medium | Block |
| Sexual content | Low | Block |
| Self-harm | Low | Block |
| Harassment | Medium | Block |

#### 4. Prompt Injection Detection

| Pattern | Action |
|---------|--------|
| Ignore previous instructions | Flag + Log |
| System prompt extraction attempts | Block |
| Role-play manipulation | Flag |
| Jailbreak patterns | Block + Alert |

## Consequences

### Positive

- **Enterprise-ready**: Meets compliance requirements out of the box
- **Low latency**: Guardrails add less than 100ms to requests
- **Comprehensive**: Covers PII, toxicity, and custom patterns
- **Auditable**: All interventions logged to CloudWatch
- **Configurable**: Thresholds adjustable per use case
- **Native integration**: Works seamlessly with Bedrock models

### Negative

- **AWS lock-in**: Only works with Bedrock-hosted models
- **Cost**: $0.75 per 1000 text units analyzed
- **False positives**: May block legitimate security discussions
- **Limited customization**: Cannot train custom classifiers

### Mitigations

- Use guardrails only for external-facing APIs
- Implement feedback loop for false positive tuning
- Provide bypass mechanism for authorized workflows
- Monitor and adjust thresholds based on usage patterns

## Monitoring and Alerting

### CloudWatch Metrics

| Metric | Alert Threshold | Action |
|--------|-----------------|--------|
| GuardrailIntervention | >10/hour | Investigate patterns |
| PIIDetected | >5/hour | Review data handling |
| PromptInjectionAttempt | Any | Security alert |
| BlockedContent | >20/hour | Check for false positives |

## Implementation

See Terraform configuration in `infrastructure/bedrock-guardrails.tf` for full implementation including:
- Guardrail resource definition with content policies
- PII entity configuration (SSN, credit card blocking)
- Custom regex patterns for AWS keys
- Python integration examples

## Testing

Test cases should verify:
- SSN patterns are blocked
- Email addresses are masked to [EMAIL]
- Code generation requests pass through
- Prompt injection attempts are flagged

## References

- [AWS Bedrock Guardrails Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- ADR-004: SigV4 Authentication
- CLAUDE.md Section: "NEVER LIE OR FABRICATE"
- Enterprise security policy (internal)
