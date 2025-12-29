#!/usr/bin/env python3
"""
Alert Manager for Claude Workspace
Purpose: Send alerts via email, desktop notifications, etc.
Date: 2025-10-01
"""

import os
import sys
import json
import smtplib
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

class AlertManager:
    """Manage alerts for Claude workspace."""

    def __init__(self, config_file=None):
        """Initialize alert manager."""
        self.config_file = config_file or os.path.join(
            os.getcwd(), 'tools', 'monitoring', 'alert-config.json'
        )
        self.config = self.load_config()

    def load_config(self):
        """Load alert configuration."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[WARNING] Could not load config: {e}")

        # Default configuration
        return {
            'email': {
                'enabled': False,
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'from_email': 'your-email@gmail.com',
                'to_email': 'your-email@gmail.com',
                'password': 'your-app-password'
            },
            'desktop': {
                'enabled': True
            },
            'log': {
                'enabled': True,
                'file': 'tools/monitoring/alerts.log'
            }
        }

    def save_default_config(self, output_path):
        """Save default configuration."""
        default_config = {
            'email': {
                'enabled': False,
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'from_email': 'your-email@gmail.com',
                'to_email': 'your-email@gmail.com',
                'password': 'your-app-password',
                'note': 'For Gmail, use app-specific password from https://myaccount.google.com/apppasswords'
            },
            'desktop': {
                'enabled': True,
                'note': 'Desktop notifications work on Windows, Mac, and Linux'
            },
            'log': {
                'enabled': True,
                'file': 'tools/monitoring/alerts.log'
            }
        }

        with open(output_path, 'w') as f:
            json.dump(default_config, f, indent=2)

        print(f"[OK] Configuration template saved to {output_path}")
        print(f"[INFO] Edit the file to configure email alerts")

    def log_alert(self, level, title, message):
        """Log alert to file."""
        if not self.config.get('log', {}).get('enabled', True):
            return

        log_file = self.config.get('log', {}).get('file', 'tools/monitoring/alerts.log')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {title}: {message}\n"

        try:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_message)
        except Exception as e:
            print(f"[ERROR] Could not write to log: {e}")

    def send_email(self, subject, body):
        """Send email alert."""
        email_config = self.config.get('email', {})

        if not email_config.get('enabled', False):
            print("[INFO] Email alerts disabled")
            return False

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = email_config['from_email']
            msg['To'] = email_config['to_email']
            msg['Subject'] = f"[Claude Workspace] {subject}"

            # Add body
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_body = f"""
{body}

---
Timestamp: {timestamp}
Source: Claude Workspace Alert Manager
"""
            msg.attach(MIMEText(full_body, 'plain'))

            # Send email
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['from_email'], email_config['password'])
            server.send_message(msg)
            server.quit()

            print(f"[OK] Email sent: {subject}")
            return True

        except Exception as e:
            print(f"[ERROR] Could not send email: {e}")
            return False

    def send_desktop_notification(self, title, message):
        """Send desktop notification."""
        desktop_config = self.config.get('desktop', {})

        if not desktop_config.get('enabled', True):
            print("[INFO] Desktop notifications disabled")
            return False

        try:
            # Windows
            if sys.platform == 'win32':
                # Use PowerShell for Windows notifications
                ps_script = f"""
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.UI.Notifications.ToastNotification, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

$template = @"
<toast>
    <visual>
        <binding template="ToastText02">
            <text id="1">{title}</text>
            <text id="2">{message}</text>
        </binding>
    </visual>
</toast>
"@

$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($template)
$toast = New-Object Windows.UI.Notifications.ToastNotification $xml
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Claude Workspace").Show($toast)
"""
                subprocess.run(['powershell', '-Command', ps_script], check=False)

            # macOS
            elif sys.platform == 'darwin':
                subprocess.run([
                    'osascript', '-e',
                    f'display notification "{message}" with title "{title}"'
                ])

            # Linux
            else:
                subprocess.run(['notify-send', title, message])

            print(f"[OK] Desktop notification sent: {title}")
            return True

        except Exception as e:
            print(f"[WARNING] Could not send desktop notification: {e}")
            return False

    def send_alert(self, level, title, message):
        """
        Send alert via configured channels.

        Args:
            level: Alert level (info, warning, error, critical)
            title: Alert title
            message: Alert message
        """
        print(f"\n{'='*60}")
        print(f"[{level.upper()}] {title}")
        print(f"{'='*60}")
        print(message)
        print(f"{'='*60}\n")

        # Log alert
        self.log_alert(level, title, message)

        # Send desktop notification for warnings and errors
        if level in ['warning', 'error', 'critical']:
            self.send_desktop_notification(title, message)

        # Send email for critical alerts
        if level == 'critical':
            self.send_email(title, message)

    def info(self, title, message):
        """Send info alert."""
        self.send_alert('info', title, message)

    def warning(self, title, message):
        """Send warning alert."""
        self.send_alert('warning', title, message)

    def error(self, title, message):
        """Send error alert."""
        self.send_alert('error', title, message)

    def critical(self, title, message):
        """Send critical alert."""
        self.send_alert('critical', title, message)

    def test_alerts(self):
        """Test all alert channels."""
        print("[TEST] Testing alert channels...\n")

        # Test log
        self.log_alert('test', 'Test Alert', 'Testing log functionality')
        print("[OK] Log alert sent")

        # Test desktop
        if self.config.get('desktop', {}).get('enabled', True):
            self.send_desktop_notification('Test Alert', 'Testing desktop notification')
        else:
            print("[SKIP] Desktop notifications disabled")

        # Test email
        if self.config.get('email', {}).get('enabled', False):
            self.send_email('Test Alert', 'Testing email functionality')
        else:
            print("[SKIP] Email alerts disabled")

        print("\n[OK] Alert test complete")


def main():
    """Main entry point for alert manager."""
    import argparse

    parser = argparse.ArgumentParser(description='Alert Manager for Claude Workspace')
    parser.add_argument('action', choices=['send', 'test', 'config'],
                       help='Action to perform')
    parser.add_argument('--level', choices=['info', 'warning', 'error', 'critical'],
                       default='info', help='Alert level')
    parser.add_argument('--title', help='Alert title')
    parser.add_argument('--message', help='Alert message')
    parser.add_argument('--config', help='Configuration file')
    parser.add_argument('--output', help='Output path for config generation')

    args = parser.parse_args()

    manager = AlertManager(args.config)

    if args.action == 'send':
        if not args.title or not args.message:
            print("[ERROR] --title and --message required for send")
            sys.exit(1)

        manager.send_alert(args.level, args.title, args.message)
        sys.exit(0)

    elif args.action == 'test':
        manager.test_alerts()
        sys.exit(0)

    elif args.action == 'config':
        output_path = args.output or 'alert-config.json'
        manager.save_default_config(output_path)
        sys.exit(0)


if __name__ == '__main__':
    main()
