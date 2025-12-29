/**
 * LocalStorage Sync for AI Learning Syllabus
 * Handles synchronization and backup of localStorage data
 */

class LocalStorageSync {
    constructor() {
        this.storageKey = 'ai-syllabus-progress';
        this.backupKey = 'ai-syllabus-progress-backup';
        this.lastSyncKey = 'ai-syllabus-last-sync';
        this.autoBackupInterval = 5 * 60 * 1000; // 5 minutes
        this.init();
    }

    init() {
        // Setup auto-backup
        this.startAutoBackup();

        // Check for data corruption on load
        this.checkDataIntegrity();

        // Expose sync functions to window
        window.syncProgress = {
            backup: () => this.createBackup(),
            restore: () => this.restoreFromBackup(),
            export: () => this.exportData(),
            import: (file) => this.importData(file),
            clear: () => this.clearAllData()
        };
    }

    startAutoBackup() {
        // Create initial backup
        this.createBackup();

        // Setup periodic backups
        setInterval(() => {
            this.createBackup();
        }, this.autoBackupInterval);

        // Backup before page unload
        window.addEventListener('beforeunload', () => {
            this.createBackup();
        });
    }

    createBackup() {
        try {
            const data = localStorage.getItem(this.storageKey);
            if (data) {
                localStorage.setItem(this.backupKey, data);
                localStorage.setItem(this.lastSyncKey, new Date().toISOString());
                console.log('Progress backed up successfully');
            }
        } catch (error) {
            console.error('Error creating backup:', error);
        }
    }

    restoreFromBackup() {
        try {
            const backup = localStorage.getItem(this.backupKey);
            if (backup) {
                localStorage.setItem(this.storageKey, backup);
                console.log('Progress restored from backup');
                alert('Progress restored from backup! Refresh the page to see changes.');
                return true;
            } else {
                alert('No backup found');
                return false;
            }
        } catch (error) {
            console.error('Error restoring from backup:', error);
            alert('Error restoring from backup');
            return false;
        }
    }

    checkDataIntegrity() {
        try {
            const data = localStorage.getItem(this.storageKey);
            if (data) {
                JSON.parse(data); // Try to parse to check validity
                return true;
            }
        } catch (error) {
            console.error('Data corruption detected, attempting restore:', error);
            return this.restoreFromBackup();
        }
        return true;
    }

    exportData() {
        try {
            const data = JSON.parse(localStorage.getItem(this.storageKey) || '{}');
            const lastSync = localStorage.getItem(this.lastSyncKey);

            const exportData = {
                version: '2.0',
                exportDate: new Date().toISOString(),
                lastSync: lastSync,
                data: data
            };

            const blob = new Blob([JSON.stringify(exportData, null, 2)], {
                type: 'application/json'
            });

            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `ai-syllabus-full-export-${new Date().toISOString().split('T')[0]}.json`;
            a.click();

            URL.revokeObjectURL(url);
            console.log('Data exported successfully');
        } catch (error) {
            console.error('Error exporting data:', error);
            alert('Error exporting data');
        }
    }

    importData(file) {
        const reader = new FileReader();

        reader.onload = (e) => {
            try {
                const importData = JSON.parse(e.target.result);

                if (!importData.data) {
                    alert('Invalid export file format');
                    return;
                }

                // Create backup of current data before import
                this.createBackup();

                // Import data
                localStorage.setItem(this.storageKey, JSON.stringify(importData.data));
                localStorage.setItem(this.lastSyncKey, new Date().toISOString());

                console.log('Data imported successfully');
                alert('Data imported successfully! Refresh the page to see changes.');
            } catch (error) {
                console.error('Error importing data:', error);
                alert('Error importing data. Your previous data is backed up.');
            }
        };

        reader.readAsText(file);
    }

    clearAllData() {
        if (!confirm('Are you sure you want to clear all progress and notes? This cannot be undone!')) {
            return;
        }

        // Create final backup
        this.createBackup();

        // Clear all data
        localStorage.removeItem(this.storageKey);
        localStorage.removeItem(this.lastSyncKey);

        console.log('All data cleared');
        alert('All progress and notes have been cleared. A backup was created. Refresh the page.');
    }

    getStorageInfo() {
        try {
            const data = localStorage.getItem(this.storageKey);
            const backup = localStorage.getItem(this.backupKey);
            const lastSync = localStorage.getItem(this.lastSyncKey);

            return {
                dataSize: data ? new Blob([data]).size : 0,
                backupSize: backup ? new Blob([backup]).size : 0,
                lastSync: lastSync,
                hasBackup: !!backup,
                isHealthy: this.checkDataIntegrity()
            };
        } catch (error) {
            console.error('Error getting storage info:', error);
            return null;
        }
    }

    // Cross-tab synchronization
    enableCrossTabSync() {
        window.addEventListener('storage', (e) => {
            if (e.key === this.storageKey) {
                console.log('Progress updated in another tab, reloading...');
                // Reload progress tracker
                if (window.progressTracker) {
                    window.progressTracker.data = window.progressTracker.loadProgress();
                    window.progressTracker.renderProgressBars();
                }
            }
        });
    }
}

// Initialize localStorage sync when script loads
const localStorageSync = new LocalStorageSync();

// Enable cross-tab sync
localStorageSync.enableCrossTabSync();

// Expose to window for debugging
window.localStorageSync = localStorageSync;

// Show storage info in console
console.log('Storage Info:', localStorageSync.getStorageInfo());
