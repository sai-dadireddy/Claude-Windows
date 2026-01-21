"""
Harvester Lambda for Sherpa Routing System

Nightly batch learning Lambda triggered by EventBridge.
Aggregates feedback data, computes model performance metrics,
and updates routing weights.

Schedule: cron(0 4 * * ? *) - 4 AM UTC daily

Tables:
- Input: sherpa-routing-feedback
- Output: sherpa-routing-metrics
"""

import json
import logging
import os
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import Dict, List, Any, Optional
from collections import defaultdict

import boto3
from boto3.dynamodb.conditions import Key, Attr

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Environment configuration
FEEDBACK_TABLE = os.environ.get('FEEDBACK_TABLE', 'sherpa-routing-feedback')
METRICS_TABLE = os.environ.get('METRICS_TABLE', 'sherpa-routing-metrics')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
LOOKBACK_DAYS = int(os.environ.get('LOOKBACK_DAYS', '7'))


class DecimalEncoder(json.JSONEncoder):
    """JSON encoder that handles Decimal types from DynamoDB."""
    def default(self, o):  # type: ignore[override]
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)


def get_dynamodb_resource():
    """Get DynamoDB resource with region configuration."""
    return boto3.resource('dynamodb', region_name=AWS_REGION)


def read_feedback_data(
    table,
    start_date: datetime,
    end_date: datetime
) -> List[Dict[str, Any]]:
    """
    Read feedback data from DynamoDB for the specified date range.

    Args:
        table: DynamoDB table resource
        start_date: Start of date range (inclusive)
        end_date: End of date range (exclusive)

    Returns:
        List of feedback records
    """
    feedback_items = []

    # Scan with filter for date range
    # Note: In production with large datasets, consider using a GSI on timestamp
    scan_kwargs = {
        'FilterExpression': Attr('timestamp').between(
            start_date.isoformat(),
            end_date.isoformat()
        )
    }

    done = False
    start_key = None

    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key

        response = table.scan(**scan_kwargs)
        feedback_items.extend(response.get('Items', []))

        start_key = response.get('LastEvaluatedKey')
        done = start_key is None

    logger.info(f"Read {len(feedback_items)} feedback records")
    return feedback_items


def aggregate_feedback(
    feedback_items: List[Dict[str, Any]]
) -> Dict[str, Dict[str, Any]]:
    """
    Aggregate feedback by model_id, task_type, and complexity.

    Args:
        feedback_items: List of raw feedback records

    Returns:
        Dictionary of aggregated metrics keyed by (model_id, task_type, complexity)
    """
    aggregations: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
        'success_count': 0,
        'total_count': 0,
        'latencies': [],
        'costs': [],
        'quality_scores': [],
        'feedback_ids': []
    })

    for item in feedback_items:
        model_id = item.get('model_id', 'unknown')
        task_type = item.get('task_type', 'general')
        complexity = item.get('complexity', 'medium')

        # Create composite key
        key = f"{model_id}#{task_type}#{complexity}"

        agg = aggregations[key]
        agg['total_count'] += 1

        # Track success
        if item.get('success', False):
            agg['success_count'] += 1

        # Collect metrics for averaging
        if 'latency_ms' in item:
            agg['latencies'].append(float(item['latency_ms']))

        if 'cost' in item:
            agg['costs'].append(float(item['cost']))

        if 'quality_score' in item:
            agg['quality_scores'].append(float(item['quality_score']))

        # Track feedback IDs for audit trail
        if 'feedback_id' in item:
            agg['feedback_ids'].append(item['feedback_id'])

    return aggregations


def compute_metrics(
    aggregations: Dict[str, Dict[str, Any]],
    batch_date: datetime
) -> List[Dict[str, Any]]:
    """
    Compute final metrics from aggregated data.

    Args:
        aggregations: Aggregated feedback data
        batch_date: Date of this batch run

    Returns:
        List of metric records ready for DynamoDB
    """
    metrics = []

    for key, agg in aggregations.items():
        parts = key.split('#')
        model_id = parts[0]
        task_type = parts[1] if len(parts) > 1 else 'general'
        complexity = parts[2] if len(parts) > 2 else 'medium'

        # Compute success rate
        success_rate = (
            agg['success_count'] / agg['total_count']
            if agg['total_count'] > 0 else 0.0
        )

        # Compute averages
        avg_latency = (
            sum(agg['latencies']) / len(agg['latencies'])
            if agg['latencies'] else 0.0
        )

        avg_cost = (
            sum(agg['costs']) / len(agg['costs'])
            if agg['costs'] else 0.0
        )

        avg_quality = (
            sum(agg['quality_scores']) / len(agg['quality_scores'])
            if agg['quality_scores'] else 0.0
        )

        # Compute routing weight (composite score)
        # Weight formula: quality * success_rate / (normalized_cost * normalized_latency)
        # Higher is better. Adjust weights as needed.
        routing_weight = compute_routing_weight(
            success_rate=success_rate,
            avg_quality=avg_quality,
            avg_latency=avg_latency,
            avg_cost=avg_cost
        )

        metric_record = {
            'metric_id': f"{model_id}#{task_type}#{complexity}",
            'model_id': model_id,
            'task_type': task_type,
            'complexity': complexity,
            'batch_date': batch_date.strftime('%Y-%m-%d'),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'success_rate': Decimal(str(round(success_rate, 4))),
            'avg_latency_ms': Decimal(str(round(avg_latency, 2))),
            'avg_cost': Decimal(str(round(avg_cost, 6))),
            'quality_score': Decimal(str(round(avg_quality, 4))),
            'routing_weight': Decimal(str(round(routing_weight, 4))),
            'sample_count': agg['total_count'],
            'success_count': agg['success_count'],
            'feedback_ids': agg['feedback_ids'][:100]  # Limit for storage
        }

        metrics.append(metric_record)

    logger.info(f"Computed metrics for {len(metrics)} model/task/complexity combinations")
    return metrics


def compute_routing_weight(
    success_rate: float,
    avg_quality: float,
    avg_latency: float,
    avg_cost: float
) -> float:
    """
    Compute routing weight from performance metrics.

    Formula balances quality, reliability, speed, and cost.
    Higher weight = more likely to be selected for routing.

    Args:
        success_rate: Task success rate (0-1)
        avg_quality: Average quality score (0-10)
        avg_latency: Average latency in ms
        avg_cost: Average cost per request

    Returns:
        Routing weight (0-1 normalized)
    """
    # Normalize inputs
    quality_norm = avg_quality / 10.0 if avg_quality > 0 else 0.5

    # Latency penalty (lower is better)
    # Normalize assuming 5000ms is very slow
    latency_factor = max(0.1, 1.0 - (avg_latency / 5000.0))

    # Cost penalty (lower is better)
    # Normalize assuming $0.10 is expensive
    cost_factor = max(0.1, 1.0 - (avg_cost / 0.10))

    # Weighted combination
    # Priorities: quality (35%), success (30%), latency (20%), cost (15%)
    weight = (
        0.35 * quality_norm +
        0.30 * success_rate +
        0.20 * latency_factor +
        0.15 * cost_factor
    )

    return min(1.0, max(0.0, weight))


def write_metrics(table, metrics: List[Dict[str, Any]]) -> int:
    """
    Write computed metrics to DynamoDB.

    Args:
        table: DynamoDB table resource
        metrics: List of metric records

    Returns:
        Number of records written
    """
    written = 0

    with table.batch_writer() as batch:
        for metric in metrics:
            try:
                batch.put_item(Item=metric)
                written += 1
            except Exception as e:
                logger.error(f"Failed to write metric {metric.get('metric_id')}: {e}")

    logger.info(f"Wrote {written}/{len(metrics)} metrics to {table.table_name}")
    return written


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler for nightly batch processing.

    Triggered by EventBridge schedule: cron(0 4 * * ? *)

    Args:
        event: EventBridge event (contains schedule metadata)
        context: Lambda context

    Returns:
        Processing summary with metrics counts
    """
    logger.info(f"Harvester Lambda started. Event: {json.dumps(event)}")

    try:
        # Determine date range for processing
        now = datetime.now(timezone.utc)
        end_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = end_date - timedelta(days=LOOKBACK_DAYS)

        logger.info(f"Processing feedback from {start_date} to {end_date}")

        # Initialize DynamoDB resources
        dynamodb = get_dynamodb_resource()
        feedback_table = dynamodb.Table(FEEDBACK_TABLE)  # type: ignore[union-attr]
        metrics_table = dynamodb.Table(METRICS_TABLE)  # type: ignore[union-attr]

        # Step 1: Read feedback data
        feedback_items = read_feedback_data(feedback_table, start_date, end_date)

        if not feedback_items:
            logger.info("No feedback data found for the specified period")
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'No feedback data to process',
                    'period': {
                        'start': start_date.isoformat(),
                        'end': end_date.isoformat()
                    },
                    'feedback_count': 0,
                    'metrics_written': 0
                })
            }

        # Step 2: Aggregate feedback by model/task/complexity
        aggregations = aggregate_feedback(feedback_items)

        # Step 3: Compute performance metrics
        metrics = compute_metrics(aggregations, end_date)

        # Step 4: Write metrics to DynamoDB
        metrics_written = write_metrics(metrics_table, metrics)

        # Prepare summary
        summary = {
            'message': 'Harvester batch completed successfully',
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'feedback_count': len(feedback_items),
            'unique_combinations': len(aggregations),
            'metrics_written': metrics_written,
            'models_processed': list(set(m['model_id'] for m in metrics)),
            'task_types_processed': list(set(m['task_type'] for m in metrics))
        }

        logger.info(f"Harvester completed: {json.dumps(summary)}")

        return {
            'statusCode': 200,
            'body': json.dumps(summary, cls=DecimalEncoder)
        }

    except Exception as e:
        logger.exception(f"Harvester failed: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'message': 'Harvester batch failed'
            })
        }


# For local testing
if __name__ == '__main__':
    # Simulate EventBridge event
    test_event = {
        'source': 'aws.events',
        'detail-type': 'Scheduled Event',
        'detail': {}
    }

    result = lambda_handler(test_event, None)
    print(json.dumps(result, indent=2))
