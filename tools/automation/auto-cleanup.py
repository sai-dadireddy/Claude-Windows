#!/usr/bin/env python3
"""
Auto-Cleanup Routine for Claude Workspace
Purpose: Clean up temporary files, caches, and build outputs
Date: 2025-10-01
"""

import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

class AutoCleanup:
    def __init__(self, workspace_path=None, dry_run=False):
        """Initialize auto-cleanup."""
        self.workspace_path = workspace_path or os.getcwd()
        self.dry_run = dry_run
        self.cleaned_files = 0
        self.cleaned_dirs = 0
        self.space_freed = 0

    def log(self, message):
        """Log message."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prefix = "[DRY RUN] " if self.dry_run else ""
        print(f"[{timestamp}] {prefix}{message}")

    def get_size(self, path):
        """Get size of file or directory in bytes."""
        try:
            if os.path.isfile(path):
                return os.path.getsize(path)
            elif os.path.isdir(path):
                total = 0
                for dirpath, dirnames, filenames in os.walk(path):
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        try:
                            total += os.path.getsize(filepath)
                        except:
                            pass
                return total
        except:
            return 0

    def remove_file(self, file_path):
        """Remove a file."""
        try:
            size = self.get_size(file_path)
            if not self.dry_run:
                os.remove(file_path)
            self.cleaned_files += 1
            self.space_freed += size
            return True
        except Exception as e:
            self.log(f"  [ERROR] Could not remove {file_path}: {e}")
            return False

    def remove_directory(self, dir_path):
        """Remove a directory."""
        try:
            size = self.get_size(dir_path)
            if not self.dry_run:
                shutil.rmtree(dir_path)
            self.cleaned_dirs += 1
            self.space_freed += size
            return True
        except Exception as e:
            self.log(f"  [ERROR] Could not remove {dir_path}: {e}")
            return False

    def clean_node_modules_cache(self):
        """Clean node_modules/.cache directories."""
        self.log("[CLEAN] Node.js cache directories...")

        projects_path = os.path.join(self.workspace_path, 'claude', 'projects')
        if not os.path.exists(projects_path):
            return

        for project_dir in os.listdir(projects_path):
            project_path = os.path.join(projects_path, project_dir)
            cache_path = os.path.join(project_path, 'node_modules', '.cache')

            if os.path.exists(cache_path) and os.path.isdir(cache_path):
                size_mb = self.get_size(cache_path) / 1024 / 1024
                if self.remove_directory(cache_path):
                    self.log(f"  [OK] Removed cache from {project_dir} ({size_mb:.1f} MB)")

    def clean_angular_cache(self):
        """Clean .angular cache directories."""
        self.log("[CLEAN] Angular cache directories...")

        projects_path = os.path.join(self.workspace_path, 'claude', 'projects')
        if not os.path.exists(projects_path):
            return

        for project_dir in os.listdir(projects_path):
            project_path = os.path.join(projects_path, project_dir)
            angular_path = os.path.join(project_path, '.angular')

            if os.path.exists(angular_path) and os.path.isdir(angular_path):
                size_mb = self.get_size(angular_path) / 1024 / 1024
                if self.remove_directory(angular_path):
                    self.log(f"  [OK] Removed .angular from {project_dir} ({size_mb:.1f} MB)")

    def clean_python_cache(self):
        """Clean Python __pycache__ and .pyc files."""
        self.log("[CLEAN] Python cache files...")

        # Find all __pycache__ directories
        for root, dirs, files in os.walk(self.workspace_path):
            # Skip unified-memory and .git directories
            if 'unified-memory' in root or '.git' in root:
                continue

            if '__pycache__' in dirs:
                pycache_path = os.path.join(root, '__pycache__')
                size_mb = self.get_size(pycache_path) / 1024 / 1024
                if self.remove_directory(pycache_path):
                    rel_path = os.path.relpath(pycache_path, self.workspace_path)
                    self.log(f"  [OK] Removed {rel_path} ({size_mb:.1f} MB)")

            # Remove .pyc files
            for file in files:
                if file.endswith('.pyc'):
                    pyc_path = os.path.join(root, file)
                    if self.remove_file(pyc_path):
                        rel_path = os.path.relpath(pyc_path, self.workspace_path)
                        self.log(f"  [OK] Removed {rel_path}")

    def clean_log_files(self):
        """Clean old log files (>7 days)."""
        self.log("[CLEAN] Old log files...")

        import time
        cutoff_time = time.time() - (7 * 24 * 60 * 60)  # 7 days

        for root, dirs, files in os.walk(self.workspace_path):
            # Skip unified-memory and .git
            if 'unified-memory' in root or '.git' in root:
                continue

            for file in files:
                if file.endswith('.log'):
                    log_path = os.path.join(root, file)
                    try:
                        mtime = os.path.getmtime(log_path)
                        if mtime < cutoff_time:
                            size_kb = self.get_size(log_path) / 1024
                            if self.remove_file(log_path):
                                rel_path = os.path.relpath(log_path, self.workspace_path)
                                self.log(f"  [OK] Removed {rel_path} ({size_kb:.1f} KB)")
                    except:
                        pass

    def clean_temp_files(self):
        """Clean temporary files."""
        self.log("[CLEAN] Temporary files...")

        temp_patterns = [
            '*.tmp',
            '*.temp',
            '*~',
            '.DS_Store',
            'Thumbs.db',
        ]

        for root, dirs, files in os.walk(self.workspace_path):
            # Skip unified-memory and .git
            if 'unified-memory' in root or '.git' in root:
                continue

            for file in files:
                for pattern in temp_patterns:
                    if pattern.startswith('*'):
                        # Extension match
                        if file.endswith(pattern[1:]):
                            temp_path = os.path.join(root, file)
                            if self.remove_file(temp_path):
                                rel_path = os.path.relpath(temp_path, self.workspace_path)
                                self.log(f"  [OK] Removed {rel_path}")
                    else:
                        # Exact match
                        if file == pattern:
                            temp_path = os.path.join(root, file)
                            if self.remove_file(temp_path):
                                rel_path = os.path.relpath(temp_path, self.workspace_path)
                                self.log(f"  [OK] Removed {rel_path}")

    def clean_build_outputs(self):
        """Clean build output directories."""
        self.log("[CLEAN] Build output directories...")

        projects_path = os.path.join(self.workspace_path, 'claude', 'projects')
        if not os.path.exists(projects_path):
            return

        build_dirs = ['dist', 'build', 'out', '.next']

        for project_dir in os.listdir(projects_path):
            project_path = os.path.join(projects_path, project_dir)

            for build_dir in build_dirs:
                build_path = os.path.join(project_path, build_dir)
                if os.path.exists(build_path) and os.path.isdir(build_path):
                    size_mb = self.get_size(build_path) / 1024 / 1024
                    if self.remove_directory(build_path):
                        self.log(f"  [OK] Removed {build_dir} from {project_dir} ({size_mb:.1f} MB)")

    def clean_npm_cache(self):
        """Clean npm cache."""
        self.log("[CLEAN] npm cache...")

        import subprocess
        try:
            if not self.dry_run:
                result = subprocess.run(['npm', 'cache', 'clean', '--force'],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self.log("  [OK] npm cache cleaned")
                else:
                    self.log(f"  [ERROR] npm cache clean failed: {result.stderr}")
            else:
                self.log("  [DRY RUN] Would clean npm cache")
        except Exception as e:
            self.log(f"  [ERROR] Could not clean npm cache: {e}")

    def run(self, clean_all=False):
        """Run cleanup routine."""
        self.log("\n" + "="*60)
        self.log("AUTO-CLEANUP ROUTINE START")
        self.log("="*60)

        if self.dry_run:
            self.log("[INFO] Running in DRY RUN mode (no files will be deleted)")

        # Safe cleanups (always run)
        self.clean_node_modules_cache()
        self.clean_angular_cache()
        self.clean_python_cache()
        self.clean_log_files()
        self.clean_temp_files()

        # Aggressive cleanups (only if --all flag)
        if clean_all:
            self.log("\n[INFO] Running aggressive cleanup (--all flag)")
            self.clean_build_outputs()
            self.clean_npm_cache()

        # Report
        self.log("\n" + "="*60)
        self.log(f"[OK] Cleanup complete:")
        self.log(f"  Files removed: {self.cleaned_files}")
        self.log(f"  Directories removed: {self.cleaned_dirs}")
        self.log(f"  Space freed: {self.space_freed / 1024 / 1024:.1f} MB")
        self.log("="*60 + "\n")

        return 0


def main():
    """Main entry point for auto-cleanup."""
    import argparse

    parser = argparse.ArgumentParser(description='Auto-Cleanup Routine for Claude Workspace')
    parser.add_argument('--path', help='Workspace path (default: current directory)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be deleted without actually deleting')
    parser.add_argument('--all', action='store_true',
                       help='Run aggressive cleanup (includes build outputs)')

    args = parser.parse_args()

    cleanup = AutoCleanup(args.path, dry_run=args.dry_run)
    sys.exit(cleanup.run(clean_all=args.all))


if __name__ == '__main__':
    main()
