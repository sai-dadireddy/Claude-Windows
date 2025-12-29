#!/usr/bin/env python3
"""
Hooks-Based Logging System
Automatically logs all agent actions for observability and debugging

Based on Kenny's YouTube video pattern
Triggered by post-tool-use and stop events
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def parse_transcript(stdin_data):
    """
    Parse the conversation transcript from stdin

    Expects JSON with structure:
    {
        "messages": [...],
        "session_id": "...",
        "result": {...}
    }
    """
    try:
        data = json.loads(stdin_data)
        return data
    except json.JSONDecodeError as e:
        print(f"Error parsing transcript: {e}", file=sys.stderr)
        return None

def extract_agent_actions(transcript):
    """
    Extract all agent actions from transcript

    Actions include:
    - Tool calls (with inputs)
    - Tool results
    - Agent invocations
    - Thinking blocks
    - Assistant messages
    """
    actions = []

    messages = transcript.get("messages", [])

    for msg in messages:
        msg_type = msg.get("type")

        if msg_type == "tool_use":
            # Tool call
            actions.append({
                "timestamp": datetime.now().isoformat(),
                "type": "tool_call",
                "tool": msg.get("name"),
                "inputs": msg.get("input", {}),
                "id": msg.get("id")
            })

        elif msg_type == "tool_result":
            # Tool result
            actions.append({
                "timestamp": datetime.now().isoformat(),
                "type": "tool_result",
                "tool_use_id": msg.get("tool_use_id"),
                "content": msg.get("content", "")[:500],  # Truncate long results
                "is_error": msg.get("is_error", False)
            })

        elif msg_type == "assistant" and "content" in msg:
            # Check for thinking blocks or text responses
            for content_block in msg.get("content", []):
                if isinstance(content_block, dict):
                    if content_block.get("type") == "thinking":
                        actions.append({
                            "timestamp": datetime.now().isoformat(),
                            "type": "thinking",
                            "content": content_block.get("thinking", "")[:200]
                        })
                    elif content_block.get("type") == "text":
                        actions.append({
                            "timestamp": datetime.now().isoformat(),
                            "type": "assistant_message",
                            "content": content_block.get("text", "")[:200]
                        })

        elif msg_type == "system" and "agents" in msg.get("data", {}):
            # Agent invocations
            for agent in msg["data"]["agents"]:
                actions.append({
                    "timestamp": datetime.now().isoformat(),
                    "type": "agent_invocation",
                    "agent": agent.get("name"),
                    "description": agent.get("description", "")
                })

    return actions

def save_log(session_id, actions, transcript):
    """
    Save log to file

    File structure:
    logs/YYYY-MM-DD/session-{session_id}-actions.json
    """
    # Create logs directory structure
    logs_dir = Path(__file__).parent.parent.parent / "logs"
    date_dir = logs_dir / datetime.now().strftime("%Y-%m-%d")
    date_dir.mkdir(parents=True, exist_ok=True)

    # Log file path
    log_file = date_dir / f"session-{session_id}-actions.json"

    # Prepare log data
    log_data = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "total_actions": len(actions),
        "actions": actions,
        "usage": transcript.get("result", {}).get("usage", {}),
        "cost": transcript.get("result", {}).get("total_cost", 0)
    }

    # Write to file
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

    print(f"[OK] Logged {len(actions)} actions to {log_file}", file=sys.stderr)
    return log_file

def main():
    """
    Main hook execution
    Reads transcript from stdin and logs agent actions
    """
    # Read from stdin
    stdin_data = sys.stdin.read()

    if not stdin_data:
        print("No data received from stdin", file=sys.stderr)
        return

    # Parse transcript
    transcript = parse_transcript(stdin_data)
    if not transcript:
        return

    # Extract session ID
    session_id = transcript.get("session_id", "unknown")

    # Extract actions
    actions = extract_agent_actions(transcript)

    if not actions:
        print("No actions found in transcript", file=sys.stderr)
        return

    # Save log
    log_file = save_log(session_id, actions, transcript)

    # Print summary to stderr (user feedback)
    print(f"\n[DATA] Agent Actions Summary:", file=sys.stderr)
    print(f"   - Total actions: {len(actions)}", file=sys.stderr)
    print(f"   - Tool calls: {sum(1 for a in actions if a['type'] == 'tool_call')}", file=sys.stderr)
    print(f"   - Agent invocations: {sum(1 for a in actions if a['type'] == 'agent_invocation')}", file=sys.stderr)
    print(f"   - Log saved: {log_file}", file=sys.stderr)

if __name__ == "__main__":
    main()
