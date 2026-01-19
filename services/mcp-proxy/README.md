# Sherpa v4.1 MCP Proxy

Thin MCP proxy for Sherpa AWS Lambda endpoints with IAM SigV4 signing.

## Overview

This proxy provides MCP tools that route to Sherpa's AWS Lambda backend:
- `/mcp/*` - Router for backend MCPs
- `/memory/*` - Memory CRUD operations
- `/beads/*` - Beads task tracker sync
- `/kb/*` - Knowledge base retrieval (Workday/Oracle)

## Setup

### 1. Install Dependencies
```bash
cd services/mcp-proxy
npm install
```

### 2. Configure AWS Credentials

Ensure you have the `sherpa` profile configured in `~/.aws/credentials`:

```ini
[sherpa]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
# Optional: aws_session_token = YOUR_SESSION_TOKEN
```

### 3. Test Authentication
```bash
npm start
# Should show: [MCP-Proxy] Authenticated as: arn:aws:iam::...
```

## MCP Tools

### router_execute
Execute tool on backend MCP via Sherpa router.

```javascript
{
  "mcp_name": "context7",
  "tool_name": "get-library-docs",
  "arguments": {
    "context7CompatibleLibraryID": "/vercel/next.js"
  }
}
```

### memory_search
Search Sherpa memory system.

```javascript
{
  "query": "database migration",
  "project": "myproject",  // optional
  "type": "decision",      // optional: decision, preference, observation
  "limit": 10              // optional, default: 10
}
```

### memory_save
Save memory to Sherpa system.

```javascript
{
  "project": "myproject",
  "type": "decision",
  "content": "Using PostgreSQL for primary database",
  "metadata": {}  // optional
}
```

### beads_sync
Sync with Beads task tracker.

```javascript
{
  "action": "list",  // list, create, update, close
  "data": {}
}
```

### kb_retrieve
Retrieve from knowledge base.

```javascript
{
  "kb_name": "workday",  // workday, oracle
  "query": "WSDL operations",
  "top_k": 5  // optional, default: 5
}
```

## Architecture

```
Claude Code MCP Client
        ↓
  mcp-proxy (stdio)
        ↓
  SigV4 Signing
        ↓
  AWS API Gateway (IAM auth)
        ↓
  Lambda Functions
```

## Configuration

- **AWS Region**: us-east-1
- **AWS Profile**: sherpa
- **API Endpoint**: https://hl98rmqgd6.execute-api.us-east-1.amazonaws.com/prod

## Troubleshooting

### Authentication Failed
```bash
# Verify AWS profile exists
aws sts get-caller-identity --profile sherpa

# Check credentials
cat ~/.aws/credentials | grep -A 3 "\[sherpa\]"
```

### Connection Errors
- Ensure API Gateway endpoint is accessible
- Check IAM permissions for execute-api:Invoke
- Verify security group rules allow HTTPS outbound

## Development

The proxy is intentionally minimal - all business logic lives in Lambda.

Key files:
- `index.js` - Main proxy (~150 lines)
- `package.json` - Dependencies
- `test/index.test.js` - Unit tests

## Testing

### Install Dependencies
```bash
npm install
```

### Run Tests
```bash
# Run all tests
npm test

# Run tests in watch mode (re-runs on file changes)
npm run test:watch

# Run tests with coverage report
npm run test:coverage
```

### Test Structure

The test suite covers:

1. **Credential Loading**
   - AWS profile loading
   - Credential caching
   - Missing credentials handling
   - Session token support

2. **SigV4 Signing**
   - Request signing with correct parameters
   - Session token inclusion
   - Service name verification

3. **Tool Routing**
   - `router_execute` - MCP router endpoint
   - `memory_search` - Memory search with defaults
   - `memory_save` - Memory persistence
   - `beads_sync` - Task tracker sync (list, create, update, close)
   - `kb_retrieve` - Knowledge base retrieval (workday, oracle)

4. **MCP Message Handling**
   - Initialize response format
   - Tools list response
   - Tool call success/error formatting

5. **Error Handling**
   - Unknown tool errors
   - API errors (4xx, 5xx)
   - JSON parse errors
   - Network errors

6. **Edge Cases**
   - Empty/null inputs
   - Unicode content
   - Large payloads
   - Special characters
   - Nested JSON

### Mocking Strategy

Tests use Jest's ES module mocking (`jest.unstable_mockModule`) to mock:
- `@aws-sdk/credential-providers` - AWS credential loading
- `@aws-sdk/client-sts` - STS client for identity verification
- `aws4` - SigV4 signing library
- `https` - HTTP requests

Example mock credentials used in tests:
```javascript
const mockCredentials = {
  accessKeyId: 'AKIAIOSFODNN7EXAMPLE',
  secretAccessKey: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
  sessionToken: 'AQoDYXdzEJr...'
};
```

## License

MIT
