
## [2025-12-15 18:05:56]
Script deployment by server type:

COMMON SCRIPTS (ALL servers - APP, WEB, PRCS, DB, S3 Backup):
- disk_usage_monitor.sh - Disk usage monitoring
- dnf_weekly_update.sh - Weekly DNF patching
- dnf_weekly_reboot_check.sh - Weekly reboot check

PEOPLESOFT SERVERS ONLY (APP, WEB, PRCS):
- psoft_shutdown_handler.sh - Graceful shutdown before reboot
- psoft_startup_handler.sh - Startup on boot (via rc.local)
- start_domain.sh - Start individual domain
- stop_domain.sh - Stop individual domain

S3 BACKUP SERVER ONLY:
- s3_bucket_sync_daily.sh - Daily EFS to S3 sync
- s3_bucket_weekly_dbbackups_validation.sh - Weekly backup validation

Cron Schedule Summary:
- Disk monitoring: Daily on ALL servers
- DNF updates: Weekly on ALL servers  
- Reboot check: Weekly on ALL servers (after DNF)
- S3 sync: Daily on S3 backup server
- S3 validation: Weekly on S3 backup server
