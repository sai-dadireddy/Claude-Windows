#!/usr/bin/env python3
"""
Multi-AI Change Tracker
Tracks and attributes changes across Claude, Codex, and Gemini

Usage:
    python change-tracker.py list [--recent N] [--ai NAME]
    python change-tracker.py log <ai> <action> <files...>
    python change-tracker.py status <change-id>
    python change-tracker.py validate <change-id> <validator-ai>
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import uuid

# Get root directory (2 levels up from tools/ai-collaboration/)
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent.parent
CHANGE_LOG = ROOT_DIR / ".ai-workspace" / "shared" / "change-log.jsonl"
REVIEW_QUEUE = ROOT_DIR / ".ai-workspace" / "shared" / "review-queue.json"


class ChangeTracker:
    """Track and manage changes from multiple AIs"""

    def __init__(self):
        self.ensure_workspace()

    def ensure_workspace(self):
        """Ensure .ai-workspace exists"""
        workspace = ROOT_DIR / ".ai-workspace"
        if not workspace.exists():
            print("❌ Error: .ai-workspace not found!")
            print("   Run: pwsh tools/ai-collaboration/setup-multi-ai.ps1")
            sys.exit(1)

        # Ensure change log exists
        if not CHANGE_LOG.exists():
            CHANGE_LOG.parent.mkdir(parents=True, exist_ok=True)
            self._write_header()

    def _write_header(self):
        """Write change log header"""
        header = {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "description": "Multi-AI change tracking log"
        }
        with open(CHANGE_LOG, 'w', encoding='utf-8') as f:
            f.write(json.dumps(header) + '\n')

    def log_change(
        self,
        ai: str,
        action: str,
        files: List[str],
        change_type: str = "file_modify",
        references: Optional[str] = None,
        status: str = "completed"
    ) -> str:
        """Log a new change"""

        change_id = f"change-{datetime.now().strftime('%Y-%m-%d')}-{uuid.uuid4().hex[:6]}"

        change = {
            "id": change_id,
            "ai": ai,
            "timestamp": datetime.now().isoformat(),
            "type": change_type,
            "action": action,
            "files": files,
            "status": status,
            "review_status": "pending",
            "validated_by": None,
            "enhanced_by": None,
            "references": references
        }

        # Append to change log
        with open(CHANGE_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(change) + '\n')

        # Add to review queue if completed
        if status == "completed":
            self._add_to_review_queue(change)

        print(f"✅ Change logged: {change_id}")
        print(f"   AI: {ai}")
        print(f"   Action: {action}")
        print(f"   Files: {', '.join(files)}")

        return change_id

    def _add_to_review_queue(self, change: Dict):
        """Add change to review queue"""
        if not REVIEW_QUEUE.exists():
            queue = {"version": "1.0", "pending_reviews": [], "completed_reviews": []}
        else:
            with open(REVIEW_QUEUE, 'r', encoding='utf-8') as f:
                queue = json.load(f)

        queue["pending_reviews"].append(change)

        with open(REVIEW_QUEUE, 'w', encoding='utf-8') as f:
            json.dump(queue, f, indent=2)

    def list_changes(
        self,
        recent: Optional[int] = None,
        ai_filter: Optional[str] = None
    ):
        """List changes with optional filters"""

        if not CHANGE_LOG.exists():
            print("📝 No changes logged yet")
            return

        changes = []
        with open(CHANGE_LOG, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i == 0:  # Skip header
                    continue
                try:
                    change = json.loads(line.strip())
                    if ai_filter and change.get("ai") != ai_filter:
                        continue
                    changes.append(change)
                except json.JSONDecodeError:
                    continue

        if not changes:
            print(f"📝 No changes found{f' for {ai_filter}' if ai_filter else ''}")
            return

        # Apply recent filter
        if recent:
            changes = changes[-recent:]

        print(f"\n📋 Changes{f' (last {recent})' if recent else ''}{f' by {ai_filter}' if ai_filter else ''}:")
        print("=" * 80)

        for change in changes:
            timestamp = datetime.fromisoformat(change["timestamp"]).strftime("%Y-%m-%d %H:%M")
            ai_icon = self._get_ai_icon(change["ai"])
            status_icon = "✅" if change["status"] == "completed" else "🔄"

            print(f"\n{status_icon} {ai_icon} [{change['id']}]")
            print(f"   Time: {timestamp}")
            print(f"   AI: {change['ai']}")
            print(f"   Action: {change['action']}")
            print(f"   Files: {', '.join(change['files'][:3])}")
            if len(change['files']) > 3:
                print(f"          ... and {len(change['files']) - 3} more")
            print(f"   Review: {change['review_status']}")

            if change.get("validated_by"):
                print(f"   ✓ Validated by: {change['validated_by']}")
            if change.get("enhanced_by"):
                print(f"   ⚡ Enhanced by: {change['enhanced_by']}")
            if change.get("references"):
                print(f"   🔗 References: {change['references']}")

        print(f"\n{'=' * 80}\n")

    def get_change_status(self, change_id: str):
        """Get status of a specific change"""

        if not CHANGE_LOG.exists():
            print("❌ Change log not found")
            return

        with open(CHANGE_LOG, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i == 0:
                    continue
                try:
                    change = json.loads(line.strip())
                    if change.get("id") == change_id:
                        self._print_change_detail(change)
                        return
                except json.JSONDecodeError:
                    continue

        print(f"❌ Change not found: {change_id}")

    def validate_change(self, change_id: str, validator_ai: str):
        """Mark a change as validated by another AI"""

        if not CHANGE_LOG.exists():
            print("❌ Change log not found")
            return

        # Read all changes
        changes = []
        with open(CHANGE_LOG, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i == 0:
                    changes.append(line.strip())
                    continue
                try:
                    change = json.loads(line.strip())
                    if change.get("id") == change_id:
                        change["validated_by"] = validator_ai
                        change["review_status"] = "approved"
                    changes.append(json.dumps(change))
                except json.JSONDecodeError:
                    changes.append(line.strip())

        # Write back
        with open(CHANGE_LOG, 'w', encoding='utf-8') as f:
            f.write('\n'.join(changes) + '\n')

        print(f"✅ Change {change_id} validated by {validator_ai}")

    def _get_ai_icon(self, ai: str) -> str:
        """Get icon for AI"""
        icons = {
            "claude": "🔵",
            "codex": "🟢",
            "gemini": "🔷"
        }
        return icons.get(ai, "🤖")

    def _print_change_detail(self, change: Dict):
        """Print detailed change information"""
        ai_icon = self._get_ai_icon(change["ai"])
        timestamp = datetime.fromisoformat(change["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")

        print(f"\n{ai_icon} Change Details")
        print("=" * 80)
        print(f"ID:         {change['id']}")
        print(f"AI:         {change['ai']}")
        print(f"Timestamp:  {timestamp}")
        print(f"Type:       {change['type']}")
        print(f"Action:     {change['action']}")
        print(f"Status:     {change['status']}")
        print(f"Review:     {change['review_status']}")

        print(f"\nFiles ({len(change['files'])}):")
        for file in change['files']:
            print(f"  • {file}")

        if change.get("validated_by"):
            print(f"\n✓ Validated by: {change['validated_by']}")
        if change.get("enhanced_by"):
            print(f"⚡ Enhanced by: {change['enhanced_by']}")
        if change.get("references"):
            print(f"🔗 References: {change['references']}")

        print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Multi-AI Change Tracker")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # List command
    list_parser = subparsers.add_parser("list", help="List changes")
    list_parser.add_argument("--recent", type=int, help="Show last N changes")
    list_parser.add_argument("--ai", choices=["claude", "codex", "gemini"], help="Filter by AI")

    # Log command
    log_parser = subparsers.add_parser("log", help="Log a new change")
    log_parser.add_argument("ai", choices=["claude", "codex", "gemini"], help="AI making the change")
    log_parser.add_argument("action", help="Description of the action")
    log_parser.add_argument("files", nargs="+", help="Files affected")
    log_parser.add_argument("--type", default="file_modify", help="Change type")
    log_parser.add_argument("--references", help="Reference to related change")
    log_parser.add_argument("--status", default="completed", help="Change status")

    # Status command
    status_parser = subparsers.add_parser("status", help="Get change status")
    status_parser.add_argument("change_id", help="Change ID")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate a change")
    validate_parser.add_argument("change_id", help="Change ID to validate")
    validate_parser.add_argument("validator", choices=["claude", "codex", "gemini"], help="AI doing validation")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    tracker = ChangeTracker()

    if args.command == "list":
        tracker.list_changes(recent=args.recent, ai_filter=args.ai)

    elif args.command == "log":
        tracker.log_change(
            ai=args.ai,
            action=args.action,
            files=args.files,
            change_type=args.type,
            references=args.references,
            status=args.status
        )

    elif args.command == "status":
        tracker.get_change_status(args.change_id)

    elif args.command == "validate":
        tracker.validate_change(args.change_id, args.validator)


if __name__ == "__main__":
    main()
