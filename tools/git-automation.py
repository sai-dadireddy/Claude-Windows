#!/usr/bin/env python3
"""
Git Automation Tool
Purpose: Auto-commit, checkpoints, and rollback for safe development
Date: 2025-10-01
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path

class GitAutomation:
    def __init__(self, repo_path=None):
        """Initialize Git automation for a repository."""
        self.repo_path = repo_path or os.getcwd()
        self.checkpoint_file = os.path.join(self.repo_path, '.git', 'checkpoints.json')

    def is_git_repo(self):
        """Check if current directory is a git repository."""
        try:
            subprocess.run(['git', 'rev-parse', '--git-dir'],
                         cwd=self.repo_path,
                         check=True,
                         capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def init_repo(self):
        """Initialize git repository if not exists."""
        if not self.is_git_repo():
            print(f"Initializing git repository in {self.repo_path}...")
            subprocess.run(['git', 'init'], cwd=self.repo_path, check=True)

            # Create .gitignore
            gitignore_path = os.path.join(self.repo_path, '.gitignore')
            if not os.path.exists(gitignore_path):
                with open(gitignore_path, 'w') as f:
                    f.write("""# Build outputs
node_modules/
dist/
.angular/
*.pyc
__pycache__/

# Cache
.claude/
*.log

# OS
.DS_Store
Thumbs.db

# Sensitive
*.env
.env.*
credentials.json
""")
                print("Created .gitignore")

            print("[OK] Git repository initialized")
            return True
        return False

    def get_status(self):
        """Get git status."""
        try:
            result = subprocess.run(['git', 'status', '--short'],
                                  cwd=self.repo_path,
                                  capture_output=True,
                                  text=True,
                                  check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error getting git status: {e}")
            return None

    def auto_commit(self, message=None, add_all=True):
        """
        Auto-commit changes with descriptive message.

        Args:
            message: Commit message (auto-generated if None)
            add_all: Add all changes (default True)
        """
        if not self.is_git_repo():
            print("Not a git repository. Run 'init' first.")
            return False

        # Check if there are changes
        status = self.get_status()
        if not status:
            print("No changes to commit")
            return False

        # Add files
        if add_all:
            subprocess.run(['git', 'add', '.'], cwd=self.repo_path, check=True)
            print("[OK] Staged all changes")

        # Generate message if not provided
        if not message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = f"Auto-commit: {timestamp}\n\n🤖 Generated with Claude Code"
        else:
            # Add Claude Code attribution
            message = f"{message}\n\n🤖 Generated with Claude Code\nCo-Authored-By: Claude <noreply@anthropic.com>"

        # Commit
        try:
            subprocess.run(['git', 'commit', '-m', message],
                         cwd=self.repo_path,
                         check=True)
            print(f"[OK] Committed: {message.split(chr(10))[0]}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error committing: {e}")
            return False

    def create_checkpoint(self, name=None):
        """
        Create a named checkpoint (tag) for easy rollback.

        Args:
            name: Checkpoint name (auto-generated if None)
        """
        if not self.is_git_repo():
            print("Not a git repository. Run 'init' first.")
            return False

        # Auto-commit current changes first
        if self.get_status():
            self.auto_commit(f"Checkpoint: {name or 'auto'}")

        # Get current commit hash
        result = subprocess.run(['git', 'rev-parse', 'HEAD'],
                              cwd=self.repo_path,
                              capture_output=True,
                              text=True,
                              check=True)
        commit_hash = result.stdout.strip()

        # Generate checkpoint name
        if not name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"checkpoint_{timestamp}"

        # Create tag
        subprocess.run(['git', 'tag', '-a', name, '-m', f'Checkpoint: {name}'],
                      cwd=self.repo_path,
                      check=True)

        # Save checkpoint info
        self._save_checkpoint(name, commit_hash)

        print(f"[OK] Created checkpoint: {name}")
        print(f"  Commit: {commit_hash[:8]}")
        return name

    def list_checkpoints(self):
        """List all checkpoints."""
        try:
            result = subprocess.run(['git', 'tag', '--list', 'checkpoint_*'],
                                  cwd=self.repo_path,
                                  capture_output=True,
                                  text=True,
                                  check=True)
            checkpoints = result.stdout.strip().split('\n')
            checkpoints = [c for c in checkpoints if c]  # Remove empty

            if not checkpoints:
                print("No checkpoints found")
                return []

            print(f"\nCheckpoints ({len(checkpoints)}):")
            for cp in checkpoints:
                # Get commit info
                result = subprocess.run(['git', 'show', '-s', '--format=%h %ci %s', cp],
                                      cwd=self.repo_path,
                                      capture_output=True,
                                      text=True)
                info = result.stdout.strip()
                print(f"  {cp}: {info}")

            return checkpoints
        except subprocess.CalledProcessError:
            return []

    def rollback_to_checkpoint(self, checkpoint_name):
        """
        Rollback to a specific checkpoint.

        Args:
            checkpoint_name: Name of checkpoint to rollback to
        """
        if not self.is_git_repo():
            print("Not a git repository.")
            return False

        # Check if checkpoint exists
        try:
            subprocess.run(['git', 'rev-parse', checkpoint_name],
                         cwd=self.repo_path,
                         check=True,
                         capture_output=True)
        except subprocess.CalledProcessError:
            print(f"Checkpoint '{checkpoint_name}' not found")
            return False

        # Warn about uncommitted changes
        if self.get_status():
            print("⚠️  WARNING: You have uncommitted changes!")
            print("Creating safety checkpoint before rollback...")
            self.create_checkpoint("pre_rollback_safety")

        # Rollback
        try:
            subprocess.run(['git', 'reset', '--hard', checkpoint_name],
                         cwd=self.repo_path,
                         check=True)
            print(f"[OK] Rolled back to checkpoint: {checkpoint_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error rolling back: {e}")
            return False

    def rollback_last_commit(self):
        """Rollback the last commit (keep changes in working directory)."""
        if not self.is_git_repo():
            print("Not a git repository.")
            return False

        try:
            subprocess.run(['git', 'reset', '--soft', 'HEAD~1'],
                         cwd=self.repo_path,
                         check=True)
            print("[OK] Rolled back last commit (changes kept in staging)")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error rolling back: {e}")
            return False

    def _save_checkpoint(self, name, commit_hash):
        """Save checkpoint info to JSON file."""
        checkpoints = {}
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r') as f:
                checkpoints = json.load(f)

        checkpoints[name] = {
            'commit': commit_hash,
            'timestamp': datetime.now().isoformat(),
        }

        # Ensure .git directory exists
        git_dir = os.path.join(self.repo_path, '.git')
        os.makedirs(git_dir, exist_ok=True)

        with open(self.checkpoint_file, 'w') as f:
            json.dump(checkpoints, f, indent=2)

    def show_log(self, limit=10):
        """Show recent commit log."""
        if not self.is_git_repo():
            print("Not a git repository.")
            return

        try:
            result = subprocess.run(['git', 'log', f'-{limit}', '--oneline', '--decorate'],
                                  cwd=self.repo_path,
                                  capture_output=True,
                                  text=True,
                                  check=True)
            print(f"\nRecent commits (last {limit}):")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error showing log: {e}")


def main():
    """Main CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(description='Git Automation Tool')
    parser.add_argument('action', choices=['init', 'commit', 'checkpoint', 'list', 'rollback', 'undo', 'status', 'log'],
                       help='Action to perform')
    parser.add_argument('--message', '-m', help='Commit message')
    parser.add_argument('--name', '-n', help='Checkpoint name')
    parser.add_argument('--path', '-p', help='Repository path (default: current directory)')

    args = parser.parse_args()

    git = GitAutomation(args.path)

    if args.action == 'init':
        git.init_repo()

    elif args.action == 'commit':
        git.auto_commit(args.message)

    elif args.action == 'checkpoint':
        git.create_checkpoint(args.name)

    elif args.action == 'list':
        git.list_checkpoints()

    elif args.action == 'rollback':
        if not args.name:
            print("Error: --name required for rollback")
            sys.exit(1)
        git.rollback_to_checkpoint(args.name)

    elif args.action == 'undo':
        git.rollback_last_commit()

    elif args.action == 'status':
        status = git.get_status()
        if status:
            print("Changes:")
            print(status)
        else:
            print("No changes")

    elif args.action == 'log':
        git.show_log()


if __name__ == '__main__':
    main()
