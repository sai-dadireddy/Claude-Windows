#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Cache Manager - Reduces token usage by caching expensive operations

Features:
- File-based cache with TTL
- Hash-based cache keys
- Automatic cleanup of expired entries
- JSON serialization for results
"""

import json
import os
import hashlib
import time
from pathlib import Path
from typing import Any, Optional

CACHE_DIR = Path.home() / ".claude" / "cache"
DEFAULT_TTL = 3600  # 1 hour

def get_cache_key(operation: str, *args, **kwargs) -> str:
    """Generate a unique cache key from operation and arguments"""
    key_data = json.dumps({"op": operation, "args": args, "kwargs": kwargs}, sort_keys=True)
    return hashlib.sha256(key_data.encode()).hexdigest()[:16]

def get_cache(key: str, ttl: int = DEFAULT_TTL) -> Optional[Any]:
    """Get cached result if exists and not expired"""
    cache_file = CACHE_DIR / f"{key}.json"

    if not cache_file.exists():
        return None

    try:
        with open(cache_file, 'r') as f:
            data = json.load(f)

        # Check TTL
        if time.time() - data.get("timestamp", 0) > ttl:
            cache_file.unlink()  # Delete expired
            return None

        return data.get("result")
    except Exception:
        return None

def set_cache(key: str, result: Any) -> None:
    """Store result in cache"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"{key}.json"

    try:
        with open(cache_file, 'w') as f:
            json.dump({
                "timestamp": time.time(),
                "result": result
            }, f)
    except Exception:
        pass

def clear_cache(max_age: int = 86400) -> int:
    """Clear cache entries older than max_age seconds. Returns count cleared."""
    if not CACHE_DIR.exists():
        return 0

    cleared = 0
    now = time.time()

    for cache_file in CACHE_DIR.glob("*.json"):
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
            if now - data.get("timestamp", 0) > max_age:
                cache_file.unlink()
                cleared += 1
        except Exception:
            cache_file.unlink()
            cleared += 1

    return cleared

def cache_stats() -> dict:
    """Get cache statistics"""
    if not CACHE_DIR.exists():
        return {"entries": 0, "size_bytes": 0}

    entries = list(CACHE_DIR.glob("*.json"))
    total_size = sum(f.stat().st_size for f in entries)

    return {
        "entries": len(entries),
        "size_bytes": total_size,
        "size_kb": round(total_size / 1024, 2)
    }

# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: cache_manager.py <command> [args]"}))
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "get":
        key = sys.argv[2] if len(sys.argv) > 2 else ""
        result = get_cache(key)
        print(json.dumps({"key": key, "result": result, "hit": result is not None}))

    elif cmd == "set":
        key = sys.argv[2] if len(sys.argv) > 2 else ""
        value = sys.argv[3] if len(sys.argv) > 3 else "{}"
        try:
            value = json.loads(value)
        except:
            pass
        set_cache(key, value)
        print(json.dumps({"key": key, "stored": True}))

    elif cmd == "clear":
        max_age = int(sys.argv[2]) if len(sys.argv) > 2 else 86400
        cleared = clear_cache(max_age)
        print(json.dumps({"cleared": cleared}))

    elif cmd == "stats":
        print(json.dumps(cache_stats()))

    else:
        print(json.dumps({"error": f"Unknown command: {cmd}"}))
