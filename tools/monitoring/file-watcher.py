#!/usr/bin/env python3
"""
File Watcher for Claude Workspace
Purpose: Watch files for changes and trigger actions
Date: 2025-10-01
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ProjectFileHandler(FileSystemEventHandler):
    """Handler for file system events."""

    def __init__(self, config):
        """
        Initialize handler.

        Args:
            config: Dict with watch patterns and actions
        """
        self.config = config
        self.last_action_time = {}
        self.debounce_seconds = config.get('debounce_seconds', 2)

    def log(self, message):
        """Log message with timestamp."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")

    def should_process(self, file_path):
        """Check if file should be processed (debouncing)."""
        now = time.time()
        last_time = self.last_action_time.get(file_path, 0)

        if now - last_time < self.debounce_seconds:
            return False

        self.last_action_time[file_path] = now
        return True

    def matches_pattern(self, file_path):
        """Check if file matches watch patterns."""
        patterns = self.config.get('patterns', [])
        if not patterns:
            return True

        for pattern in patterns:
            if file_path.endswith(pattern):
                return True
        return False

    def run_action(self, action_name, file_path):
        """Run configured action."""
        actions = self.config.get('actions', {})
        action = actions.get(action_name)

        if not action:
            return

        command = action.get('command', '')
        if not command:
            return

        # Replace placeholders
        command = command.replace('{file}', file_path)
        command = command.replace('{dir}', os.path.dirname(file_path))
        command = command.replace('{name}', os.path.basename(file_path))

        self.log(f"[ACTION] {action_name}: {command}")

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=action.get('timeout', 60)
            )

            if result.returncode == 0:
                self.log(f"  [OK] {action_name} completed")
                if result.stdout:
                    self.log(f"  Output: {result.stdout.strip()}")
            else:
                self.log(f"  [ERROR] {action_name} failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            self.log(f"  [ERROR] {action_name} timed out")
        except Exception as e:
            self.log(f"  [ERROR] {action_name} failed: {e}")

    def on_modified(self, event):
        """Handle file modification."""
        if event.is_directory:
            return

        file_path = event.src_path
        if not self.matches_pattern(file_path):
            return

        if not self.should_process(file_path):
            return

        self.log(f"[MODIFIED] {file_path}")
        self.run_action('on_modify', file_path)

    def on_created(self, event):
        """Handle file creation."""
        if event.is_directory:
            return

        file_path = event.src_path
        if not self.matches_pattern(file_path):
            return

        self.log(f"[CREATED] {file_path}")
        self.run_action('on_create', file_path)

    def on_deleted(self, event):
        """Handle file deletion."""
        if event.is_directory:
            return

        file_path = event.src_path
        if not self.matches_pattern(file_path):
            return

        self.log(f"[DELETED] {file_path}")
        self.run_action('on_delete', file_path)


class FileWatcher:
    """File watcher for Claude workspace."""

    def __init__(self, config_file=None):
        """Initialize file watcher."""
        self.config_file = config_file
        self.config = self.load_config()
        self.observers = []

    def load_config(self):
        """Load watch configuration."""
        if self.config_file and os.path.exists(self.config_file):
            import json
            with open(self.config_file, 'r') as f:
                return json.load(f)

        # Default configuration
        return {
            'watches': [
                {
                    'name': 'TypeScript/JavaScript files',
                    'path': 'claude/projects',
                    'patterns': ['.ts', '.tsx', '.js', '.jsx'],
                    'debounce_seconds': 2,
                    'actions': {
                        'on_modify': {
                            'command': 'echo "File changed: {file}"',
                            'timeout': 30
                        }
                    }
                }
            ]
        }

    def save_default_config(self, output_path):
        """Save default configuration to file."""
        default_config = {
            'watches': [
                {
                    'name': 'TypeScript files - Run tests',
                    'path': 'claude/projects/active-genie-nginx/src',
                    'patterns': ['.ts', '.tsx'],
                    'debounce_seconds': 2,
                    'actions': {
                        'on_modify': {
                            'command': 'npm test -- --watch=false',
                            'timeout': 120
                        }
                    }
                },
                {
                    'name': 'Python files - Run linter',
                    'path': 'tools',
                    'patterns': ['.py'],
                    'debounce_seconds': 2,
                    'actions': {
                        'on_modify': {
                            'command': 'pylint {file}',
                            'timeout': 30
                        }
                    }
                },
                {
                    'name': 'Markdown files - Update timestamp',
                    'path': '.',
                    'patterns': ['.md'],
                    'debounce_seconds': 5,
                    'actions': {
                        'on_modify': {
                            'command': 'echo "Updated: {name}"',
                            'timeout': 10
                        }
                    }
                }
            ]
        }

        import json
        with open(output_path, 'w') as f:
            json.dump(default_config, f, indent=2)

        print(f"[OK] Default configuration saved to {output_path}")

    def start(self):
        """Start watching files."""
        print("\n" + "="*60)
        print("FILE WATCHER - Claude Workspace")
        print("="*60)

        watches = self.config.get('watches', [])
        if not watches:
            print("[ERROR] No watches configured")
            return 1

        for watch in watches:
            name = watch.get('name', 'Unnamed watch')
            path = watch.get('path', '.')
            full_path = os.path.abspath(path)

            if not os.path.exists(full_path):
                print(f"[WARNING] Path does not exist: {full_path}")
                continue

            print(f"\n[WATCH] {name}")
            print(f"  Path: {full_path}")
            print(f"  Patterns: {', '.join(watch.get('patterns', ['*']))}")

            # Create handler and observer
            handler = ProjectFileHandler(watch)
            observer = Observer()
            observer.schedule(handler, full_path, recursive=True)
            observer.start()
            self.observers.append(observer)

        print("\n[INFO] Press Ctrl+C to stop watching\n")

        # Run until interrupted
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[INFO] Stopping watchers...")
            for observer in self.observers:
                observer.stop()

            for observer in self.observers:
                observer.join()

            print("[OK] File watcher stopped")

        return 0


def main():
    """Main entry point for file watcher."""
    import argparse

    parser = argparse.ArgumentParser(description='File Watcher for Claude Workspace')
    parser.add_argument('action', choices=['start', 'config'],
                       help='Action: start (watch files) or config (generate config)')
    parser.add_argument('--config', help='Configuration file (JSON)')
    parser.add_argument('--output', help='Output path for config generation')

    args = parser.parse_args()

    watcher = FileWatcher(args.config)

    if args.action == 'start':
        sys.exit(watcher.start())
    elif args.action == 'config':
        output_path = args.output or 'file-watcher-config.json'
        watcher.save_default_config(output_path)
        sys.exit(0)


if __name__ == '__main__':
    main()
