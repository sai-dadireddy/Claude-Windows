#!/usr/bin/env python3
"""
Log Event Helper
Command-line interface for logging events from PowerShell/Bash
"""

import argparse
import json
import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

from security_audit_logger import get_security_logger, get_operations_logger


def main():
    parser = argparse.ArgumentParser(description='Log events to security-audit.log or operations.log')
    parser.add_argument('--log-type', required=True, choices=['security', 'operations'],
                        help='Type of log (security or operations)')
    parser.add_argument('--event-type', required=True,
                        help='Type of event')
    parser.add_argument('--details', required=True,
                        help='JSON string with event details')
    parser.add_argument('--severity', default='info',
                        help='Event severity (info, warning, critical)')
    parser.add_argument('--duration-ms', type=int,
                        help='Operation duration in milliseconds')

    args = parser.parse_args()

    # Parse details JSON
    try:
        details = json.loads(args.details)
    except json.JSONDecodeError as e:
        print(f"Error parsing details JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Log to appropriate logger
    if args.log_type == 'security':
        logger = get_security_logger()
        logger.log_event(args.event_type, details, args.severity)
    else:
        logger = get_operations_logger()
        logger.log_operation(args.event_type, details, args.duration_ms)

    print(f"✓ Event logged: {args.event_type}")


if __name__ == "__main__":
    main()
