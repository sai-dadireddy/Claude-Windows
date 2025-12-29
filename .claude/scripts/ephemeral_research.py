#!/usr/bin/env python3
"""
Ephemeral Research: Fetch data, extract insights, delete source.

This implements "Research & Burn" - gather information, save only the
insight to memory, delete the raw source material to prevent context pollution.

Usage:
    ephemeral_research.py <url_or_file> <query>
    ephemeral_research.py --cleanup  # Clean temp directory

Examples:
    ephemeral_research.py https://docs.example.com/api "authentication flow"
    ephemeral_research.py /tmp/large-log.txt "error pattern"
"""

import sys
import os
import shutil
import json
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError

TEMP_DIR = Path.home() / ".claude" / "tmp" / "research"
MEMORY_SCRIPT = Path.home() / ".claude" / "scripts" / "memory_manager.py"
MAX_CONTENT_SIZE = 100_000  # 100KB max to prevent context explosion


def log(msg: str):
    """Log with timestamp."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def fetch_url(url: str) -> str:
    """Fetch URL content."""
    try:
        req = Request(url, headers={'User-Agent': 'Claude-Ephemeral-Research/1.0'})
        with urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8', errors='ignore')
            return content[:MAX_CONTENT_SIZE]
    except Exception as e:
        log(f"Failed to fetch URL: {e}")
        return ""


def read_file(filepath: str) -> str:
    """Read file content."""
    try:
        path = Path(filepath)
        if not path.exists():
            log(f"File not found: {filepath}")
            return ""
        content = path.read_text(errors='ignore')
        return content[:MAX_CONTENT_SIZE]
    except Exception as e:
        log(f"Failed to read file: {e}")
        return ""


def extract_relevant_lines(content: str, query: str, context_lines: int = 3) -> str:
    """Extract lines matching the query with context."""
    lines = content.split('\n')
    query_lower = query.lower()
    query_words = query_lower.split()

    relevant = []
    for i, line in enumerate(lines):
        line_lower = line.lower()
        # Check if any query word is in the line
        if any(word in line_lower for word in query_words):
            # Get context lines
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)
            chunk = '\n'.join(lines[start:end])
            if chunk not in relevant:
                relevant.append(chunk)

    # Limit to prevent huge outputs
    combined = '\n---\n'.join(relevant[:10])
    return combined[:5000]  # Max 5KB of extracted content


def save_to_memory(project: str, insight: str, source: str):
    """Save extracted insight to memory."""
    if not MEMORY_SCRIPT.exists():
        log("Memory script not found, skipping save")
        return

    # Prepare the insight with source attribution
    content = f"Research from {source[:50]}: {insight}"

    try:
        subprocess.run(
            ["python3", str(MEMORY_SCRIPT), "save-memory", project, "learning", content],
            timeout=10, capture_output=True
        )
        log("Insight saved to memory")
    except:
        log("Failed to save to memory")


def cleanup_temp():
    """Clean the temp research directory."""
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
        log(f"Cleaned up: {TEMP_DIR}")
    else:
        log("Temp directory already clean")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    # Handle cleanup command
    if sys.argv[1] == "--cleanup":
        cleanup_temp()
        sys.exit(0)

    if len(sys.argv) < 3:
        print("Usage: ephemeral_research.py <url_or_file> <query>")
        sys.exit(1)

    source = sys.argv[1]
    query = sys.argv[2]
    project = os.path.basename(os.getcwd())

    log(f"🕵️ Ephemeral Research")
    log(f"   Source: {source[:60]}")
    log(f"   Query: {query}")

    # Ensure temp dir exists
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    # Create temp file for raw content
    source_hash = hashlib.md5(source.encode()).hexdigest()[:8]
    temp_file = TEMP_DIR / f"raw_{source_hash}.txt"

    # 1. Fetch/Read content
    if source.startswith('http://') or source.startswith('https://'):
        log("📥 Fetching URL...")
        content = fetch_url(source)
    else:
        log("📄 Reading file...")
        content = read_file(source)

    if not content:
        log("❌ No content retrieved")
        sys.exit(1)

    # Save raw content temporarily (for debugging if needed)
    temp_file.write_text(content)
    log(f"   Raw content: {len(content)} chars")

    # 2. Extract relevant information
    log("🔍 Extracting relevant content...")
    extracted = extract_relevant_lines(content, query)

    if not extracted:
        log("⚠️ No matching content found for query")
        # Clean up immediately
        if temp_file.exists():
            temp_file.unlink()
        sys.exit(0)

    # 3. Output the extracted insight
    print("\n" + "="*60)
    print(f"📋 EXTRACTED INSIGHT for '{query}':")
    print("="*60)
    print(extracted)
    print("="*60 + "\n")

    # 4. Save insight to memory
    # Create a summary (first 500 chars of extracted content)
    summary = extracted[:500].replace('\n', ' ')
    save_to_memory(project, summary, source)

    # 5. CLEANUP - Delete raw source file
    if temp_file.exists():
        temp_file.unlink()
        log("🗑️ Raw source file deleted (context hygiene preserved)")

    # Also clean up old temp files (> 1 hour old)
    for old_file in TEMP_DIR.glob("raw_*.txt"):
        try:
            age = datetime.now().timestamp() - old_file.stat().st_mtime
            if age > 3600:  # 1 hour
                old_file.unlink()
        except:
            pass

    log("✅ Research complete. Insight saved, source discarded.")


if __name__ == "__main__":
    main()
