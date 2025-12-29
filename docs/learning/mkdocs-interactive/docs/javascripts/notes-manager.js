/**
 * Notes Manager for AI Learning Syllabus
 * Handles auto-saving and loading of personal notes for each topic
 */

class NotesManager {
    constructor() {
        this.storageKey = 'ai-syllabus-progress';
        this.autoSaveDelay = 1000; // 1 second debounce
        this.saveTimers = {};
        this.init();
    }

    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupNotes());
        } else {
            this.setupNotes();
        }
    }

    setupNotes() {
        // Find all notes textareas
        const notesTextareas = document.querySelectorAll('.topic-notes-textarea');

        notesTextareas.forEach(textarea => {
            const topicId = textarea.getAttribute('data-notes-for');
            if (!topicId) return;

            // Load saved notes
            this.loadNotes(topicId, textarea);

            // Setup auto-save on input
            textarea.addEventListener('input', () => {
                this.scheduleAutoSave(topicId, textarea);
            });

            // Save on blur (when user clicks away)
            textarea.addEventListener('blur', () => {
                this.saveNotes(topicId, textarea);
            });
        });
    }

    loadNotes(topicId, textarea) {
        try {
            const data = JSON.parse(localStorage.getItem(this.storageKey) || '{}');
            const notes = data.notes || {};

            if (notes[topicId] && notes[topicId].content) {
                textarea.value = notes[topicId].content;
            }
        } catch (error) {
            console.error('Error loading notes:', error);
        }
    }

    scheduleAutoSave(topicId, textarea) {
        // Clear existing timer
        if (this.saveTimers[topicId]) {
            clearTimeout(this.saveTimers[topicId]);
        }

        // Schedule new save
        this.saveTimers[topicId] = setTimeout(() => {
            this.saveNotes(topicId, textarea);
        }, this.autoSaveDelay);
    }

    saveNotes(topicId, textarea) {
        try {
            // Load existing data
            const data = JSON.parse(localStorage.getItem(this.storageKey) || '{}');

            // Ensure notes object exists
            if (!data.notes) {
                data.notes = {};
            }

            // Save notes with timestamp
            data.notes[topicId] = {
                content: textarea.value,
                lastModified: new Date().toISOString()
            };

            // Save to localStorage
            localStorage.setItem(this.storageKey, JSON.stringify(data));

            // Show save indicator
            this.showSaveIndicator(textarea);
        } catch (error) {
            console.error('Error saving notes:', error);
            this.showErrorIndicator(textarea);
        }
    }

    showSaveIndicator(textarea) {
        // Find the auto-save indicator
        const container = textarea.closest('.topic-notes-container');
        if (!container) return;

        const indicator = container.querySelector('.notes-auto-save');
        if (!indicator) return;

        // Temporarily show "Saved!" message
        const originalText = indicator.textContent;
        indicator.textContent = '✅ Saved!';
        indicator.style.color = '#4caf50';

        setTimeout(() => {
            indicator.textContent = originalText;
            indicator.style.color = '';
        }, 2000);
    }

    showErrorIndicator(textarea) {
        const container = textarea.closest('.topic-notes-container');
        if (!container) return;

        const indicator = container.querySelector('.notes-auto-save');
        if (!indicator) return;

        indicator.textContent = '❌ Error saving';
        indicator.style.color = '#f44336';

        setTimeout(() => {
            indicator.textContent = '💾 Auto-saves';
            indicator.style.color = '';
        }, 3000);
    }

    // Export all notes as JSON
    exportNotes() {
        try {
            const data = JSON.parse(localStorage.getItem(this.storageKey) || '{}');
            const notes = data.notes || {};

            const exportData = {
                exportDate: new Date().toISOString(),
                notes: notes
            };

            const blob = new Blob([JSON.stringify(exportData, null, 2)], {
                type: 'application/json'
            });

            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `ai-syllabus-notes-${new Date().toISOString().split('T')[0]}.json`;
            a.click();

            URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Error exporting notes:', error);
        }
    }

    // Import notes from JSON
    importNotes(file) {
        const reader = new FileReader();

        reader.onload = (e) => {
            try {
                const importData = JSON.parse(e.target.result);

                if (!importData.notes) {
                    alert('Invalid notes file format');
                    return;
                }

                const data = JSON.parse(localStorage.getItem(this.storageKey) || '{}');
                data.notes = { ...data.notes, ...importData.notes };

                localStorage.setItem(this.storageKey, JSON.stringify(data));

                alert('Notes imported successfully! Refresh the page to see changes.');
            } catch (error) {
                console.error('Error importing notes:', error);
                alert('Error importing notes file');
            }
        };

        reader.readAsText(file);
    }
}

// Initialize notes manager when script loads
const notesManager = new NotesManager();

// Expose to window for debugging/export
window.notesManager = notesManager;
