# Beads Sync Client

Client library for syncing beads to AWS Lambda backend via API Gateway (Sherpa v4.1).

## Architecture

- **API Gateway**: `https://hl98rmqgd6.execute-api.us-east-1.amazonaws.com/prod/beads`
- **Lambda**: `sherpa-beads-sync`
- **DynamoDB**: `sherpa-beads` table
  - PK: `PROJ#{project}`
  - SK: `BEAD#{id}`
- **Auth**: IAM with SigV4 signing
- **Region**: `us-east-1`
- **Profile**: `sherpa`

## Installation

```bash
pip install boto3 requests pyyaml
```

## Configuration

1. Copy example config:
```bash
cp config.example.yaml config.yaml
```

2. Ensure AWS credentials are configured:
```bash
# Check ~/.aws/credentials has [sherpa] profile
aws configure --profile sherpa
```

## Usage

### Basic Example

```python
from sync_client import BeadsSyncClient

# Initialize client
client = BeadsSyncClient(
    api_endpoint="https://hl98rmqgd6.execute-api.us-east-1.amazonaws.com/prod/beads",
    region="us-east-1",
    profile="sherpa"
)

# Sync a bead
bead_data = {
    'id': 'bead-123',
    'title': 'Implement feature X',
    'status': 'in_progress',
    'priority': 1
}
response = client.sync_bead('my-project', bead_data)
print(f"Synced: {response}")

# Get all beads for a project
beads = client.get_beads('my-project')
print(f"Found {len(beads)} beads")

# Delete a bead
response = client.delete_bead('my-project', 'bead-123')
print(f"Deleted: {response}")
```

### Using Config File

```python
from sync_client import BeadsSyncClient, load_config

# Load from config.yaml
config = load_config('config.yaml')
client = BeadsSyncClient(**config)

# Use client
beads = client.get_beads('my-project')
```

### Error Handling

```python
from requests import HTTPError

try:
    client.sync_bead('my-project', {'id': 'test', 'title': 'Test'})
except ValueError as e:
    print(f"Invalid bead data: {e}")
except HTTPError as e:
    print(f"API error: {e.response.status_code} - {e.response.text}")
```

## API Methods

### `sync_bead(project, bead_data)`

Sync a single bead to the backend (create or update).

**Args:**
- `project` (str): Project identifier
- `bead_data` (dict): Bead data (must include 'id' field)

**Returns:** API response dict

**Raises:**
- `ValueError`: If bead_data missing 'id' field
- `requests.HTTPError`: If API request fails

### `get_beads(project)`

Retrieve all beads for a project.

**Args:**
- `project` (str): Project identifier

**Returns:** List of bead dictionaries

**Raises:**
- `requests.HTTPError`: If API request fails

### `delete_bead(project, bead_id)`

Delete a bead from the backend.

**Args:**
- `project` (str): Project identifier
- `bead_id` (str): Bead ID to delete

**Returns:** API response dict

**Raises:**
- `requests.HTTPError`: If API request fails

## Authentication

The client uses AWS SigV4 signing for IAM authentication. Ensure your AWS credentials have the necessary permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "execute-api:Invoke"
      ],
      "Resource": "arn:aws:execute-api:us-east-1:*:*/prod/POST/beads"
    }
  ]
}
```

## DynamoDB Schema

Beads are stored with composite keys:

- **Partition Key**: `PROJ#{project}` (e.g., `PROJ#my-project`)
- **Sort Key**: `BEAD#{id}` (e.g., `BEAD#bead-123`)

This allows efficient querying of all beads for a project.

## Troubleshooting

### Credentials Not Found

```
NoCredentialsError: Unable to locate credentials
```

**Solution:** Configure AWS credentials for the sherpa profile:
```bash
aws configure --profile sherpa
```

### 403 Forbidden

```
HTTPError: 403 Client Error: Forbidden
```

**Solution:** Ensure your IAM user/role has `execute-api:Invoke` permission for the API Gateway.

### Connection Timeout

```
ConnectionError: Max retries exceeded
```

**Solution:** Check network connectivity and API Gateway endpoint URL.

## Integration with Beads CLI

To integrate with the local beads system:

```python
import json
from pathlib import Path
from sync_client import BeadsSyncClient

# Initialize client
client = BeadsSyncClient(profile='sherpa')

# Load local beads
beads_dir = Path('.beads')
project = 'my-project'

# Sync all local beads
for bead_file in beads_dir.glob('*.json'):
    with open(bead_file) as f:
        bead_data = json.load(f)
    client.sync_bead(project, bead_data)
    print(f"Synced {bead_data['id']}")

# Pull remote beads
remote_beads = client.get_beads(project)
for bead in remote_beads:
    bead_file = beads_dir / f"{bead['id']}.json"
    with open(bead_file, 'w') as f:
        json.dump(bead, f, indent=2)
    print(f"Pulled {bead['id']}")
```

## Testing

### Installation

Install test dependencies:

```bash
pip install pytest pytest-cov
```

Or install all dependencies including test requirements:

```bash
pip install -r requirements.txt -r requirements-test.txt
```

### Running Tests

Run all tests:

```bash
# From the beads-sync directory
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ -v --cov=sync_client --cov-report=term-missing
```

Run specific test classes:

```bash
# Test initialization
pytest tests/test_sync_client.py::TestBeadsSyncClientInitialization -v

# Test CRUD operations
pytest tests/test_sync_client.py::TestListBeads -v
pytest tests/test_sync_client.py::TestGetBead -v
pytest tests/test_sync_client.py::TestCreateBead -v
pytest tests/test_sync_client.py::TestUpdateBead -v
pytest tests/test_sync_client.py::TestDeleteBead -v
pytest tests/test_sync_client.py::TestSyncBeads -v

# Test edge cases
pytest tests/test_sync_client.py::TestEdgeCases -v
```

Run tests matching a pattern:

```bash
pytest tests/ -v -k "create or update"
```

### Test Coverage

The test suite covers:

- **Initialization**: Default parameters, custom parameters, URL normalization, credential storage
- **API Methods**: list_beads, get_bead, create_bead, update_bead, delete_bead, sync_beads
- **Error Handling**: HTTP errors, missing required fields, file not found
- **Edge Cases**: Special characters, Unicode, large payloads, empty inputs
- **Status Filters**: All valid status values (open, in_progress, closed)

### Mocking Strategy

Tests use mocked AWS credentials and HTTP requests to avoid:
- Requiring actual AWS credentials
- Making real API calls
- Incurring AWS costs during testing

The mocks are provided via pytest fixtures in `tests/conftest.py`.

## License

Part of Sherpa v4.1 project.
