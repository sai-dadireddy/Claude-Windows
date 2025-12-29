#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Test Changed Files (PostToolUse) - Run tests related to modified files

Features:
- Finds and runs tests related to changed files
- Supports pytest, jest, go test, cargo test
- Fast targeted testing
- Reports failures immediately
"""

import json
import sys
import subprocess
import os
from pathlib import Path

VERBOSE = False

def log(msg: str):
    if VERBOSE:
        print(f"[Test] {msg}", file=sys.stderr)

def run_cmd(cmd: list, cwd: str, timeout: int = 120) -> tuple:
    """Run command and return (success, output)"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Timeout - tests took too long"
    except FileNotFoundError:
        return None, "Not found"
    except Exception as e:
        return False, str(e)

def find_python_test(file_path: str, cwd: str) -> str:
    """Find test file for a Python source file"""
    path = Path(file_path)
    filename = path.stem
    parent = path.parent

    # Common test file patterns
    test_patterns = [
        parent / f"test_{filename}.py",
        parent / f"{filename}_test.py",
        parent / "tests" / f"test_{filename}.py",
        parent / "tests" / f"{filename}_test.py",
        Path(cwd) / "tests" / f"test_{filename}.py",
        Path(cwd) / "tests" / f"{filename}_test.py",
        Path(cwd) / "test" / f"test_{filename}.py",
    ]

    for pattern in test_patterns:
        if pattern.exists():
            return str(pattern)

    # If the file itself is a test file
    if filename.startswith("test_") or filename.endswith("_test"):
        return file_path

    return None

def find_js_test(file_path: str, cwd: str) -> str:
    """Find test file for a JavaScript/TypeScript source file"""
    path = Path(file_path)
    stem = path.stem.replace(".test", "").replace(".spec", "")
    parent = path.parent
    ext = path.suffix

    # Common test file patterns
    test_patterns = [
        parent / f"{stem}.test{ext}",
        parent / f"{stem}.spec{ext}",
        parent / "__tests__" / f"{stem}.test{ext}",
        parent / "__tests__" / f"{stem}.spec{ext}",
        parent / "tests" / f"{stem}.test{ext}",
    ]

    for pattern in test_patterns:
        if pattern.exists():
            return str(pattern)

    # If the file itself is a test file
    if ".test." in file_path or ".spec." in file_path:
        return file_path

    return None

def test_python(file_path: str, cwd: str) -> dict:
    """Run pytest for Python file"""
    test_file = find_python_test(file_path, cwd)

    if not test_file:
        return {"skip": True, "reason": "No test file found"}

    log(f"Running pytest for {os.path.basename(test_file)}...")

    success, output = run_cmd(
        ["pytest", "-xvs", test_file],
        cwd,
        timeout=120
    )

    if success is None:
        return {"skip": True, "reason": "pytest not found"}

    if success:
        # Extract pass count
        passed = output.count(" PASSED")
        return {"pass": True, "tests": passed}
    else:
        failed = output.count(" FAILED")
        # Extract failure info
        return {
            "pass": False,
            "failed": failed,
            "sample": output[-500:]
        }

def test_javascript(file_path: str, cwd: str) -> dict:
    """Run jest for JavaScript/TypeScript file"""
    test_file = find_js_test(file_path, cwd)

    if not test_file:
        return {"skip": True, "reason": "No test file found"}

    log(f"Running jest for {os.path.basename(test_file)}...")

    # Check if jest is available
    success, output = run_cmd(
        ["npx", "jest", "--testPathPattern", test_file, "--passWithNoTests"],
        cwd,
        timeout=120
    )

    if success is None:
        return {"skip": True, "reason": "jest not found"}

    if success:
        return {"pass": True}
    else:
        failed = output.count("FAIL ")
        return {
            "pass": False,
            "failed": failed,
            "sample": output[-500:]
        }

def test_go(file_path: str, cwd: str) -> dict:
    """Run go test for Go file"""
    if not file_path.endswith(".go"):
        return {"skip": True}

    # Go tests are in the same directory
    test_dir = os.path.dirname(file_path)
    pkg = "./" + os.path.relpath(test_dir, cwd) if test_dir != cwd else "./..."

    log(f"Running go test for {pkg}...")

    success, output = run_cmd(
        ["go", "test", "-v", pkg],
        cwd,
        timeout=120
    )

    if success is None:
        return {"skip": True, "reason": "go not found"}

    if success:
        passed = output.count("--- PASS:")
        return {"pass": True, "tests": passed}
    else:
        failed = output.count("--- FAIL:")
        return {
            "pass": False,
            "failed": failed,
            "sample": output[-500:]
        }

def test_rust(file_path: str, cwd: str) -> dict:
    """Run cargo test for Rust file"""
    log("Running cargo test...")

    # Get the module name from file
    filename = os.path.basename(file_path).replace(".rs", "")

    success, output = run_cmd(
        ["cargo", "test", filename, "--", "--nocapture"],
        cwd,
        timeout=180
    )

    if success is None:
        return {"skip": True, "reason": "cargo not found"}

    if success:
        passed = output.count("test result: ok")
        return {"pass": True}
    else:
        failed = output.count("FAILED")
        return {
            "pass": False,
            "failed": failed,
            "sample": output[-500:]
        }

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    cwd = data.get("cwd", os.getcwd())

    # Only run for Write/Edit operations
    if tool not in ["Write", "Edit", "MultiEdit"]:
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    # Skip test files themselves to avoid recursion
    filename = os.path.basename(file_path)
    if any(x in filename for x in ["test_", "_test.", ".test.", ".spec."]):
        log(f"[END]️ Skipping test file itself")
        sys.exit(0)

    ext = os.path.splitext(file_path)[1].lower()
    result = None

    # Python
    if ext == ".py":
        result = test_python(file_path, cwd)

    # JavaScript/TypeScript
    elif ext in [".js", ".jsx", ".ts", ".tsx"]:
        result = test_javascript(file_path, cwd)

    # Go
    elif ext == ".go":
        result = test_go(file_path, cwd)

    # Rust
    elif ext == ".rs":
        result = test_rust(file_path, cwd)

    else:
        log(f"[END]️ No test runner for {ext}")
        sys.exit(0)

    # Handle result
    if result:
        if result.get("skip"):
            log(f"[END]️ Skipped: {result.get('reason', 'N/A')}")
        elif result.get("pass"):
            tests = result.get("tests", "all")
            log(f"[OK] Tests passed ({tests})")
        else:
            failed = result.get("failed", 0)
            log(f"[FAIL] Tests failed: {failed}")

            output = {
                "systemMessage": f"🔴 Tests failed for {filename}: {failed} failure(s)"
            }
            print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()
