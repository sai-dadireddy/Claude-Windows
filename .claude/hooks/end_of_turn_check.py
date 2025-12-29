#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
End of Turn Quality Gates (Stop) - Run quality checks before finishing

Features:
- TypeScript type checking
- Lint validation (ESLint, Ruff, etc.)
- Test runner for changed files
- Build verification
- Reports issues to user
"""

import json
import sys
import subprocess
import os
from pathlib import Path
from datetime import datetime

VERBOSE = False
LOG_DIR = Path.home() / ".claude" / "logs"

def log(msg: str):
    if VERBOSE:
        print(f"[QualityGate] {msg}", file=sys.stderr)

def run_cmd(cmd: list, cwd: str, timeout: int = 60) -> tuple:
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
        return False, "Timeout"
    except FileNotFoundError:
        return None, "Not found"  # Tool not installed
    except Exception as e:
        return False, str(e)

def check_typescript(cwd: str) -> dict:
    """Run TypeScript type checking"""
    tsconfig = Path(cwd) / "tsconfig.json"
    if not tsconfig.exists():
        return {"skip": True}

    log("Running TypeScript check...")
    success, output = run_cmd(["npx", "tsc", "--noEmit"], cwd, timeout=120)

    if success is None:
        return {"skip": True, "reason": "tsc not found"}

    if success:
        return {"pass": True}
    else:
        # Count errors
        error_count = output.count("error TS")
        return {
            "pass": False,
            "errors": error_count,
            "sample": output[:200] if output else ""
        }

def check_eslint(cwd: str) -> dict:
    """Run ESLint"""
    pkg_json = Path(cwd) / "package.json"
    if not pkg_json.exists():
        return {"skip": True}

    # Check if eslint is configured
    try:
        pkg = json.loads(pkg_json.read_text())
        has_eslint = (
            "eslint" in pkg.get("devDependencies", {}) or
            "eslint" in pkg.get("dependencies", {}) or
            "lint" in pkg.get("scripts", {})
        )
        if not has_eslint:
            return {"skip": True}
    except:
        return {"skip": True}

    log("Running ESLint...")
    success, output = run_cmd(["npm", "run", "lint", "--if-present"], cwd, timeout=120)

    if success is None:
        return {"skip": True}

    if success:
        return {"pass": True}
    else:
        error_count = output.count("error")
        return {
            "pass": False,
            "errors": error_count,
            "sample": output[:200] if output else ""
        }

def check_ruff(cwd: str) -> dict:
    """Run Ruff for Python projects"""
    # Check if Python project
    has_python = any([
        (Path(cwd) / "pyproject.toml").exists(),
        (Path(cwd) / "setup.py").exists(),
        (Path(cwd) / "requirements.txt").exists(),
        list(Path(cwd).glob("*.py"))
    ])

    if not has_python:
        return {"skip": True}

    log("Running Ruff check...")
    success, output = run_cmd(["ruff", "check", "."], cwd, timeout=60)

    if success is None:
        # Try with uvx
        success, output = run_cmd(["uvx", "ruff", "check", "."], cwd, timeout=60)
        if success is None:
            return {"skip": True, "reason": "ruff not found"}

    if success:
        return {"pass": True}
    else:
        error_count = len([l for l in output.split("\n") if l.strip() and not l.startswith("Found")])
        return {
            "pass": False,
            "errors": error_count,
            "sample": output[:200] if output else ""
        }

def check_pytest(cwd: str) -> dict:
    """Run pytest for Python projects"""
    # Check if pytest is likely configured
    has_tests = any([
        (Path(cwd) / "tests").exists(),
        (Path(cwd) / "test").exists(),
        list(Path(cwd).glob("**/test_*.py")),
        list(Path(cwd).glob("**/*_test.py"))
    ])

    if not has_tests:
        return {"skip": True}

    log("Running pytest...")
    success, output = run_cmd(["pytest", "--tb=no", "-q"], cwd, timeout=180)

    if success is None:
        return {"skip": True, "reason": "pytest not found"}

    if success:
        # Extract pass count
        return {"pass": True}
    else:
        # Extract failure count
        failed_match = output.split("failed")
        failures = 0
        if len(failed_match) > 1:
            try:
                failures = int(failed_match[0].split()[-1])
            except:
                pass
        return {
            "pass": False,
            "errors": failures,
            "sample": output[:200] if output else ""
        }

def check_build(cwd: str) -> dict:
    """Check if build succeeds"""
    pkg_json = Path(cwd) / "package.json"
    if not pkg_json.exists():
        return {"skip": True}

    try:
        pkg = json.loads(pkg_json.read_text())
        if "build" not in pkg.get("scripts", {}):
            return {"skip": True}
    except:
        return {"skip": True}

    log("Running build check...")
    success, output = run_cmd(["npm", "run", "build"], cwd, timeout=300)

    if success is None:
        return {"skip": True}

    if success:
        return {"pass": True}
    else:
        return {
            "pass": False,
            "errors": 1,
            "sample": output[-200:] if output else ""
        }

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    cwd = data.get("cwd", os.getcwd())
    session_id = data.get("session_id", "")

    log(f"Running quality gates for {cwd}")

    # Run all checks
    checks = {
        "typescript": check_typescript(cwd),
        "eslint": check_eslint(cwd),
        "ruff": check_ruff(cwd),
        # "pytest": check_pytest(cwd),  # Commented out - can be slow
        # "build": check_build(cwd),     # Commented out - can be slow
    }

    # Collect results
    passed = []
    failed = []
    skipped = []

    for name, result in checks.items():
        if result.get("skip"):
            skipped.append(name)
        elif result.get("pass"):
            passed.append(name)
        else:
            failed.append((name, result.get("errors", 0)))

    # Log results
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(LOG_DIR / "quality_gates.jsonl", "a") as f:
            f.write(json.dumps({
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id[:12] if session_id else "",
                "cwd": cwd,
                "passed": passed,
                "failed": [f[0] for f in failed],
                "skipped": skipped
            }) + "\n")
    except:
        pass

    # Generate user message
    if failed:
        issues = [f"{name}({errors})" for name, errors in failed]
        log(f"[FAIL] Failed: {', '.join(issues)}")
        output = {
            "systemMessage": f"[WARN] Quality issues: {', '.join(issues)}"
        }
        print(json.dumps(output))
    elif passed:
        log(f"[OK] Passed: {', '.join(passed)}")
        output = {
            "systemMessage": f"[OK] Quality checks passed: {', '.join(passed)}"
        }
        print(json.dumps(output))
    else:
        log("[END]️ No applicable checks")

    sys.exit(0)

if __name__ == "__main__":
    main()
