#!/usr/bin/env python3
"""
Build Monitor for Claude Workspace
Purpose: Monitor build processes and report status
Date: 2025-10-01
"""

import os
import sys
import time
import subprocess
import json
from datetime import datetime
from pathlib import Path

class BuildMonitor:
    """Monitor build processes and track status."""

    def __init__(self, workspace_path=None):
        """Initialize build monitor."""
        self.workspace_path = workspace_path or os.getcwd()
        self.status_file = os.path.join(self.workspace_path, 'tools', 'monitoring', 'build-status.json')
        self.log_file = os.path.join(self.workspace_path, 'tools', 'monitoring', 'build-monitor.log')

    def log(self, message):
        """Log message to file and console."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)

        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_message + '\n')
        except Exception as e:
            print(f"[ERROR] Could not write to log: {e}")

    def run_command(self, cmd, cwd=None, timeout=300):
        """Run a command and return success status."""
        try:
            start_time = time.time()
            result = subprocess.run(
                cmd,
                cwd=cwd or self.workspace_path,
                capture_output=True,
                text=True,
                shell=True,
                timeout=timeout
            )
            duration = time.time() - start_time

            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'duration': duration
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'stdout': '',
                'stderr': f'Command timed out after {timeout} seconds',
                'returncode': -1,
                'duration': timeout
            }
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'returncode': -1,
                'duration': 0
            }

    def save_status(self, project, build_type, status):
        """Save build status to file."""
        try:
            # Load existing status
            if os.path.exists(self.status_file):
                with open(self.status_file, 'r') as f:
                    all_status = json.load(f)
            else:
                all_status = {}

            # Update status
            if project not in all_status:
                all_status[project] = {}

            all_status[project][build_type] = {
                'success': status['success'],
                'timestamp': datetime.now().isoformat(),
                'duration': status['duration'],
                'returncode': status['returncode']
            }

            # Save
            os.makedirs(os.path.dirname(self.status_file), exist_ok=True)
            with open(self.status_file, 'w') as f:
                json.dump(all_status, f, indent=2)

        except Exception as e:
            self.log(f"[ERROR] Could not save status: {e}")

    def get_status(self, project=None):
        """Get build status."""
        try:
            if not os.path.exists(self.status_file):
                return {}

            with open(self.status_file, 'r') as f:
                all_status = json.load(f)

            if project:
                return all_status.get(project, {})
            return all_status

        except Exception as e:
            self.log(f"[ERROR] Could not read status: {e}")
            return {}

    def monitor_build(self, project_name, project_path, build_command, timeout=300):
        """Monitor a build process."""
        self.log(f"\n{'='*60}")
        self.log(f"BUILD MONITOR - {project_name}")
        self.log(f"{'='*60}")
        self.log(f"Command: {build_command}")
        self.log(f"Path: {project_path}")
        self.log(f"Timeout: {timeout}s")
        self.log(f"{'='*60}\n")

        # Run build
        self.log(f"[BUILD] Starting build for {project_name}...")
        result = self.run_command(build_command, cwd=project_path, timeout=timeout)

        # Report results
        if result['success']:
            self.log(f"[OK] Build succeeded ({result['duration']:.1f}s)")
            if result['stdout']:
                self.log(f"Output:\n{result['stdout']}")
        else:
            self.log(f"[ERROR] Build failed ({result['duration']:.1f}s)")
            self.log(f"Return code: {result['returncode']}")
            if result['stderr']:
                self.log(f"Error output:\n{result['stderr']}")

        # Save status
        self.save_status(project_name, 'build', result)

        return result

    def monitor_tests(self, project_name, project_path, test_command, timeout=300):
        """Monitor test execution."""
        self.log(f"\n{'='*60}")
        self.log(f"TEST MONITOR - {project_name}")
        self.log(f"{'='*60}")
        self.log(f"Command: {test_command}")
        self.log(f"Path: {project_path}")
        self.log(f"Timeout: {timeout}s")
        self.log(f"{'='*60}\n")

        # Run tests
        self.log(f"[TEST] Running tests for {project_name}...")
        result = self.run_command(test_command, cwd=project_path, timeout=timeout)

        # Report results
        if result['success']:
            self.log(f"[OK] Tests passed ({result['duration']:.1f}s)")
            if result['stdout']:
                self.log(f"Output:\n{result['stdout']}")
        else:
            self.log(f"[ERROR] Tests failed ({result['duration']:.1f}s)")
            self.log(f"Return code: {result['returncode']}")
            if result['stderr']:
                self.log(f"Error output:\n{result['stderr']}")

        # Save status
        self.save_status(project_name, 'test', result)

        return result

    def monitor_all_projects(self):
        """Monitor builds for all projects."""
        self.log(f"\n{'='*60}")
        self.log("MONITORING ALL PROJECTS")
        self.log(f"{'='*60}\n")

        projects_path = os.path.join(self.workspace_path, 'claude', 'projects')
        if not os.path.exists(projects_path):
            self.log("[ERROR] Projects directory not found")
            return

        results = {}

        for project_dir in os.listdir(projects_path):
            project_path = os.path.join(projects_path, project_dir)
            if not os.path.isdir(project_path):
                continue

            # Check for package.json (Node.js projects)
            package_json = os.path.join(project_path, 'package.json')
            if os.path.exists(package_json):
                self.log(f"\n[PROJECT] {project_dir} (Node.js)")

                # Try to build
                build_result = self.monitor_build(
                    project_dir,
                    project_path,
                    'npm run build',
                    timeout=600
                )
                results[f"{project_dir}/build"] = build_result['success']

                # Try to test
                test_result = self.monitor_tests(
                    project_dir,
                    project_path,
                    'npm test -- --watch=false',
                    timeout=300
                )
                results[f"{project_dir}/test"] = test_result['success']

            # Check for requirements.txt (Python projects)
            requirements_txt = os.path.join(project_path, 'requirements.txt')
            if os.path.exists(requirements_txt):
                self.log(f"\n[PROJECT] {project_dir} (Python)")

                # Try to test
                test_result = self.monitor_tests(
                    project_dir,
                    project_path,
                    'pytest',
                    timeout=300
                )
                results[f"{project_dir}/test"] = test_result['success']

        # Summary
        self.log(f"\n{'='*60}")
        self.log("SUMMARY")
        self.log(f"{'='*60}")

        total = len(results)
        passed = sum(1 for v in results.values() if v)
        failed = total - passed

        self.log(f"Total builds/tests: {total}")
        self.log(f"Passed: {passed}")
        self.log(f"Failed: {failed}")

        if failed == 0:
            self.log("[OK] All builds and tests passed!")
        else:
            self.log(f"[WARNING] {failed} build(s)/test(s) failed")

        self.log(f"{'='*60}\n")

    def show_status(self):
        """Show current build status."""
        status = self.get_status()

        if not status:
            print("[INFO] No build status available")
            return

        print("\n" + "="*60)
        print("BUILD STATUS")
        print("="*60 + "\n")

        for project, builds in status.items():
            print(f"Project: {project}")

            for build_type, info in builds.items():
                status_str = "[OK]" if info['success'] else "[FAIL]"
                timestamp = datetime.fromisoformat(info['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
                duration = info['duration']

                print(f"  {build_type}: {status_str} ({duration:.1f}s) - {timestamp}")

            print()

        print("="*60 + "\n")

    def watch_and_rebuild(self, project_name, project_path, build_command):
        """Watch for file changes and rebuild."""
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        class RebuildHandler(FileSystemEventHandler):
            def __init__(self, monitor, project_name, project_path, build_command):
                self.monitor = monitor
                self.project_name = project_name
                self.project_path = project_path
                self.build_command = build_command
                self.last_build_time = 0
                self.debounce_seconds = 2

            def on_modified(self, event):
                if event.is_directory:
                    return

                # Only rebuild for source files
                if not (event.src_path.endswith(('.ts', '.tsx', '.js', '.jsx', '.py'))):
                    return

                # Debounce
                now = time.time()
                if now - self.last_build_time < self.debounce_seconds:
                    return

                self.last_build_time = now

                # Rebuild
                self.monitor.log(f"[CHANGE] {event.src_path}")
                self.monitor.monitor_build(
                    self.project_name,
                    self.project_path,
                    self.build_command
                )

        self.log(f"[WATCH] Watching {project_path} for changes...")
        self.log("[INFO] Press Ctrl+C to stop\n")

        handler = RebuildHandler(self, project_name, project_path, build_command)
        observer = Observer()
        observer.schedule(handler, project_path, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.log("\n[INFO] Stopping watcher...")
            observer.stop()
            observer.join()
            self.log("[OK] Watcher stopped")


def main():
    """Main entry point for build monitor."""
    import argparse

    parser = argparse.ArgumentParser(description='Build Monitor for Claude Workspace')
    parser.add_argument('action', choices=['build', 'test', 'all', 'status', 'watch'],
                       help='Action to perform')
    parser.add_argument('--project', help='Project name')
    parser.add_argument('--path', help='Project path')
    parser.add_argument('--command', help='Build/test command')
    parser.add_argument('--timeout', type=int, default=300, help='Timeout in seconds')
    parser.add_argument('--workspace', help='Workspace path')

    args = parser.parse_args()

    monitor = BuildMonitor(args.workspace)

    if args.action == 'build':
        if not args.project or not args.path or not args.command:
            print("[ERROR] --project, --path, and --command required for build")
            sys.exit(1)
        result = monitor.monitor_build(args.project, args.path, args.command, args.timeout)
        sys.exit(0 if result['success'] else 1)

    elif args.action == 'test':
        if not args.project or not args.path or not args.command:
            print("[ERROR] --project, --path, and --command required for test")
            sys.exit(1)
        result = monitor.monitor_tests(args.project, args.path, args.command, args.timeout)
        sys.exit(0 if result['success'] else 1)

    elif args.action == 'all':
        monitor.monitor_all_projects()
        sys.exit(0)

    elif args.action == 'status':
        monitor.show_status()
        sys.exit(0)

    elif args.action == 'watch':
        if not args.project or not args.path or not args.command:
            print("[ERROR] --project, --path, and --command required for watch")
            sys.exit(1)
        monitor.watch_and_rebuild(args.project, args.path, args.command)
        sys.exit(0)


if __name__ == '__main__':
    main()
