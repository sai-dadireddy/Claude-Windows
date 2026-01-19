# ADR-004: SigV4 Authentication for API Gateway

## Status

**Accepted** - January 2025

## Context

Sherpa's AWS backend exposes APIs for:
- Memory storage and retrieval (DynamoDB)
- Knowledge base access (S3)
- Secret retrieval (Secrets Manager)
- Usage analytics

These APIs need authentication that:
1. Works from CLI environments (no browser OAuth flow)
2. Integrates with existing AWS IAM
3. Provides fine-grained access control
4. Does not require managing separate credentials
5. Supports temporary credentials (SSO, assumed roles)

Options considered:

| Method | Pros | Cons |
|--------|------|------|
| API Keys | Simple | No IAM integration, manual rotation |
| Cognito | User pools | Overkill, requires user management |
| OAuth 2.0 | Standard | Requires browser flow |
| **SigV4** | IAM native, CLI-friendly | Slightly complex signing |
| Lambda authorizers | Flexible | Additional Lambda costs |

## Decision

Use AWS Signature Version 4 (SigV4) authentication for all API Gateway endpoints.

### Architecture

```
+-------------+     SigV4 Signed Request      +---------------+
|   Claude    | ----------------------------> |  API Gateway  |
|   Code      |                               |  (IAM Auth)   |
+-------------+                               +---------------+
      |                                              |
      | AWS Credentials                              v
      | (from ~/.aws/ or env)                +---------------+
      v                                      |    Lambda     |
+-------------+                              +---------------+
| AWS SDK     |                                     |
| (boto3)     |                                     v
+-------------+                              +---------------+
                                             |  DynamoDB /   |
                                             |  S3 / Secrets |
                                             +---------------+
```

### IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "execute-api:Invoke",
      "Resource": [
        "arn:aws:execute-api:us-east-1:*:*/prod/GET/memories/*",
        "arn:aws:execute-api:us-east-1:*:*/prod/POST/memories",
        "arn:aws:execute-api:us-east-1:*:*/prod/GET/knowledge/*"
      ]
    }
  ]
}
```

### Request Flow

1. **Credential Resolution**
   - Check environment variables (`AWS_ACCESS_KEY_ID`, etc.)
   - Check `~/.aws/credentials` profile
   - Check EC2 instance metadata (if applicable)
   - Check SSO session cache

2. **Request Signing**
   ```python
   from botocore.auth import SigV4Auth
   from botocore.awsrequest import AWSRequest

   request = AWSRequest(method='GET', url=api_url, headers=headers)
   SigV4Auth(credentials, 'execute-api', region).add_auth(request)
   ```

3. **API Gateway Validation**
   - Extracts signature from Authorization header
   - Validates against IAM
   - Checks policy permissions
   - Forwards to Lambda if authorized

4. **Response**
   - Success: JSON payload
   - Auth failure: 403 Forbidden
   - Policy denial: 403 with specific message

## Implementation

### Client-Side (Python)

```python
import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import requests

def call_sherpa_api(endpoint: str, method: str = 'GET', body: dict = None):
    session = boto3.Session()
    credentials = session.get_credentials()

    url = f"https://sherpa-api.execute-api.us-east-1.amazonaws.com/prod{endpoint}"

    request = AWSRequest(
        method=method,
        url=url,
        data=json.dumps(body) if body else None,
        headers={'Content-Type': 'application/json'}
    )

    SigV4Auth(credentials, 'execute-api', 'us-east-1').add_auth(request)

    response = requests.request(
        method=method,
        url=url,
        headers=dict(request.headers),
        data=request.body
    )

    return response.json()
```

### API Gateway Configuration (Terraform)

```hcl
resource "aws_api_gateway_rest_api" "sherpa" {
  name = "sherpa-api"
}

resource "aws_api_gateway_method" "memories_get" {
  rest_api_id   = aws_api_gateway_rest_api.sherpa.id
  resource_id   = aws_api_gateway_resource.memories.id
  http_method   = "GET"
  authorization = "AWS_IAM"
}

resource "aws_api_gateway_method" "memories_post" {
  rest_api_id   = aws_api_gateway_rest_api.sherpa.id
  resource_id   = aws_api_gateway_resource.memories.id
  http_method   = "POST"
  authorization = "AWS_IAM"
}
```

## Consequences

### Positive

- **No separate credentials**: Uses existing AWS credentials
- **Fine-grained access**: IAM policies control per-endpoint access
- **SSO compatible**: Works with AWS SSO temporary credentials
- **Audit trail**: CloudTrail logs all API calls with IAM identity
- **CLI-native**: No browser required, works in headless environments
- **Secure**: Request signing prevents tampering and replay attacks

### Negative

- **AWS lock-in**: Tightly coupled to AWS IAM
- **Complexity**: SigV4 signing is non-trivial to implement
- **Clock sensitivity**: Requests fail if client clock is >5 minutes off
- **Credential management**: Users must configure AWS credentials

### Mitigations

- Provide helper library that handles signing
- Document credential setup in README
- NTP sync recommendation in setup guide
- Fallback to API keys for non-AWS environments (future)

## Security Considerations

1. **Credential Storage**: Never log or store credentials in plaintext
2. **Least Privilege**: IAM policies grant minimal required permissions
3. **Rotation**: Supports credential rotation without code changes
4. **MFA**: Can require MFA for sensitive operations via IAM conditions
5. **VPC Endpoints**: Option to restrict to VPC for additional isolation

## API Endpoints

| Endpoint | Method | Purpose | Required Permission |
|----------|--------|---------|---------------------|
| `/memories` | GET | List memories | `execute-api:Invoke` |
| `/memories` | POST | Save memory | `execute-api:Invoke` |
| `/memories/{id}` | GET | Get specific memory | `execute-api:Invoke` |
| `/knowledge/{kb}` | GET | Query knowledge base | `execute-api:Invoke` |
| `/secrets/{name}` | GET | Retrieve secret | `execute-api:Invoke` + condition |

## References

- [AWS SigV4 Documentation](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html)
- ADR-002: Hybrid Storage Strategy
- ADR-005: Bedrock Guardrails (for content filtering)
