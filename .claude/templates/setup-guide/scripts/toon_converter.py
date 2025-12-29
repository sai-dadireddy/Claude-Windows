#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["python-toon"]
# ///
"""
TOON Converter - Convert between JSON and TOON formats

Usage:
  toon_converter.py encode <json_file>       - Convert JSON file to TOON
  toon_converter.py decode <toon_file>       - Convert TOON file to JSON
  toon_converter.py stats <json_file>        - Show token savings estimate
  toon_converter.py -                        - Read JSON from stdin, output TOON

TOON (Token-Oriented Object Notation) saves 30-60% tokens vs JSON for LLMs.
"""

import json
import sys
from pathlib import Path

def encode_toon(data):
    """Encode data to TOON format"""
    try:
        from toon import encode
        return encode(data)
    except ImportError:
        return fallback_encode(data)

def decode_toon(toon_str: str):
    """Decode TOON to Python object"""
    try:
        from toon import decode
        return decode(toon_str)
    except ImportError:
        raise NotImplementedError("TOON decode requires python-toon library")

def fallback_encode(data, indent=0) -> str:
    """Fallback TOON encoder without library"""
    prefix = " " * indent

    if isinstance(data, dict):
        lines = []
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{prefix}{k}:")
                lines.append(fallback_encode(v, indent + 1))
            elif v is None:
                lines.append(f"{prefix}{k}: null")
            elif isinstance(v, bool):
                lines.append(f"{prefix}{k}: {'true' if v else 'false'}")
            elif isinstance(v, str) and (',' in v or ':' in v or '\n' in v):
                lines.append(f'{prefix}{k}: "{v}"')
            else:
                lines.append(f"{prefix}{k}: {v}")
        return "\n".join(lines)

    elif isinstance(data, list):
        if not data:
            return f"{prefix}[]"

        # Uniform array of objects -> tabular format
        if all(isinstance(x, dict) for x in data) and len(data) > 1:
            keys = list(data[0].keys())
            if all(set(x.keys()) == set(keys) for x in data):
                lines = [f"{prefix}[{len(data)}]{{{','.join(keys)}}}:"]
                for item in data:
                    vals = []
                    for k in keys:
                        v = item.get(k, "")
                        if v is None:
                            vals.append("null")
                        elif isinstance(v, bool):
                            vals.append("true" if v else "false")
                        elif isinstance(v, str) and ',' in v:
                            vals.append(f'"{v}"')
                        else:
                            vals.append(str(v))
                    lines.append(f"{prefix} {','.join(vals)}")
                return "\n".join(lines)

        # Mixed array
        lines = []
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.append(fallback_encode(item, indent + 1))
            else:
                lines.append(f"{prefix}- {item}")
        return "\n".join(lines)

    elif data is None:
        return "null"
    elif isinstance(data, bool):
        return "true" if data else "false"
    else:
        return str(data)

def estimate_tokens(text: str) -> int:
    """Rough token estimate (avg 4 chars per token)"""
    return len(text) // 4

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "-":
        # Read JSON from stdin
        try:
            data = json.load(sys.stdin)
            print(encode_toon(data))
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)

    elif cmd == "encode":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: toon_converter.py encode <file>"}))
            sys.exit(1)

        file_path = Path(sys.argv[2])
        try:
            with open(file_path) as f:
                data = json.load(f)
            print(encode_toon(data))
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)

    elif cmd == "decode":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: toon_converter.py decode <file>"}))
            sys.exit(1)

        file_path = Path(sys.argv[2])
        try:
            with open(file_path) as f:
                toon_str = f.read()
            data = decode_toon(toon_str)
            print(json.dumps(data, indent=2))
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)

    elif cmd == "stats":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: toon_converter.py stats <file>"}))
            sys.exit(1)

        file_path = Path(sys.argv[2])
        try:
            with open(file_path) as f:
                content = f.read()
                data = json.loads(content)

            json_str = json.dumps(data)
            toon_str = encode_toon(data)

            json_tokens = estimate_tokens(json_str)
            toon_tokens = estimate_tokens(toon_str)
            savings_pct = round((1 - toon_tokens / json_tokens) * 100, 1) if json_tokens > 0 else 0

            print(json.dumps({
                "json_chars": len(json_str),
                "toon_chars": len(toon_str),
                "json_tokens_est": json_tokens,
                "toon_tokens_est": toon_tokens,
                "savings_percent": savings_pct
            }, indent=2))
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)

    else:
        print(json.dumps({"error": f"Unknown command: {cmd}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
