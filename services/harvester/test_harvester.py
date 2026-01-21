"""
Tests for Harvester Lambda

Run with: pytest test_harvester.py -v
"""

import json
import pytest
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from unittest.mock import MagicMock, patch, ANY

# Import module under test
from lambda_function import (
    lambda_handler,
    read_feedback_data,
    aggregate_feedback,
    compute_metrics,
    compute_routing_weight,
    write_metrics,
    DecimalEncoder
)


class TestDecimalEncoder:
    """Tests for DecimalEncoder JSON encoder."""

    def test_encodes_decimal_to_float(self):
        encoder = DecimalEncoder()
        result = encoder.default(Decimal('123.456'))
        assert result == 123.456

    def test_raises_for_non_decimal(self):
        encoder = DecimalEncoder()
        with pytest.raises(TypeError):
            encoder.default(object())

    def test_json_dumps_with_decimal(self):
        data = {'value': Decimal('0.1234')}
        result = json.dumps(data, cls=DecimalEncoder)
        assert result == '{"value": 0.1234}'


class TestAggregateFeedback:
    """Tests for feedback aggregation logic."""

    def test_aggregates_by_model_task_complexity(self):
        feedback = [
            {
                'model_id': 'claude-sonnet',
                'task_type': 'coding',
                'complexity': 'high',
                'success': True,
                'latency_ms': 1000,
                'cost': 0.01,
                'quality_score': 8.5,
                'feedback_id': 'fb-001'
            },
            {
                'model_id': 'claude-sonnet',
                'task_type': 'coding',
                'complexity': 'high',
                'success': True,
                'latency_ms': 1200,
                'cost': 0.012,
                'quality_score': 9.0,
                'feedback_id': 'fb-002'
            },
            {
                'model_id': 'gpt-4o',
                'task_type': 'coding',
                'complexity': 'high',
                'success': False,
                'latency_ms': 800,
                'cost': 0.008,
                'quality_score': 6.0,
                'feedback_id': 'fb-003'
            }
        ]

        result = aggregate_feedback(feedback)

        assert len(result) == 2
        assert 'claude-sonnet#coding#high' in result
        assert 'gpt-4o#coding#high' in result

        sonnet_agg = result['claude-sonnet#coding#high']
        assert sonnet_agg['total_count'] == 2
        assert sonnet_agg['success_count'] == 2
        assert sonnet_agg['latencies'] == [1000, 1200]
        assert sonnet_agg['costs'] == [0.01, 0.012]

    def test_handles_missing_fields(self):
        feedback = [
            {'model_id': 'test-model', 'success': True},
            {'success': False}  # Missing model_id
        ]

        result = aggregate_feedback(feedback)

        # Should use defaults for missing fields
        assert 'test-model#general#medium' in result
        assert 'unknown#general#medium' in result

    def test_empty_feedback_list(self):
        result = aggregate_feedback([])
        assert result == {}


class TestComputeRoutingWeight:
    """Tests for routing weight computation."""

    def test_perfect_scores_give_high_weight(self):
        weight = compute_routing_weight(
            success_rate=1.0,
            avg_quality=10.0,
            avg_latency=100,
            avg_cost=0.001
        )
        # High quality, high success, low latency, low cost = high weight
        assert weight > 0.9

    def test_poor_scores_give_low_weight(self):
        weight = compute_routing_weight(
            success_rate=0.2,
            avg_quality=2.0,
            avg_latency=4000,
            avg_cost=0.08
        )
        # Low quality, low success, high latency, high cost = low weight
        assert weight < 0.4

    def test_weight_bounded_0_to_1(self):
        # Test edge cases
        weight1 = compute_routing_weight(0, 0, 10000, 1.0)
        weight2 = compute_routing_weight(1.0, 10.0, 0, 0)

        assert 0.0 <= weight1 <= 1.0
        assert 0.0 <= weight2 <= 1.0

    def test_balanced_metrics(self):
        weight = compute_routing_weight(
            success_rate=0.8,
            avg_quality=7.5,
            avg_latency=1500,
            avg_cost=0.02
        )
        # Reasonable metrics should give moderate weight
        assert 0.5 < weight < 0.9


class TestComputeMetrics:
    """Tests for metrics computation from aggregations."""

    def test_computes_averages_correctly(self):
        aggregations = {
            'model-a#task-x#low': {
                'success_count': 8,
                'total_count': 10,
                'latencies': [100, 200, 150, 180],
                'costs': [0.01, 0.02, 0.015, 0.012],
                'quality_scores': [8.0, 9.0, 7.5, 8.5],
                'feedback_ids': ['fb-1', 'fb-2', 'fb-3', 'fb-4']
            }
        }

        batch_date = datetime(2024, 1, 15, tzinfo=timezone.utc)
        metrics = compute_metrics(aggregations, batch_date)

        assert len(metrics) == 1
        metric = metrics[0]

        assert metric['metric_id'] == 'model-a#task-x#low'
        assert metric['model_id'] == 'model-a'
        assert metric['task_type'] == 'task-x'
        assert metric['complexity'] == 'low'
        assert metric['batch_date'] == '2024-01-15'
        assert float(metric['success_rate']) == 0.8
        assert float(metric['avg_latency_ms']) == 157.5  # (100+200+150+180)/4
        assert metric['sample_count'] == 10
        assert metric['success_count'] == 8

    def test_handles_empty_metrics_lists(self):
        aggregations = {
            'model-b#task-y#medium': {
                'success_count': 5,
                'total_count': 5,
                'latencies': [],  # No latency data
                'costs': [],
                'quality_scores': [],
                'feedback_ids': []
            }
        }

        batch_date = datetime(2024, 1, 15, tzinfo=timezone.utc)
        metrics = compute_metrics(aggregations, batch_date)

        metric = metrics[0]
        assert float(metric['avg_latency_ms']) == 0.0
        assert float(metric['avg_cost']) == 0.0
        assert float(metric['quality_score']) == 0.0


class TestReadFeedbackData:
    """Tests for DynamoDB feedback reading."""

    def test_reads_with_pagination(self):
        mock_table = MagicMock()

        # Simulate paginated response
        mock_table.scan.side_effect = [
            {
                'Items': [{'id': '1'}, {'id': '2'}],
                'LastEvaluatedKey': {'pk': 'key1'}
            },
            {
                'Items': [{'id': '3'}],
                # No LastEvaluatedKey = done
            }
        ]

        start = datetime(2024, 1, 1, tzinfo=timezone.utc)
        end = datetime(2024, 1, 8, tzinfo=timezone.utc)

        result = read_feedback_data(mock_table, start, end)

        assert len(result) == 3
        assert mock_table.scan.call_count == 2

    def test_empty_result(self):
        mock_table = MagicMock()
        mock_table.scan.return_value = {'Items': []}

        start = datetime(2024, 1, 1, tzinfo=timezone.utc)
        end = datetime(2024, 1, 8, tzinfo=timezone.utc)

        result = read_feedback_data(mock_table, start, end)

        assert result == []


class TestWriteMetrics:
    """Tests for writing metrics to DynamoDB."""

    def test_writes_all_metrics(self):
        mock_table = MagicMock()
        mock_batch_writer = MagicMock()
        mock_table.batch_writer.return_value.__enter__ = MagicMock(
            return_value=mock_batch_writer
        )
        mock_table.batch_writer.return_value.__exit__ = MagicMock(return_value=False)
        mock_table.table_name = 'test-table'

        metrics = [
            {'metric_id': 'm1', 'value': Decimal('1.0')},
            {'metric_id': 'm2', 'value': Decimal('2.0')}
        ]

        result = write_metrics(mock_table, metrics)

        assert result == 2
        assert mock_batch_writer.put_item.call_count == 2

    def test_handles_write_errors(self):
        mock_table = MagicMock()
        mock_batch_writer = MagicMock()
        mock_batch_writer.put_item.side_effect = [None, Exception("Write failed")]
        mock_table.batch_writer.return_value.__enter__ = MagicMock(
            return_value=mock_batch_writer
        )
        mock_table.batch_writer.return_value.__exit__ = MagicMock(return_value=False)
        mock_table.table_name = 'test-table'

        metrics = [
            {'metric_id': 'm1'},
            {'metric_id': 'm2'}
        ]

        result = write_metrics(mock_table, metrics)

        # First write succeeds, second fails
        assert result == 1


class TestLambdaHandler:
    """Integration tests for the Lambda handler."""

    @patch('lambda_function.get_dynamodb_resource')
    def test_successful_batch_processing(self, mock_get_dynamo):
        """Test end-to-end processing with mock DynamoDB."""
        # Setup mock tables
        mock_dynamodb = MagicMock()
        mock_feedback_table = MagicMock()
        mock_metrics_table = MagicMock()
        mock_metrics_table.table_name = 'sherpa-routing-metrics'

        mock_dynamodb.Table.side_effect = lambda name: (
            mock_feedback_table if 'feedback' in name else mock_metrics_table
        )
        mock_get_dynamo.return_value = mock_dynamodb

        # Setup mock feedback data
        mock_feedback_table.scan.return_value = {
            'Items': [
                {
                    'feedback_id': 'fb-001',
                    'model_id': 'claude-sonnet',
                    'task_type': 'coding',
                    'complexity': 'medium',
                    'success': True,
                    'latency_ms': Decimal('1500'),
                    'cost': Decimal('0.015'),
                    'quality_score': Decimal('8.5'),
                    'timestamp': '2024-01-14T10:00:00Z'
                },
                {
                    'feedback_id': 'fb-002',
                    'model_id': 'claude-sonnet',
                    'task_type': 'coding',
                    'complexity': 'medium',
                    'success': True,
                    'latency_ms': Decimal('1200'),
                    'cost': Decimal('0.012'),
                    'quality_score': Decimal('9.0'),
                    'timestamp': '2024-01-14T11:00:00Z'
                }
            ]
        }

        # Setup mock batch writer
        mock_batch_writer = MagicMock()
        mock_metrics_table.batch_writer.return_value.__enter__ = MagicMock(
            return_value=mock_batch_writer
        )
        mock_metrics_table.batch_writer.return_value.__exit__ = MagicMock(
            return_value=False
        )

        # Execute
        event = {
            'source': 'aws.events',
            'detail-type': 'Scheduled Event'
        }

        result = lambda_handler(event, None)

        # Verify
        assert result['statusCode'] == 200

        body = json.loads(result['body'])
        assert body['feedback_count'] == 2
        assert body['metrics_written'] == 1
        assert 'claude-sonnet' in body['models_processed']

    @patch('lambda_function.get_dynamodb_resource')
    def test_no_feedback_data(self, mock_get_dynamo):
        """Test handler when no feedback data exists."""
        mock_dynamodb = MagicMock()
        mock_feedback_table = MagicMock()
        mock_metrics_table = MagicMock()

        mock_dynamodb.Table.side_effect = lambda name: (
            mock_feedback_table if 'feedback' in name else mock_metrics_table
        )
        mock_get_dynamo.return_value = mock_dynamodb

        # Empty feedback
        mock_feedback_table.scan.return_value = {'Items': []}

        event = {'source': 'aws.events'}
        result = lambda_handler(event, None)

        assert result['statusCode'] == 200
        body = json.loads(result['body'])
        assert body['feedback_count'] == 0
        assert body['metrics_written'] == 0

    @patch('lambda_function.get_dynamodb_resource')
    def test_handles_dynamodb_error(self, mock_get_dynamo):
        """Test error handling when DynamoDB fails."""
        mock_get_dynamo.side_effect = Exception("DynamoDB connection failed")

        event = {'source': 'aws.events'}
        result = lambda_handler(event, None)

        assert result['statusCode'] == 500
        body = json.loads(result['body'])
        assert 'error' in body


class TestEndToEndScenarios:
    """End-to-end scenario tests."""

    def test_multiple_models_multiple_tasks(self):
        """Test aggregation across multiple models and task types."""
        feedback = [
            # Claude Sonnet - Coding
            {'model_id': 'claude-sonnet', 'task_type': 'coding', 'complexity': 'high',
             'success': True, 'latency_ms': 2000, 'cost': 0.02, 'quality_score': 9.0},
            {'model_id': 'claude-sonnet', 'task_type': 'coding', 'complexity': 'high',
             'success': True, 'latency_ms': 2200, 'cost': 0.022, 'quality_score': 8.5},

            # Claude Sonnet - Writing
            {'model_id': 'claude-sonnet', 'task_type': 'writing', 'complexity': 'low',
             'success': True, 'latency_ms': 800, 'cost': 0.008, 'quality_score': 9.5},

            # GPT-4o - Coding
            {'model_id': 'gpt-4o', 'task_type': 'coding', 'complexity': 'high',
             'success': False, 'latency_ms': 1500, 'cost': 0.015, 'quality_score': 6.0},
            {'model_id': 'gpt-4o', 'task_type': 'coding', 'complexity': 'high',
             'success': True, 'latency_ms': 1600, 'cost': 0.016, 'quality_score': 7.5},

            # Gemini - Analysis
            {'model_id': 'gemini-pro', 'task_type': 'analysis', 'complexity': 'medium',
             'success': True, 'latency_ms': 1000, 'cost': 0.005, 'quality_score': 8.0},
        ]

        aggregations = aggregate_feedback(feedback)

        # Should have 4 unique combinations
        assert len(aggregations) == 4
        assert 'claude-sonnet#coding#high' in aggregations
        assert 'claude-sonnet#writing#low' in aggregations
        assert 'gpt-4o#coding#high' in aggregations
        assert 'gemini-pro#analysis#medium' in aggregations

        # Verify Claude Sonnet coding aggregation
        sonnet_coding = aggregations['claude-sonnet#coding#high']
        assert sonnet_coding['total_count'] == 2
        assert sonnet_coding['success_count'] == 2

        # Verify GPT-4o coding aggregation
        gpt_coding = aggregations['gpt-4o#coding#high']
        assert gpt_coding['total_count'] == 2
        assert gpt_coding['success_count'] == 1  # One failed

        # Compute metrics and verify routing weights
        batch_date = datetime(2024, 1, 15, tzinfo=timezone.utc)
        metrics = compute_metrics(aggregations, batch_date)

        # Claude Sonnet with 100% success rate should have higher weight than GPT-4o with 50%
        sonnet_metric = next(m for m in metrics if m['model_id'] == 'claude-sonnet' and m['task_type'] == 'coding')
        gpt_metric = next(m for m in metrics if m['model_id'] == 'gpt-4o')

        assert float(sonnet_metric['routing_weight']) > float(gpt_metric['routing_weight'])


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
