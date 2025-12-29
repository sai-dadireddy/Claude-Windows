
## [2025-12-15 18:04:04]
PeopleSoft Infrastructure Architecture:
- APP Servers: RHEL 8 Linux (Application Server domains)
- PRCS Servers: RHEL 8 Linux (Process Scheduler domains)  
- WEB Servers: RHEL 8 Linux (PIA/WebLogic web servers)
- PSNT Server: Windows Server 2022 (PeopleSoft NT scheduler)
- DB Servers: RHEL 8 Linux (Oracle Database)
- S3 Backup Server: RHEL 8 Linux (dedicated for S3 backup operations)

Storage:
- /s3backups: Common EFS mount shared across ALL servers
- All monitoring/automation scripts located in /s3backups/scripts_monitoring/
- S3 backup server pushes backups to S3 bucket and validates them

Script Locations on Servers:
- /s3backups/scripts_monitoring/disk_usage_monitor.sh
- /s3backups/scripts_monitoring/dnf_weekly_update.sh
- /s3backups/scripts_monitoring/dnf_weekly_reboot_check.sh
- /s3backups/scripts_monitoring/psoft_shutdown_handler.sh
- /s3backups/scripts_monitoring/psoft_startup_handler.sh
- /s3backups/scripts_monitoring/start_domain.sh
- /s3backups/scripts_monitoring/stop_domain.sh
- /s3backups/scripts_monitoring/s3_bucket_sync_daily.sh
- /s3backups/scripts_monitoring/s3_bucket_weekly_dbbackups_validation.sh

Server Type Detection:
- /home/psoft/server_type.txt contains: APP, UNX, or WEB
- Domain configs in /u01/app/psoft/ps_cfg_homes/<domain>/
- Environment scripts in /home/psoft/<domain>.sh
