/**
 * Progress Tracker for AI Learning Syllabus
 * Manages topic completion status using localStorage
 */

class ProgressTracker {
    constructor() {
        this.storageKey = 'ai-syllabus-progress';
        this.data = this.loadProgress();
        this.init();
    }

    init() {
        // Initialize checkboxes on page load
        document.addEventListener('DOMContentLoaded', () => {
            this.renderCheckboxes();
            this.renderProgressBars();
            this.attachEventListeners();
            this.updateDashboard();
        });
    }

    loadProgress() {
        const saved = localStorage.getItem(this.storageKey);
        return saved ? JSON.parse(saved) : {
            topics: {},
            notes: {},
            startDate: new Date().toISOString(),
            lastUpdated: new Date().toISOString()
        };
    }

    saveProgress() {
        this.data.lastUpdated = new Date().toISOString();
        localStorage.setItem(this.storageKey, JSON.stringify(this.data));
        this.updateDashboard();
    }

    renderCheckboxes() {
        // Find all topic sections with data-topic-id
        const topicSections = document.querySelectorAll('[data-topic-id]');

        topicSections.forEach(section => {
            const topicId = section.getAttribute('data-topic-id');
            const isCompleted = this.data.topics[topicId]?.completed || false;

            // Create checkbox container
            const checkboxContainer = document.createElement('div');
            checkboxContainer.className = 'topic-checkbox-container';
            checkboxContainer.innerHTML = `
                <label class="topic-checkbox">
                    <input type="checkbox"
                           data-topic-id="${topicId}"
                           ${isCompleted ? 'checked' : ''}>
                    <span class="checkbox-label">
                        ${isCompleted ? '✅ Completed' : '☐ Mark as Complete'}
                    </span>
                </label>
                <span class="completion-date">
                    ${isCompleted ? `Completed: ${this.formatDate(this.data.topics[topicId].completedDate)}` : ''}
                </span>
            `;

            // Insert at the beginning of the section
            section.insertBefore(checkboxContainer, section.firstChild);
        });
    }

    renderProgressBars() {
        const progressBars = document.querySelectorAll('[data-progress-group]');

        progressBars.forEach(bar => {
            const group = bar.getAttribute('data-progress-group');
            const progress = this.calculateProgress(group);

            bar.innerHTML = `
                <div class="progress-bar-container">
                    <div class="progress-bar-label">
                        <span>${group} Progress</span>
                        <span>${progress.completed}/${progress.total} (${progress.percentage}%)</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-bar-fill" style="width: ${progress.percentage}%"></div>
                    </div>
                </div>
            `;
        });
    }

    attachEventListeners() {
        // Checkbox change events
        document.addEventListener('change', (e) => {
            if (e.target.matches('input[type="checkbox"][data-topic-id]')) {
                const topicId = e.target.getAttribute('data-topic-id');
                this.toggleTopicCompletion(topicId, e.target.checked);
            }
        });

        // Notes textarea events
        document.addEventListener('blur', (e) => {
            if (e.target.matches('textarea[data-notes-for]')) {
                const topicId = e.target.getAttribute('data-notes-for');
                this.saveNotes(topicId, e.target.value);
            }
        }, true);

        // Export button
        const exportBtn = document.getElementById('export-progress');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportProgress());
        }

        // Reset button
        const resetBtn = document.getElementById('reset-progress');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => this.resetProgress());
        }
    }

    toggleTopicCompletion(topicId, completed) {
        if (!this.data.topics[topicId]) {
            this.data.topics[topicId] = {};
        }

        this.data.topics[topicId].completed = completed;
        this.data.topics[topicId].completedDate = completed ? new Date().toISOString() : null;

        this.saveProgress();
        this.updateCheckboxLabel(topicId, completed);
        this.renderProgressBars();
    }

    updateCheckboxLabel(topicId, completed) {
        const checkbox = document.querySelector(`input[data-topic-id="${topicId}"]`);
        if (checkbox) {
            const label = checkbox.nextElementSibling;
            const dateSpan = checkbox.closest('.topic-checkbox-container').querySelector('.completion-date');

            if (label) {
                label.textContent = completed ? '✅ Completed' : '☐ Mark as Complete';
            }

            if (dateSpan) {
                dateSpan.textContent = completed ?
                    `Completed: ${this.formatDate(new Date().toISOString())}` : '';
            }
        }
    }

    saveNotes(topicId, notes) {
        if (!this.data.notes[topicId]) {
            this.data.notes[topicId] = {};
        }

        this.data.notes[topicId].content = notes;
        this.data.notes[topicId].lastUpdated = new Date().toISOString();

        this.saveProgress();
    }

    calculateProgress(group) {
        const topicElements = document.querySelectorAll(`[data-topic-id^="${group}-"]`);
        const total = topicElements.length;
        const completed = Array.from(topicElements).filter(el => {
            const topicId = el.getAttribute('data-topic-id');
            return this.data.topics[topicId]?.completed;
        }).length;

        return {
            total,
            completed,
            percentage: total > 0 ? Math.round((completed / total) * 100) : 0
        };
    }

    calculateOverallProgress() {
        const allTopics = document.querySelectorAll('[data-topic-id]');
        const total = allTopics.length;
        const completed = Array.from(allTopics).filter(el => {
            const topicId = el.getAttribute('data-topic-id');
            return this.data.topics[topicId]?.completed;
        }).length;

        return {
            total,
            completed,
            percentage: total > 0 ? Math.round((completed / total) * 100) : 0
        };
    }

    updateDashboard() {
        const dashboard = document.getElementById('progress-dashboard');
        if (!dashboard) return;

        const overall = this.calculateOverallProgress();
        const daysStudying = this.calculateDaysStudying();

        dashboard.innerHTML = `
            <div class="dashboard-stats">
                <div class="stat-card">
                    <h3>Overall Progress</h3>
                    <div class="stat-value">${overall.percentage}%</div>
                    <div class="stat-detail">${overall.completed} of ${overall.total} topics</div>
                </div>

                <div class="stat-card">
                    <h3>Days Learning</h3>
                    <div class="stat-value">${daysStudying}</div>
                    <div class="stat-detail">Since ${this.formatDate(this.data.startDate)}</div>
                </div>

                <div class="stat-card">
                    <h3>Topics This Week</h3>
                    <div class="stat-value">${this.getTopicsCompletedThisWeek()}</div>
                    <div class="stat-detail">Last 7 days</div>
                </div>

                <div class="stat-card">
                    <h3>Current Streak</h3>
                    <div class="stat-value">${this.calculateStreak()}</div>
                    <div class="stat-detail">Consecutive days</div>
                </div>
            </div>

            <div class="dashboard-progress">
                <h3>Progress by Part</h3>
                ${this.renderPartProgressBars()}
            </div>

            <div class="dashboard-recent">
                <h3>Recently Completed</h3>
                ${this.renderRecentTopics()}
            </div>
        `;
    }

    renderPartProgressBars() {
        const parts = ['part1', 'part2', 'part3', 'part4', 'part5', 'part6',
                      'part7', 'part8', 'part9', 'part10', 'part11', 'part12'];

        return parts.map(part => {
            const progress = this.calculateProgress(part);
            return `
                <div class="part-progress">
                    <div class="part-progress-label">
                        <span>${part.toUpperCase()}</span>
                        <span>${progress.completed}/${progress.total}</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-bar-fill" style="width: ${progress.percentage}%"></div>
                    </div>
                </div>
            `;
        }).join('');
    }

    renderRecentTopics() {
        const recentTopics = Object.entries(this.data.topics)
            .filter(([_, data]) => data.completed)
            .sort((a, b) => new Date(b[1].completedDate) - new Date(a[1].completedDate))
            .slice(0, 5);

        if (recentTopics.length === 0) {
            return '<p class="no-recent">No topics completed yet. Start learning!</p>';
        }

        return `
            <ul class="recent-topics-list">
                ${recentTopics.map(([id, data]) => `
                    <li>
                        <span class="topic-name">${this.getTopicName(id)}</span>
                        <span class="topic-date">${this.formatDate(data.completedDate)}</span>
                    </li>
                `).join('')}
            </ul>
        `;
    }

    getTopicName(topicId) {
        // Extract readable name from topic ID
        return topicId.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    calculateDaysStudying() {
        const start = new Date(this.data.startDate);
        const today = new Date();
        const diffTime = Math.abs(today - start);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        return diffDays;
    }

    getTopicsCompletedThisWeek() {
        const oneWeekAgo = new Date();
        oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

        return Object.values(this.data.topics).filter(topic => {
            if (!topic.completed || !topic.completedDate) return false;
            return new Date(topic.completedDate) >= oneWeekAgo;
        }).length;
    }

    calculateStreak() {
        const completedTopics = Object.values(this.data.topics)
            .filter(t => t.completed)
            .map(t => new Date(t.completedDate).toDateString())
            .sort((a, b) => new Date(b) - new Date(a));

        if (completedTopics.length === 0) return 0;

        let streak = 1;
        const today = new Date().toDateString();
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);

        // Check if learned today or yesterday
        if (completedTopics[0] !== today && completedTopics[0] !== yesterday.toDateString()) {
            return 0;
        }

        for (let i = 1; i < completedTopics.length; i++) {
            const current = new Date(completedTopics[i]);
            const previous = new Date(completedTopics[i - 1]);
            const diffDays = (previous - current) / (1000 * 60 * 60 * 24);

            if (diffDays <= 1) {
                streak++;
            } else {
                break;
            }
        }

        return streak;
    }

    formatDate(isoString) {
        const date = new Date(isoString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }

    exportProgress() {
        const exportData = {
            ...this.data,
            exportDate: new Date().toISOString(),
            overallProgress: this.calculateOverallProgress()
        };

        const blob = new Blob([JSON.stringify(exportData, null, 2)], {
            type: 'application/json'
        });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `ai-syllabus-progress-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }

    resetProgress() {
        if (confirm('Are you sure you want to reset all progress? This cannot be undone.')) {
            localStorage.removeItem(this.storageKey);
            location.reload();
        }
    }
}

// Initialize the progress tracker
const progressTracker = new ProgressTracker();
