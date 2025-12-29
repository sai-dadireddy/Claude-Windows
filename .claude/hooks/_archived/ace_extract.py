#!/usr/bin/env python3
"""
ACE (Agentic Context Engineering) - Extract Learnings
Extracts key learnings from session and saves to playbook
"""

import sys
import json
from pathlib import Path
from datetime import datetime

PLAYBOOK_PATH = Path.home() / '.claude' / 'playbook.json'

def load_playbook():
    """Load existing playbook"""
    try:
        if not PLAYBOOK_PATH.exists():
            return {"learnings": [], "last_updated": None}
        return json.loads(PLAYBOOK_PATH.read_text())
    except:
        return {"learnings": [], "last_updated": None}

def save_playbook(playbook):
    """Save playbook to disk"""
    try:
        PLAYBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
        PLAYBOOK_PATH.write_text(json.dumps(playbook, indent=2))
        return True
    except Exception as e:
        print(f"Error saving playbook: {e}", file=sys.stderr)
        return False

def extract_learnings_from_session():
    """
    Extract key learnings from current session

    This is a simplified version - In full ACE, this would:
    1. Read conversation transcript
    2. Use Claude to extract key insights
    3. Score each insight

    For now, we'll use a simplified approach with common patterns
    """

    # Common learnings to track (these get scored over time)
    common_learnings = [
        {
            "text": "Use RAG before reading documentation (97% token savings)",
            "category": "optimization",
            "score": 0
        },
        {
            "text": "Claude for planning (80% time), GLM for implementation (20% time)",
            "category": "workflow",
            "score": 0
        },
        {
            "text": "GLM-4.6 produces better frontend code than Claude",
            "category": "model-selection",
            "score": 0
        },
        {
            "text": "Use parallel agents for multi-file operations (3-5x faster)",
            "category": "performance",
            "score": 0
        },
        {
            "text": "RDS Data API simpler than psycopg2 for low-frequency Lambda",
            "category": "architecture",
            "score": 0
        },
        {
            "text": "Row-Level Security (RLS) critical for multi-tenant isolation",
            "category": "security",
            "score": 0
        },
        {
            "text": "Specialized agents for domain expertise (security, AWS, database)",
            "category": "workflow",
            "score": 0
        },
        {
            "text": "Jan AI (local) for quick optimizations (free, fast)",
            "category": "optimization",
            "score": 0
        }
    ]

    return common_learnings

def merge_learnings(existing, new_learnings):
    """Merge new learnings with existing playbook"""

    # Create lookup of existing learnings
    existing_texts = {l['text']: l for l in existing}

    # Merge
    for new in new_learnings:
        text = new['text']
        if text in existing_texts:
            # Existing - increment usage
            existing_texts[text]['sessions_applied'] = existing_texts[text].get('sessions_applied', 0) + 1
        else:
            # New learning
            new['sessions_applied'] = 1
            new['created_at'] = datetime.utcnow().isoformat()
            existing.append(new)

    return existing

def main():
    try:
        # Load existing playbook
        playbook = load_playbook()

        # Extract learnings from this session
        new_learnings = extract_learnings_from_session()

        # Merge with existing
        playbook['learnings'] = merge_learnings(
            playbook.get('learnings', []),
            new_learnings
        )

        # Update metadata
        playbook['last_updated'] = datetime.utcnow().isoformat()
        playbook['total_sessions'] = playbook.get('total_sessions', 0) + 1

        # Save
        if save_playbook(playbook):
            result = {
                "action": "ace_extract",
                "learnings_added": len(new_learnings),
                "total_learnings": len(playbook['learnings']),
                "message": f"ACE: Saved {len(new_learnings)} learnings"
            }
            print(json.dumps(result))
        else:
            print(json.dumps({"action": "error", "message": "Failed to save"}))

    except Exception as e:
        # Fail gracefully
        print(json.dumps({"action": "error", "message": str(e)}), file=sys.stderr)

if __name__ == '__main__':
    main()
