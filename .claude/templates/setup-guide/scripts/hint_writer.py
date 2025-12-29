#!/usr/bin/env python3
"""
Shared hint writer for hooks.
Writes hints to ~/.claude/hints/current.txt with auto-cleanup.
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

HINT_FILE = Path.home() / ".claude" / "hints" / "current.txt"
MAX_AGE_MINUTES = 5  # Hints older than this are cleaned up
MAX_HINTS = 10  # Keep only this many recent hints

def write_hint(category: str, hint: str):
    """Write a hint with timestamp."""
    HINT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] [{category}] {hint}\n"
    
    # Read existing hints and filter old ones
    existing = []
    if HINT_FILE.exists():
        cutoff = datetime.now() - timedelta(minutes=MAX_AGE_MINUTES)
        for line in HINT_FILE.read_text().strip().split("\n"):
            if line.strip():
                try:
                    # Parse timestamp from line
                    ts_str = line.split("]")[0].replace("[", "")
                    ts = datetime.strptime(ts_str, "%H:%M:%S").replace(
                        year=datetime.now().year,
                        month=datetime.now().month,
                        day=datetime.now().day
                    )
                    if ts > cutoff:
                        existing.append(line)
                except:
                    pass  # Skip malformed lines
    
    # Add new hint and keep only recent ones
    existing.append(entry.strip())
    existing = existing[-MAX_HINTS:]
    
    HINT_FILE.write_text("\n".join(existing) + "\n")

def clear_hints():
    """Clear all hints."""
    if HINT_FILE.exists():
        HINT_FILE.unlink()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: hint_writer.py <category> <hint>")
        sys.exit(1)
    
    if sys.argv[1] == "--clear":
        clear_hints()
    else:
        write_hint(sys.argv[1], " ".join(sys.argv[2:]))
