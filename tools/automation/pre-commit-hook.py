#!/usr/bin/env python3
"""
Pre-Commit Hook for Claude Workspace
Purpose: Auto-format, lint, and validate before commits
Date: 2025-10-01
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class PreCommitHook:
    def __init__(self, repo_path=None):
        """Initialize pre-commit hook."""
        self.repo_path = repo_path or os.getcwd()
        self.errors = []
        self.warnings = []

    def run_command(self, cmd, cwd=None):
        """Run a command and return success status."""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.repo_path,
                capture_output=True,
                text=True,
                shell=True
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)

    def get_staged_files(self):
        """Get list of staged files."""
        success, stdout, _ = self.run_command("git diff --cached --name-only")
        if not success:
            return []

        files = stdout.strip().split('\n')
        return [f for f in files if f]

    def check_for_secrets(self, file_path):
        """Check if file contains potential secrets."""
        # Patterns that might indicate secrets
        secret_patterns = [
            'password',
            'api_key',
            'apikey',
            'secret',
            'token',
            'aws_access_key',
            'aws_secret_key',
            'private_key',
            'credentials'
        ]

        try:
            full_path = os.path.join(self.repo_path, file_path)
            if not os.path.exists(full_path):
                return

            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()

            for pattern in secret_patterns:
                if pattern in content and '=' in content:
                    # Check if it looks like an assignment
                    lines = content.split('\n')
                    for i, line in enumerate(lines, 1):
                        if pattern in line and '=' in line:
                            # Skip comments and variable names
                            if not line.strip().startswith('#') and not line.strip().startswith('//'):
                                self.warnings.append(
                                    f"{file_path}:{i} - Possible secret detected: {pattern}"
                                )
        except Exception as e:
            self.warnings.append(f"Could not scan {file_path}: {e}")

    def format_python_files(self, files):
        """Format Python files with black (if available)."""
        python_files = [f for f in files if f.endswith('.py')]
        if not python_files:
            return True

        print(f"[FORMAT] Checking {len(python_files)} Python file(s)...")

        # Check if black is available
        success, _, _ = self.run_command("black --version")
        if not success:
            self.warnings.append("Black formatter not installed (optional)")
            return True

        # Format files
        for file in python_files:
            full_path = os.path.join(self.repo_path, file)
            if os.path.exists(full_path):
                success, stdout, stderr = self.run_command(f'black "{full_path}"')
                if success:
                    print(f"  [OK] Formatted: {file}")
                    # Re-stage the formatted file
                    self.run_command(f'git add "{file}"')
                else:
                    self.warnings.append(f"Could not format {file}")

        return True

    def lint_python_files(self, files):
        """Lint Python files with pylint (if available)."""
        python_files = [f for f in files if f.endswith('.py')]
        if not python_files:
            return True

        print(f"[LINT] Checking {len(python_files)} Python file(s)...")

        # Check if pylint is available
        success, _, _ = self.run_command("pylint --version")
        if not success:
            self.warnings.append("Pylint not installed (optional)")
            return True

        # Lint files (non-blocking - just warnings)
        for file in python_files:
            full_path = os.path.join(self.repo_path, file)
            if os.path.exists(full_path):
                success, stdout, stderr = self.run_command(
                    f'pylint "{full_path}" --score=no --max-line-length=120'
                )
                if not success and stderr:
                    # Only show critical errors
                    if "error" in stderr.lower():
                        self.warnings.append(f"Lint warnings in {file}")

        return True

    def format_typescript_files(self, files):
        """Format TypeScript/JavaScript files with prettier (if available)."""
        ts_files = [f for f in files if f.endswith(('.ts', '.js', '.tsx', '.jsx'))]
        if not ts_files:
            return True

        print(f"[FORMAT] Checking {len(ts_files)} TypeScript/JS file(s)...")

        # Check if prettier is available
        success, _, _ = self.run_command("npx prettier --version")
        if not success:
            self.warnings.append("Prettier not installed (optional)")
            return True

        # Format files
        for file in ts_files:
            full_path = os.path.join(self.repo_path, file)
            if os.path.exists(full_path):
                success, stdout, stderr = self.run_command(
                    f'npx prettier --write "{full_path}"'
                )
                if success:
                    print(f"  [OK] Formatted: {file}")
                    # Re-stage the formatted file
                    self.run_command(f'git add "{file}"')
                else:
                    self.warnings.append(f"Could not format {file}")

        return True

    def lint_typescript_files(self, files):
        """Lint TypeScript files with eslint (if available)."""
        ts_files = [f for f in files if f.endswith(('.ts', '.tsx'))]
        if not ts_files:
            return True

        print(f"[LINT] Checking {len(ts_files)} TypeScript file(s)...")

        # Check if eslint is available
        success, _, _ = self.run_command("npx eslint --version")
        if not success:
            self.warnings.append("ESLint not installed (optional)")
            return True

        # Lint files
        for file in ts_files:
            full_path = os.path.join(self.repo_path, file)
            if os.path.exists(full_path):
                success, stdout, stderr = self.run_command(
                    f'npx eslint "{full_path}" --fix'
                )
                if success:
                    print(f"  [OK] Linted: {file}")
                    # Re-stage if fixed
                    self.run_command(f'git add "{file}"')
                else:
                    # Non-blocking - just warn
                    self.warnings.append(f"Lint warnings in {file}")

        return True

    def update_timestamps(self, files):
        """Update timestamps in markdown files."""
        md_files = [f for f in files if f.endswith('.md')]
        if not md_files:
            return True

        print(f"[UPDATE] Checking {len(md_files)} markdown file(s)...")

        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")

        for file in md_files:
            full_path = os.path.join(self.repo_path, file)
            if not os.path.exists(full_path):
                continue

            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Update common timestamp patterns
                updated = False

                # Pattern: **Date**: YYYY-MM-DD
                if "**Date**:" in content and "**Date**: " + today not in content:
                    # Find and update
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if line.startswith("**Date**:"):
                            lines[i] = f"**Date**: {today}"
                            updated = True
                            break
                    if updated:
                        content = '\n'.join(lines)

                # Pattern: Last updated: YYYY-MM-DD
                if "Last updated:" in content and "Last updated: " + today not in content:
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if "Last updated:" in line:
                            lines[i] = f"**Last updated**: {today}"
                            updated = True
                            break
                    if updated:
                        content = '\n'.join(lines)

                if updated:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  [OK] Updated timestamp: {file}")
                    self.run_command(f'git add "{file}"')

            except Exception as e:
                self.warnings.append(f"Could not update timestamp in {file}: {e}")

        return True

    def run(self):
        """Run all pre-commit checks."""
        print("\n" + "="*60)
        print("PRE-COMMIT HOOK - Claude Workspace")
        print("="*60 + "\n")

        # Get staged files
        staged_files = self.get_staged_files()
        if not staged_files:
            print("[INFO] No files staged for commit")
            return 0

        print(f"[INFO] Checking {len(staged_files)} staged file(s)\n")

        # Run checks
        checks = [
            ("Secret detection", lambda: self.check_secrets(staged_files)),
            ("Python formatting", lambda: self.format_python_files(staged_files)),
            ("Python linting", lambda: self.lint_python_files(staged_files)),
            ("TypeScript formatting", lambda: self.format_typescript_files(staged_files)),
            ("TypeScript linting", lambda: self.lint_typescript_files(staged_files)),
            ("Timestamp updates", lambda: self.update_timestamps(staged_files)),
        ]

        for check_name, check_func in checks:
            try:
                check_func()
            except Exception as e:
                self.warnings.append(f"{check_name} failed: {e}")

        # Report results
        print("\n" + "="*60)
        if self.errors:
            print("[ERROR] Pre-commit checks failed:")
            for error in self.errors:
                print(f"  - {error}")
            print("\n[BLOCKED] Commit aborted. Fix errors and try again.")
            return 1

        if self.warnings:
            print("[WARNING] Issues detected:")
            for warning in self.warnings:
                print(f"  - {warning}")
            print("\n[OK] Proceeding with commit (warnings are non-blocking)")
        else:
            print("[OK] All checks passed!")

        print("="*60 + "\n")
        return 0

    def check_secrets(self, files):
        """Check all files for secrets."""
        for file in files:
            self.check_for_secrets(file)
        return True


def main():
    """Main entry point for pre-commit hook."""
    hook = PreCommitHook()
    sys.exit(hook.run())


if __name__ == '__main__':
    main()
