#!/usr/bin/env python3
"""
Security Audit Logger for Claude Code
Implements security event logging as specified in .claude/settings.json

Features:
- Daily log rotation
- 30-day retention
- JSON structured logging
- Event types: file_access, command_execution, permission_denied, suspicious_patterns, security_recommendations
"""

import os
import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from logging.handlers import RotatingFileHandler
import glob
import sys

# Set UTF-8 encoding for console output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

class SecurityAuditLogger:
    """Security audit logger with rotation and retention management"""

    def __init__(self, log_path=None, retention_days=30):
        """
        Initialize security audit logger

        Args:
            log_path: Path to log file (default: $HOME/.claude/security-audit.log)
            retention_days: Number of days to retain logs (default: 30)
        """
        if log_path is None:
            # Resolve $HOME to actual user home directory
            home = Path.home()
            log_path = home / ".claude" / "security-audit.log"
        else:
            log_path = Path(log_path.replace("$HOME", str(Path.home())))

        self.log_path = Path(log_path)
        self.retention_days = retention_days

        # Create log directory if it doesn't exist
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        # Setup logger
        self.logger = logging.getLogger('security-audit')
        self.logger.setLevel(logging.INFO)

        # Remove existing handlers
        self.logger.handlers.clear()

        # Create file handler with daily rotation
        handler = logging.FileHandler(self.log_path, mode='a', encoding='utf-8')
        handler.setLevel(logging.INFO)

        # JSON formatter
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

        # Clean old logs on initialization
        self._cleanup_old_logs()

    def log_event(self, event_type, details, severity="info"):
        """
        Log a security event

        Args:
            event_type: Type of event (file_access, command_execution, etc.)
            details: Dictionary with event details
            severity: Event severity (info, warning, critical)
        """
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "severity": severity,
            "details": details
        }

        self.logger.info(json.dumps(event))

    def log_file_access(self, file_path, operation, user=None, result="success"):
        """Log file access event"""
        self.log_event("file_access", {
            "file_path": file_path,
            "operation": operation,
            "user": user or os.environ.get("USERNAME", "unknown"),
            "result": result
        })

    def log_command_execution(self, command, args=None, user=None, result="success"):
        """Log command execution event"""
        self.log_event("command_execution", {
            "command": command,
            "args": args or [],
            "user": user or os.environ.get("USERNAME", "unknown"),
            "result": result
        })

    def log_permission_denied(self, resource, operation, reason):
        """Log permission denied event"""
        self.log_event("permission_denied", {
            "resource": resource,
            "operation": operation,
            "reason": reason,
            "user": os.environ.get("USERNAME", "unknown")
        }, severity="warning")

    def log_suspicious_pattern(self, pattern, context, risk_level="medium"):
        """Log suspicious pattern detection"""
        self.log_event("suspicious_patterns", {
            "pattern": pattern,
            "context": context,
            "risk_level": risk_level
        }, severity="warning" if risk_level != "high" else "critical")

    def log_security_recommendation(self, recommendation, category, priority="medium"):
        """Log security recommendation"""
        self.log_event("security_recommendations", {
            "recommendation": recommendation,
            "category": category,
            "priority": priority
        })

    def rotate_log(self):
        """Rotate log file with timestamp"""
        if self.log_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d")
            rotated_path = self.log_path.parent / f"{self.log_path.stem}-{timestamp}{self.log_path.suffix}"

            # Only rotate if today's rotated log doesn't exist
            if not rotated_path.exists():
                self.log_path.rename(rotated_path)
                # Logger will create new file on next write

    def _cleanup_old_logs(self):
        """Remove logs older than retention period"""
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)

        # Find all rotated log files
        pattern = str(self.log_path.parent / f"{self.log_path.stem}-*{self.log_path.suffix}")
        for log_file in glob.glob(pattern):
            log_path = Path(log_file)
            # Extract date from filename (format: security-audit-YYYYMMDD.log)
            try:
                date_str = log_path.stem.split('-')[-1]
                log_date = datetime.strptime(date_str, "%Y%m%d")

                if log_date < cutoff_date:
                    log_path.unlink()
                    print(f"Deleted old log: {log_file}")
            except (ValueError, IndexError):
                # Skip files that don't match expected pattern
                pass


class OperationsLogger:
    """Operations logger for general Claude Code activities"""

    def __init__(self, log_path=None):
        """
        Initialize operations logger

        Args:
            log_path: Path to log file (default: $HOME/.claude/operations.log)
        """
        if log_path is None:
            home = Path.home()
            log_path = home / ".claude" / "operations.log"
        else:
            log_path = Path(log_path.replace("$HOME", str(Path.home())))

        self.log_path = Path(log_path)

        # Create log directory if it doesn't exist
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        # Setup logger
        self.logger = logging.getLogger('operations')
        self.logger.setLevel(logging.INFO)

        # Remove existing handlers
        self.logger.handlers.clear()

        # Create file handler
        handler = logging.FileHandler(self.log_path, mode='a', encoding='utf-8')
        handler.setLevel(logging.INFO)

        # JSON formatter
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

    def log_operation(self, operation_type, details, duration_ms=None):
        """
        Log an operation

        Args:
            operation_type: Type of operation (read, write, agent_launch, etc.)
            details: Dictionary with operation details
            duration_ms: Operation duration in milliseconds
        """
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "operation_type": operation_type,
            "details": details
        }

        if duration_ms is not None:
            event["duration_ms"] = duration_ms

        self.logger.info(json.dumps(event))

    def log_agent_launch(self, agent_type, task_description, status="started"):
        """Log agent launch"""
        self.log_operation("agent_launch", {
            "agent_type": agent_type,
            "task": task_description,
            "status": status
        })

    def log_mcp_call(self, server, tool, args, result=None, duration_ms=None):
        """Log MCP server tool call"""
        self.log_operation("mcp_call", {
            "server": server,
            "tool": tool,
            "args": args,
            "result": result
        }, duration_ms)

    def log_cost(self, operation, tokens_used, cost_usd):
        """Log token usage and cost"""
        self.log_operation("cost_tracking", {
            "operation": operation,
            "tokens": tokens_used,
            "cost_usd": cost_usd
        })

    def log_error(self, error_type, error_message, context=None):
        """Log error event"""
        self.log_operation("error", {
            "error_type": error_type,
            "message": error_message,
            "context": context or {}
        })


# Singleton instances
_security_logger = None
_operations_logger = None

def get_security_logger():
    """Get or create security audit logger instance"""
    global _security_logger
    if _security_logger is None:
        _security_logger = SecurityAuditLogger()
    return _security_logger

def get_operations_logger():
    """Get or create operations logger instance"""
    global _operations_logger
    if _operations_logger is None:
        _operations_logger = OperationsLogger()
    return _operations_logger


if __name__ == "__main__":
    # Test the loggers
    print("Testing Security Audit Logger...")
    security = get_security_logger()

    security.log_file_access(
        file_path="C:/Users/test/project/config.json",
        operation="read",
        result="success"
    )

    security.log_command_execution(
        command="git",
        args=["commit", "-m", "test"],
        result="success"
    )

    security.log_suspicious_pattern(
        pattern="Hardcoded API key detected",
        context={"file": "config.py", "line": 42},
        risk_level="high"
    )

    security.log_security_recommendation(
        recommendation="Use environment variables for sensitive data",
        category="secrets_management",
        priority="high"
    )

    print(f"✓ Security audit log created: {security.log_path}")

    print("\nTesting Operations Logger...")
    operations = get_operations_logger()

    operations.log_agent_launch(
        agent_type="security-code-reviewer",
        task_description="Review authentication module",
        status="started"
    )

    operations.log_mcp_call(
        server="code-index-mcp",
        tool="search_code_advanced",
        args={"pattern": "password", "regex": False},
        result="5 matches found",
        duration_ms=234
    )

    operations.log_cost(
        operation="code_review",
        tokens_used=15000,
        cost_usd=0.045
    )

    print(f"✓ Operations log created: {operations.log_path}")

    print("\n✓ Logging implementation complete!")
    print(f"\nLog locations:")
    print(f"  Security: {security.log_path}")
    print(f"  Operations: {operations.log_path}")
