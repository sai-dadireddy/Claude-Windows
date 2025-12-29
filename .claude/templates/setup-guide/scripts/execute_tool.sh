#!/bin/bash
# execute_tool.sh - Lightweight executor for offloading heavy processing
# Runs Python scripts outside Claude's context, returns compact JSON
#
# Usage: execute_tool.sh <script.py> [args...]
# Output: Compact JSON result to stdout

set -e

SCRIPT_PATH="$1"
shift

if [ -z "$SCRIPT_PATH" ]; then
    echo '{"error": "No script provided", "usage": "execute_tool.sh <script.py> [args...]"}'
    exit 1
fi

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "{\"error\": \"Script not found: $SCRIPT_PATH\"}"
    exit 1
fi

# Create temp files for output
STDOUT_FILE=$(mktemp)
STDERR_FILE=$(mktemp)
trap "rm -f $STDOUT_FILE $STDERR_FILE" EXIT

# Run with uv for speed, capture output
if command -v uv &> /dev/null; then
    uv run --quiet python "$SCRIPT_PATH" "$@" > "$STDOUT_FILE" 2> "$STDERR_FILE"
    EXIT_CODE=$?
else
    python3 "$SCRIPT_PATH" "$@" > "$STDOUT_FILE" 2> "$STDERR_FILE"
    EXIT_CODE=$?
fi

# Check if output is already JSON
if head -1 "$STDOUT_FILE" | grep -q '^{'; then
    # Already JSON, output as-is
    cat "$STDOUT_FILE"
else
    # Wrap in JSON
    STDOUT=$(cat "$STDOUT_FILE" | head -c 10000)  # Limit output size
    STDERR=$(cat "$STDERR_FILE" | head -c 1000)

    python3 -c "
import json
import sys
stdout = '''$STDOUT'''
stderr = '''$STDERR'''
exit_code = $EXIT_CODE
result = {
    'success': exit_code == 0,
    'output': stdout.strip() if stdout.strip() else None,
    'error': stderr.strip() if stderr.strip() and exit_code != 0 else None
}
# Remove None values
result = {k: v for k, v in result.items() if v is not None}
print(json.dumps(result))
"
fi
