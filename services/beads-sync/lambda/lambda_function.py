#!/usr/bin/env python3
"""
Lambda Beads Sync - Sherpa v4.1
CRUD operations for team beads coordination via DynamoDB.
"""

import json
import logging
import traceback
import boto3
from datetime import datetime
from decimal import Decimal

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('sherpa-beads')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)

def lambda_handler(event, context):
    """Handle beads sync operations."""
    try:
        # Parse request
        body = json.loads(event.get('body', '{}')) if isinstance(event.get('body'), str) else event.get('body', {})
        path = event.get('rawPath', event.get('path', ''))
        method = event.get('requestContext', {}).get('http', {}).get('method', 'POST')
        
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
        else:
            return response(400, {'error': f'Unknown operation: {path}'})
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        logger.error(traceback.format_exc())
        return response(500, {'error': str(e), 'type': type(e).__name__})

def list_beads(body):
    """List beads for a project."""
    project = body.get('project', 'default')
    status_filter = body.get('status')
    
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
    """Get a single bead by ID."""
    project = body.get('project', 'default')
    bead_id = body.get('id')
    
    if not bead_id:
        return response(400, {'error': 'Missing bead id'})
    
    result = table.get_item(Key={'PK': f'PROJ#{project}', 'SK': f'BEAD#{bead_id}'})
    item = result.get('Item')
    
    if not item:
        return response(404, {'error': f'Bead {bead_id} not found'})
    
    return response(200, item)

def create_bead(body):
    """Create a new bead."""
    project = body.get('project', 'default')
    bead_id = body.get('id')
    
    if not bead_id:
        return response(400, {'error': 'Missing bead id'})
    
    item = {
        'PK': f'PROJ#{project}',
        'SK': f'BEAD#{bead_id}',
        'id': bead_id,
        'title': body.get('title', ''),
        'description': body.get('description', ''),
        'status': body.get('status', 'open'),
        'priority': body.get('priority', 1),
        'issue_type': body.get('issue_type', 'task'),
        'labels': body.get('labels', []),
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat(),
        'created_by': body.get('created_by', 'system')
    }
    
    table.put_item(Item=item)
    return response(201, {'created': bead_id})

def update_bead(body):
    """Update an existing bead."""
    project = body.get('project', 'default')
    bead_id = body.get('id')

    if not bead_id:
        return response(400, {'error': 'Missing bead id'})

    updates = []
    values = {':updated': datetime.utcnow().isoformat()}
    names = {}

    for field in ['title', 'description', 'status', 'priority', 'labels']:
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

    return response(200, {'updated': bead_id})

def delete_bead(body):
    """Delete a bead."""
    project = body.get('project', 'default')
    bead_id = body.get('id')
    
    if not bead_id:
        return response(400, {'error': 'Missing bead id'})
    
    table.delete_item(Key={'PK': f'PROJ#{project}', 'SK': f'BEAD#{bead_id}'})
    return response(200, {'deleted': bead_id})

def sync_beads(body):
    """Bulk sync beads from client."""
    project = body.get('project', 'default')
    items = body.get('items', [])
    
    with table.batch_writer() as batch:
        for item in items:
            item['PK'] = f'PROJ#{project}'
            item['SK'] = f'BEAD#{item.get("id")}'
            item['updated_at'] = datetime.utcnow().isoformat()
            batch.put_item(Item=item)
    
    return response(200, {'synced': len(items)})

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body, cls=DecimalEncoder)
    }
