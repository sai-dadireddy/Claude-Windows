#!/usr/bin/env python3
"""
Scheduled Tasks for Claude Workspace
Purpose: Cron-style automation for maintenance and cleanup
Date: 2025-10-01
"""

import os
import sys
import time
import schedule
import subprocess
from datetime import datetime
from pathlib import Path

class ScheduledTasks:
    def __init__(self, workspace_path=None):
        """Initialize scheduled tasks."""
        self.workspace_path = workspace_path or os.getcwd()
        self.log_file = os.path.join(self.workspace_path, 'tools', 'automation', 'scheduled-tasks.log')

    def log(self, message):
        """Log message to file and console."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)

        # Append to log file
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_message + '\n')
        except Exception as e:
            print(f"[ERROR] Could not write to log: {e}")

    def run_command(self, cmd, cwd=None):
        """Run a command and return success status."""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.workspace_path,
                capture_output=True,
                text=True,
                shell=True
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)

    def cleanup_build_outputs(self):
        """Clean up build outputs from all projects."""
        self.log("[CLEANUP] Starting build outputs cleanup...")

        projects_path = os.path.join(self.workspace_path, 'claude', 'projects')
        if not os.path.exists(projects_path):
            self.log("[SKIP] Projects directory not found")
            return

        cleaned_count = 0
        space_freed = 0

        # Find and remove build directories
        for project_dir in os.listdir(projects_path):
            project_path = os.path.join(projects_path, project_dir)
            if not os.path.isdir(project_path):
                continue

            # Common build output directories
            build_dirs = ['dist', 'build', '.angular', 'node_modules/.cache']

            for build_dir in build_dirs:
                build_path = os.path.join(project_path, build_dir)
                if os.path.exists(build_path) and os.path.isdir(build_path):
                    # Calculate size before deletion
                    try:
                        size = sum(
                            os.path.getsize(os.path.join(dirpath, filename))
                            for dirpath, dirnames, filenames in os.walk(build_path)
                            for filename in filenames
                        )
                        space_freed += size

                        # Remove directory
                        success, _, _ = self.run_command(f'rmdir /S /Q "{build_path}"')
                        if success:
                            cleaned_count += 1
                            self.log(f"  [OK] Removed {build_dir} from {project_dir} ({size/1024/1024:.1f} MB)")
                    except Exception as e:
                        self.log(f"  [ERROR] Could not remove {build_path}: {e}")

        self.log(f"[OK] Cleanup complete: {cleaned_count} directories, {space_freed/1024/1024:.1f} MB freed")

    def archive_old_sessions(self):
        """Archive old Claude sessions (>30 days)."""
        self.log("[ARCHIVE] Archiving old sessions...")

        # Check if sessions directory exists
        sessions_path = os.path.join(self.workspace_path, '.claude', 'sessions')
        if not os.path.exists(sessions_path):
            self.log("[SKIP] Sessions directory not found")
            return

        # Archive directory
        archive_path = os.path.join(self.workspace_path, '.claude', 'sessions-archive')
        os.makedirs(archive_path, exist_ok=True)

        # Find sessions older than 30 days
        cutoff_time = time.time() - (30 * 24 * 60 * 60)  # 30 days
        archived_count = 0

        try:
            for session_file in os.listdir(sessions_path):
                session_path = os.path.join(sessions_path, session_file)
                if os.path.isfile(session_path):
                    mtime = os.path.getmtime(session_path)
                    if mtime < cutoff_time:
                        # Move to archive
                        archive_file = os.path.join(archive_path, session_file)
                        os.rename(session_path, archive_file)
                        archived_count += 1

            self.log(f"[OK] Archived {archived_count} old session(s)")
        except Exception as e:
            self.log(f"[ERROR] Could not archive sessions: {e}")

    def update_dependencies(self):
        """Check for dependency updates in projects."""
        self.log("[UPDATE] Checking for dependency updates...")

        projects_path = os.path.join(self.workspace_path, 'claude', 'projects')
        if not os.path.exists(projects_path):
            self.log("[SKIP] Projects directory not found")
            return

        for project_dir in os.listdir(projects_path):
            project_path = os.path.join(projects_path, project_dir)
            if not os.path.isdir(project_path):
                continue

            # Check for package.json (Node.js projects)
            package_json = os.path.join(project_path, 'package.json')
            if os.path.exists(package_json):
                self.log(f"  [CHECK] {project_dir} (Node.js)")
                success, stdout, _ = self.run_command('npm outdated', cwd=project_path)
                if stdout:
                    self.log(f"    Outdated packages:\n{stdout}")

            # Check for requirements.txt (Python projects)
            requirements_txt = os.path.join(project_path, 'requirements.txt')
            if os.path.exists(requirements_txt):
                self.log(f"  [CHECK] {project_dir} (Python)")
                # Note: pip list --outdated requires pip to be available
                success, stdout, _ = self.run_command('pip list --outdated', cwd=project_path)
                if stdout:
                    self.log(f"    Outdated packages:\n{stdout}")

        self.log("[OK] Dependency check complete")

    def check_for_system_updates(self):
        """Check for updates to Claude tools."""
        self.log("[UPDATE] Checking for system updates...")

        # Check Git version
        success, stdout, _ = self.run_command('git --version')
        if success:
            self.log(f"  Git: {stdout.strip()}")

        # Check Python version
        success, stdout, _ = self.run_command('python --version')
        if success:
            self.log(f"  Python: {stdout.strip()}")

        # Check Node version
        success, stdout, _ = self.run_command('node --version')
        if success:
            self.log(f"  Node: {stdout.strip()}")

        self.log("[OK] System check complete")

    def run_security_scan(self):
        """Run basic security scan on projects."""
        self.log("[SECURITY] Running security scan...")

        projects_path = os.path.join(self.workspace_path, 'claude', 'projects')
        if not os.path.exists(projects_path):
            self.log("[SKIP] Projects directory not found")
            return

        issues_found = 0

        for project_dir in os.listdir(projects_path):
            project_path = os.path.join(projects_path, project_dir)
            if not os.path.isdir(project_path):
                continue

            # Check for Node.js vulnerabilities
            package_json = os.path.join(project_path, 'package.json')
            if os.path.exists(package_json):
                self.log(f"  [SCAN] {project_dir}")
                success, stdout, stderr = self.run_command('npm audit --audit-level=high', cwd=project_path)
                if not success and 'vulnerabilities' in stderr:
                    issues_found += 1
                    self.log(f"    [WARNING] Vulnerabilities found - run 'npm audit' in {project_dir}")

        if issues_found == 0:
            self.log("[OK] No security issues found")
        else:
            self.log(f"[WARNING] {issues_found} project(s) have security issues")

    def daily_checks(self):
        """Daily maintenance checks (runs every morning 9 AM)."""
        self.log("\n" + "="*60)
        self.log("DAILY CHECKS START")
        self.log("="*60)

        self.check_for_system_updates()
        self.run_security_scan()

        self.log("="*60)
        self.log("DAILY CHECKS COMPLETE")
        self.log("="*60 + "\n")

    def weekly_cleanup(self):
        """Weekly cleanup routine (runs every Friday 5 PM)."""
        self.log("\n" + "="*60)
        self.log("WEEKLY CLEANUP START")
        self.log("="*60)

        self.cleanup_build_outputs()
        self.archive_old_sessions()
        self.update_dependencies()

        self.log("="*60)
        self.log("WEEKLY CLEANUP COMPLETE")
        self.log("="*60 + "\n")

    def run_scheduler(self):
        """Run the task scheduler."""
        self.log("\n" + "="*60)
        self.log("SCHEDULED TASKS DAEMON STARTED")
        self.log("="*60)

        # Schedule tasks
        schedule.every().day.at("09:00").do(self.daily_checks)
        schedule.every().friday.at("17:00").do(self.weekly_cleanup)

        self.log("[INFO] Daily checks scheduled for 9:00 AM")
        self.log("[INFO] Weekly cleanup scheduled for Friday 5:00 PM")
        self.log("[INFO] Press Ctrl+C to stop\n")

        # Run scheduler
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.log("\n[INFO] Scheduler stopped by user")

    def run_once(self, task_name):
        """Run a specific task once."""
        tasks = {
            'daily': self.daily_checks,
            'weekly': self.weekly_cleanup,
            'cleanup': self.cleanup_build_outputs,
            'archive': self.archive_old_sessions,
            'update': self.update_dependencies,
            'security': self.run_security_scan,
        }

        if task_name not in tasks:
            print(f"[ERROR] Unknown task: {task_name}")
            print(f"Available tasks: {', '.join(tasks.keys())}")
            return 1

        tasks[task_name]()
        return 0


def main():
    """Main entry point for scheduled tasks."""
    import argparse

    parser = argparse.ArgumentParser(description='Scheduled Tasks for Claude Workspace')
    parser.add_argument('action', choices=['start', 'run'],
                       help='Action: start (daemon) or run (once)')
    parser.add_argument('--task', help='Task to run once (daily, weekly, cleanup, archive, update, security)')
    parser.add_argument('--path', help='Workspace path (default: current directory)')

    args = parser.parse_args()

    scheduler = ScheduledTasks(args.path)

    if args.action == 'start':
        scheduler.run_scheduler()
    elif args.action == 'run':
        if not args.task:
            print("[ERROR] --task required for 'run' action")
            sys.exit(1)
        sys.exit(scheduler.run_once(args.task))


if __name__ == '__main__':
    main()
