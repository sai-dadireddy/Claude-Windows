#!/usr/bin/env python3
"""
Lambda Beads Sync - Sherpa v4.2
CRUD operations for team beads coordination via DynamoDB.
Now supports project_id isolation via sherpa-project-membership table.
"""

import json
import logging
import traceback
import os
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
from decimal import Decimal

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('sherpa-beads')

# Project membership table for access control
MEMBERSHIP_TABLE = os.environ.get('MEMBERSHIP_TABLE', 'sherpa-project-membership')
membership_table = dynamodb.Table(MEMBERSHIP_TABLE)

# Projects that bypass access checks
BYPASS_PROJECTS = {'shared', 'global', 'public'}

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)


def get_caller_email(event: dict) -> str:
    """Extract user email from Lambda event context."""
    # Try requestContext identity (API Gateway with IAM/SSO)
    request_context = event.get('requestContext', {})
    identity = request_context.get('identity', {})
    user_arn = identity.get('userArn', '')
    if user_arn and '@' in user_arn:
        email = user_arn.split('/')[-1]
        if '@' in email:
            return email

    # Try body user_email field
    body = event.get('body', {})
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except:
            body = {}
    if body.get('user_email'):
        return body['user_email']

    # Try direct event user_email
    if event.get('user_email'):
        return event['user_email']

    return 'anonymous'


def get_user_projects(email: str) -> set:
    """Get all projects a user has access to."""
    if email == 'anonymous':
        return set(BYPASS_PROJECTS)

    allowed = set(BYPASS_PROJECTS)

    try:
        response = membership_table.query(
            KeyConditionExpression=Key('PK').eq(f'USER#{email}')
        )
        for item in response.get('Items', []):
            sk = item.get('SK', '')
            if sk.startswith('PROJ#'):
                allowed.add(sk.replace('PROJ#', ''))
    except Exception as e:
        logger.error(f"Failed to get user projects: {e}")

    return allowed


def can_access_project(email: str, project_id: str) -> bool:
    """Check if user can access a project."""
    if project_id in BYPASS_PROJECTS:
        return True
    return project_id in get_user_projects(email)

def lambda_handler(event, context):
    """Handle beads sync operations with project isolation."""
    try:
        # Parse request
        body = json.loads(event.get('body', '{}')) if isinstance(event.get('body'), str) else event.get('body', {})
        path = event.get('rawPath', event.get('path', ''))
        method = event.get('requestContext', {}).get('http', {}).get('method', 'POST')

        # Get caller email for access control
        caller_email = get_caller_email(event)
        logger.info(json.dumps({'event': 'request', 'caller': caller_email, 'path': path}))

        # Inject caller email into body for downstream functions
        body['_caller_email'] = caller_email

        # Route operations
        if '/beads/list' in path or body.get('operation') == 'list':
            return list_beads(body)
        elif '/beads/get' in path or body.get('operation') == 'get':
            return get_bead(body)
        elif '/beads/create' in path or body.get('operation') == 'create':
            return create_bead(body)
        elif '/beads/update' in path or body.get('operation') == 'update':
            return update_bead(body)
        elif '/beads/delete' in path or body.get('operation') == 'delete':
            return delete_bead(body)
        elif '/beads/sync' in path or body.get('operation') == 'sync':
            return sync_beads(body)
        elif '/beads/projects' in path or body.get('operation') == 'projects':
            return list_user_projects(body)
        else:
            return response(400, {'error': f'Unknown operation: {path}'})
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        logger.error(traceback.format_exc())
        return response(500, {'error': str(e), 'type': type(e).__name__})

def list_beads(body):
    """List beads for a project (enforces project access)."""
    project = body.get('project', 'default')
    status_filter = body.get('status')
    caller_email = body.get('_caller_email', 'anonymous')

    # Enforce project access
    if not can_access_project(caller_email, project):
        logger.warning(json.dumps({
            'event': 'access_denied',
            'caller': caller_email,
            'project': project,
            'operation': 'list'
        }))
        return response(403, {'error': f'Access denied to project: {project}'})

    if status_filter:
        # Use GSI for status queries
        result = table.query(
            IndexName='status-index',
            KeyConditionExpression='#s = :status',
            FilterExpression='begins_with(SK, :sk_prefix)',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':status': status_filter, ':sk_prefix': f'BEAD#'}
        )
    else:
        result = table.query(
            KeyConditionExpression='PK = :pk',
            ExpressionAttributeValues={':pk': f'PROJ#{project}'}
        )

    return response(200, {'items': result.get('Items', []), 'count': result.get('Count', 0)})

def get_bead(body):
    """Get a single bead by ID (enforces project access)."""
    project = body.get('project', 'default')
    bead_id = body.get('id')
    caller_email = body.get('_caller_email', 'anonymous')

    # Enforce project access
    if not can_access_project(caller_email, project):
        return response(403, {'error': f'Access denied to project: {project}'})

    if not bead_id:
        return response(400, {'error': 'Missing bead id'})

    result = table.get_item(Key={'PK': f'PROJ#{project}', 'SK': f'BEAD#{bead_id}'})
    item = result.get('Item')

    if not item:
        return response(404, {'error': f'Bead {bead_id} not found'})

    return response(200, item)

def create_bead(body):
    """Create a new bead (enforces project access)."""
    project = body.get('project', 'default')
    bead_id = body.get('id')
    caller_email = body.get('_caller_email', 'anonymous')

    # Enforce project access
    if not can_access_project(caller_email, project):
        logger.warning(json.dumps({
            'event': 'access_denied',
            'caller': caller_email,
            'project': project,
            'operation': 'create'
        }))
        return response(403, {'error': f'Access denied to project: {project}'})

    if not bead_id:
        return response(400, {'error': 'Missing bead id'})

    item = {
        'PK': f'PROJ#{project}',
        'SK': f'BEAD#{bead_id}',
        'id': bead_id,
        'project_id': project,  # v4.2: Explicit project_id column
        'title': body.get('title', ''),
        'description': body.get('description', ''),
        'status': body.get('status', 'open'),
        'priority': body.get('priority', 1),
        'issue_type': body.get('issue_type', 'task'),
        'labels': body.get('labels', []),
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat(),
        'created_by': body.get('created_by', caller_email)
    }

    table.put_item(Item=item)
    logger.info(json.dumps({'event': 'bead_created', 'id': bead_id, 'project': project, 'caller': caller_email}))
    return response(201, {'created': bead_id})

def update_bead(body):
    """Update an existing bead (enforces project access)."""
    project = body.get('project', 'default')
    bead_id = body.get('id')
    caller_email = body.get('_caller_email', 'anonymous')

    # Enforce project access
    if not can_access_project(caller_email, project):
        return response(403, {'error': f'Access denied to project: {project}'})

    if not bead_id:
        return response(400, {'error': 'Missing bead id'})

    updates = []
    values = {':updated': datetime.utcnow().isoformat()}
    names = {}

    for field in ['title', 'description', 'status', 'priority', 'labels', 'project_id']:
        if field in body:
            updates.append(f'#{field} = :{field}')
            values[f':{field}'] = body[field]
            names[f'#{field}'] = field

    updates.append('updated_at = :updated')

    # Build update_item kwargs - only include ExpressionAttributeNames if non-empty
    update_kwargs = {
        'Key': {'PK': f'PROJ#{project}', 'SK': f'BEAD#{bead_id}'},
        'UpdateExpression': 'SET ' + ', '.join(updates),
        'ExpressionAttributeValues': values
    }
    if names:
        update_kwargs['ExpressionAttributeNames'] = names

    table.update_item(**update_kwargs)
    logger.info(json.dumps({'event': 'bead_updated', 'id': bead_id, 'project': project, 'caller': caller_email}))

    return response(200, {'updated': bead_id})

def delete_bead(body):
    """Delete a bead (enforces project access)."""
    project = body.get('project', 'default')
    bead_id = body.get('id')
    caller_email = body.get('_caller_email', 'anonymous')

    # Enforce project access
    if not can_access_project(caller_email, project):
        return response(403, {'error': f'Access denied to project: {project}'})

    if not bead_id:
        return response(400, {'error': 'Missing bead id'})

    table.delete_item(Key={'PK': f'PROJ#{project}', 'SK': f'BEAD#{bead_id}'})
    logger.info(json.dumps({'event': 'bead_deleted', 'id': bead_id, 'project': project, 'caller': caller_email}))
    return response(200, {'deleted': bead_id})

def sync_beads(body):
    """Bulk sync beads from client (enforces project access)."""
    project = body.get('project', 'default')
    items = body.get('items', [])
    caller_email = body.get('_caller_email', 'anonymous')

    # Enforce project access
    if not can_access_project(caller_email, project):
        logger.warning(json.dumps({
            'event': 'access_denied',
            'caller': caller_email,
            'project': project,
            'operation': 'sync',
            'item_count': len(items)
        }))
        return response(403, {'error': f'Access denied to project: {project}'})

    synced = 0
    with table.batch_writer() as batch:
        for item in items:
            item['PK'] = f'PROJ#{project}'
            item['SK'] = f'BEAD#{item.get("id")}'
            item['project_id'] = project  # v4.2: Explicit project_id column
            item['updated_at'] = datetime.utcnow().isoformat()
            batch.put_item(Item=item)
            synced += 1

    logger.info(json.dumps({'event': 'beads_synced', 'project': project, 'count': synced, 'caller': caller_email}))
    return response(200, {'synced': synced})


def list_user_projects(body):
    """List all projects the caller has access to."""
    caller_email = body.get('_caller_email', 'anonymous')

    projects = list(get_user_projects(caller_email))

    return response(200, {
        'user': caller_email,
        'projects': sorted(projects),
        'count': len(projects)
    })

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body, cls=DecimalEncoder)
    }
