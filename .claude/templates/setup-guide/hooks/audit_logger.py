#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Audit Logger Hook (PostToolUse) - Compliance-ready audit trail"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

AUDIT_LOG = Path.home() / '.claude' / 'logs' / 'audit.jsonl'
VERBOSE = True

def log(msg: str):
    if VERBOSE:
        print(f"[AuditLogger] {msg}", file=sys.stderr)

def extract_metadata(tool_input):
    """Extract relevant metadata from tool input."""
    metadata = {}

    # File operations
    if 'file_path' in tool_input:
        metadata['file'] = os.path.basename(tool_input['file_path'])
        metadata['path'] = tool_input['file_path']

    # Bash commands
    if 'command' in tool_input:
        cmd = tool_input['command']
        metadata['command'] = cmd[:200] if len(cmd) > 200 else cmd

    # Content sizes (don't log actual content)
    for key in ['content', 'new_string', 'old_string']:
        if key in tool_input:
            metadata[f'{key}_size'] = len(str(tool_input[key]))

    # Other small fields
    for key, value in tool_input.items():
        if key in metadata or key in ['content', 'new_string', 'old_string']:
            continue
        if isinstance(value, str) and len(value) < 100:
            metadata[key] = value
        elif isinstance(value, (int, float, bool)):
            metadata[key] = value

    return metadata

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    tool = data.get('tool_name', 'unknown')
    log(f"📝 Logging: {tool}")

    # Build audit entry
    entry = {
        'timestamp': datetime.now().isoformat(),
        'session_id': data.get('session_id', '')[:12],
        'tool': data.get('tool_name', 'unknown'),
        'user': os.environ.get('USER', 'unknown'),
        'cwd': data.get('cwd', os.getcwd()),
        'project': os.path.basename(data.get('cwd', os.getcwd())),
    }

    # Add tool metadata
    tool_input = data.get('tool_input', {})
    if tool_input:
        entry['metadata'] = extract_metadata(tool_input)

    # Add response info
    tool_response = data.get('tool_response', {})
    if isinstance(tool_response, dict):
        if tool_response.get('success') is not None:
            entry['success'] = tool_response['success']
        if tool_response.get('error'):
            entry['error'] = str(tool_response['error'])[:200]

    # Write to audit log
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(AUDIT_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, separators=(',', ':')) + '\n')
    except Exception as e:
        # Silent fail - don't break workflow
        pass

    sys.exit(0)

if __name__ == '__main__':
    main()
