/**
 * MBA Job Dashboard - Main Application
 */

class JobDashboard {
    constructor() {
        this.allJobs = [];
        this.filteredJobs = [];
        this.savedJobs = new Set();
        this.init();
    }

    init() {
        this.loadSavedJobs();
        this.attachEventListeners();
        this.loadJobs();
    }

    attachEventListeners() {
        // Search
        document.getElementById('search-input').addEventListener('input', () => this.filterJobs());

        // Filters
        document.getElementById('location-filter').addEventListener('change', () => this.filterJobs());
        document.getElementById('source-filter').addEventListener('change', () => this.filterJobs());
        document.getElementById('job-type-filter').addEventListener('change', () => this.filterJobs());
        document.getElementById('sort-by').addEventListener('change', () => this.filterJobs());

        // Buttons
        document.getElementById('clear-filters').addEventListener('click', () => this.clearFilters());
        document.getElementById('export-btn').addEventListener('click', () => this.exportToCSV());

        // Modal close
        document.querySelector('.close').addEventListener('click', () => this.closeModal());
        window.addEventListener('click', (e) => {
            const modal = document.getElementById('job-modal');
            if (e.target === modal) this.closeModal();
        });
    }

    async loadJobs() {
        const loadingEl = document.getElementById('loading');
        loadingEl.style.display = 'block';

        try {
            // file:// pages often block fetch; prefer preloaded JS payload when available
            if (window.__JOBS_DATA__ && Array.isArray(window.__JOBS_DATA__.jobs)) {
                this.allJobs = window.__JOBS_DATA__.jobs;
            } else {
                const response = await fetch('./data/jobs.json');
                if (!response.ok) throw new Error('Failed to load jobs');
                const data = await response.json();
                this.allJobs = data.jobs || [];
            }

            console.log(`Loaded ${this.allJobs.length} jobs`);

            this.updateStats();
            this.filterJobs();
        } catch (error) {
            console.error('Error loading jobs:', error);
            document.getElementById('no-results').style.display = 'block';
            document.getElementById('no-results').innerHTML = `
                <p>⚠️ Could not load jobs. Please run the scraper first:</p>
                <p style="margin-top: 10px; font-size: 12px;">
                    <code>cd scraper && python main.py</code>
                </p>
            `;
        } finally {
            loadingEl.style.display = 'none';
        }
    }

    filterJobs() {
        const searchTerm = document.getElementById('search-input').value.toLowerCase();
        const location = document.getElementById('location-filter').value;
        const source = document.getElementById('source-filter').value;
        const jobType = document.getElementById('job-type-filter').value;
        const sortBy = document.getElementById('sort-by').value;

        this.filteredJobs = this.allJobs.filter(job => {
            const matchesSearch = 
                job.title.toLowerCase().includes(searchTerm) ||
                job.company.toLowerCase().includes(searchTerm) ||
                job.location.toLowerCase().includes(searchTerm) ||
                job.description.toLowerCase().includes(searchTerm);

            const matchesLocation = 
                location === 'all' ||
                (location === 'bangalore' && (job.location.toLowerCase().includes('bangalore') || job.location.toLowerCase().includes('bengaluru'))) ||
                (location === 'remote' && job.location.toLowerCase().includes('remote'));

            const matchesSource = source === 'all' || job.source === source;

            const matchesJobType = jobType === 'all' || job.job_type === jobType;

            return matchesSearch && matchesLocation && matchesSource && matchesJobType;
        });

        // Apply Sorting
        if (sortBy === 'score') {
            this.filteredJobs.sort((a, b) => (b.score || 0) - (a.score || 0));
        } else if (sortBy === 'published_at') {
            // Sort by published_at (recent first), then by discovered_at (recent first)
            this.filteredJobs.sort((a, b) => {
                const dateA = new Date(a.published_at || 0);
                const dateB = new Date(b.published_at || 0);
                if (dateB - dateA !== 0) return dateB - dateA;
                return new Date(b.discovered_at || 0) - new Date(a.discovered_at || 0);
            });
        } else if (sortBy === 'discovered_at') {
            // Sort by discovered_at (recent first), then by published_at (recent first)
            this.filteredJobs.sort((a, b) => {
                const dateA = new Date(a.discovered_at || 0);
                const dateB = new Date(b.discovered_at || 0);
                if (dateB - dateA !== 0) return dateB - dateA;
                return new Date(b.published_at || 0) - new Date(a.published_at || 0);
            });
        }

        this.renderJobs();
    }

    renderJobs() {
        const container = document.getElementById('jobs-grid');
        const noResults = document.getElementById('no-results');
        const sortBy = document.getElementById('sort-by').value;

        if (this.filteredJobs.length === 0) {
            container.innerHTML = '';
            noResults.style.display = 'block';
            return;
        }

        noResults.style.display = 'none';

        if (sortBy === 'score') {
            container.innerHTML = this.filteredJobs.map(job => this.createJobCard(job)).join('');
        } else {
            // Group by date
            const groups = {};
            this.filteredJobs.forEach(job => {
                const date = job[sortBy] || 'Unknown Date';
                if (!groups[date]) groups[date] = [];
                groups[date].push(job);
            });

            // Get sorted dates (descending)
            const sortedDates = Object.keys(groups).sort((a, b) => new Date(b) - new Date(a));

            let html = '';
            sortedDates.forEach(date => {
                const dateLabel = date === 'Unknown Date' ? date : new Date(date).toLocaleDateString('en-GB');
                html += `
                    <div class="date-section">
                        <h2 class="date-header">${dateLabel}</h2>
                        <div class="date-jobs-grid">
                            ${groups[date].map(job => this.createJobCard(job)).join('')}
                        </div>
                    </div>
                `;
            });
            container.innerHTML = html;
        }

        // Attach save button listeners
        document.querySelectorAll('.save-job-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleSaveJob(btn.dataset.jobId);
            });
        });

        // Attach view details listeners
        document.querySelectorAll('.job-card').forEach((card) => {
            card.addEventListener('click', (event) => {
                if (event.target.closest('.job-actions')) return;
                const jobId = card.querySelector('.save-job-btn').dataset.jobId;
                const job = this.allJobs.find(j => this.getJobId(j) === jobId);
                if (job) this.showJobDetails(job);
            });
        });
    }

    createJobCard(job) {
        const jobId = this.getJobId(job);
        const isSaved = this.savedJobs.has(jobId);
        const score = job.score || 0;
        
        // Ranking styles
        let rankingClass = '';
        if (score >= 4) {
            rankingClass = 'high-score';
        } else if (score > 0) {
            rankingClass = 'low-score';
        }

        const pubDate = job.published_at ? new Date(job.published_at).toLocaleDateString('en-GB') : 'N/A';
        const discDate = job.discovered_at ? new Date(job.discovered_at).toLocaleDateString('en-GB') : 'N/A';

        return `
            <div class="job-card ${isSaved ? 'saved' : ''} ${rankingClass}">
                <div class="job-dates">
                    <span>🗓️ Published: ${pubDate}</span>
                    <span>🔍 Scanned: ${discDate}</span>
                </div>
                ${score > 0 ? `<div class="job-score">🎯 Match Score: ${score}/5</div>` : ''}
                <div class="job-header">
                    <h3 class="job-title">${this.escapeHtml(job.title)}</h3>
                    <p class="job-company">${this.escapeHtml(job.company)}</p>
                </div>

                <div class="job-meta">
                    <span class="badge location">📍 ${this.escapeHtml(job.location)}</span>
                    ${job.job_type ? `<span class="badge">💼 ${this.escapeHtml(job.job_type)}</span>` : ''}
                    <span class="badge source">${this.escapeHtml(job.source)}</span>
                </div>

                ${job.salary ? `<div class="job-salary">💰 ${this.escapeHtml(job.salary)}</div>` : ''}

                <p class="job-description">${this.escapeHtml(job.description)}</p>

                <div class="job-actions">
                    <a href="${job.url}" target="_blank" class="btn btn-primary" style="text-decoration: none;">
                        View on ${job.source}
                    </a>
                    <button class="btn ${isSaved ? 'btn-danger' : 'btn-success'} save-job-btn" data-job-id="${jobId}">
                        ${isSaved ? '❌ Unsave' : '💾 Save'}
                    </button>
                </div>
            </div>
        `;
    }

    showJobDetails(job) {
        const modal = document.getElementById('job-modal');
        const modalBody = document.getElementById('modal-body');

        modalBody.innerHTML = `
            <h2>${this.escapeHtml(job.title)}</h2>
            <h3 style="color: var(--gray-500); margin-bottom: 20px;">${this.escapeHtml(job.company)}</h3>

            <div style="margin-bottom: 20px;">
                <p><strong>📍 Location:</strong> ${this.escapeHtml(job.location)}</p>
                <p><strong>💼 Type:</strong> ${this.escapeHtml(job.job_type)}</p>
                <p><strong>🏢 Source:</strong> ${this.escapeHtml(job.source)}</p>
                ${job.experience ? `<p><strong>⏰ Experience:</strong> ${this.escapeHtml(job.experience)}</p>` : ''}
                ${job.salary ? `<p><strong>💰 Salary:</strong> ${this.escapeHtml(job.salary)}</p>` : ''}
            </div>

            <div style="margin-bottom: 20px;">
                <h4>Description</h4>
                <p>${this.escapeHtml(job.description)}</p>
            </div>

            <div style="display: flex; gap: 10px;">
                <a href="${job.url}" target="_blank" class="btn btn-primary" style="flex: 1; text-align: center; text-decoration: none;">
                    Apply Now
                </a>
                <button class="btn btn-secondary" onclick="dashboard.closeModal()" style="flex: 1;">
                    Close
                </button>
            </div>
        `;

        modal.style.display = 'block';
    }

    closeModal() {
        document.getElementById('job-modal').style.display = 'none';
    }

    toggleSaveJob(jobId) {
        if (this.savedJobs.has(jobId)) {
            this.savedJobs.delete(jobId);
        } else {
            this.savedJobs.add(jobId);
        }
        this.saveSavedJobs();
        this.filterJobs();
        this.updateStats();
    }

    updateStats() {
        document.getElementById('total-jobs').textContent = this.allJobs.length;
        document.getElementById('saved-jobs').textContent = this.savedJobs.size;
    }

    saveSavedJobs() {
        localStorage.setItem('savedJobs', JSON.stringify([...this.savedJobs]));
    }

    loadSavedJobs() {
        const saved = localStorage.getItem('savedJobs');
        if (saved) {
            this.savedJobs = new Set(JSON.parse(saved));
        }
    }

    clearFilters() {
        document.getElementById('search-input').value = '';
        document.getElementById('location-filter').value = 'all';
        document.getElementById('source-filter').value = 'all';
        document.getElementById('job-type-filter').value = 'all';
        this.filterJobs();
    }

    exportToCSV() {
        if (this.savedJobs.size === 0) {
            this.showToast('No saved jobs to export', 'error');
            return;
        }

        const savedJobsList = this.allJobs.filter(job => 
            this.savedJobs.has(this.getJobId(job))
        );

        // Prepare CSV
        const headers = ['Title', 'Company', 'Location', 'Job Type', 'Salary', 'Experience', 'Source', 'URL', 'Saved Date'];
        const rows = savedJobsList.map(job => [
            job.title,
            job.company,
            job.location,
            job.job_type,
            job.salary,
            job.experience,
            job.source,
            job.url,
            new Date().toISOString().split('T')[0]
        ]);

        // Create CSV content
        let csvContent = 'data:text/csv;charset=utf-8,' + 
            headers.join(',') + '\n' +
            rows.map(row => 
                row.map(cell => `"${String(cell ?? '').replace(/"/g, '""')}"`).join(',')
            ).join('\n');

        // Download
        const link = document.createElement('a');
        link.setAttribute('href', encodeURI(csvContent));
        link.setAttribute('download', `saved-jobs-${new Date().toISOString().split('T')[0]}.csv`);
        link.click();

        this.showToast(`Exported ${savedJobsList.length} jobs to CSV`, 'success');
    }

    showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        if (type === 'error') {
            toast.style.background = 'var(--danger-color)';
        }
        document.body.appendChild(toast);

        setTimeout(() => toast.remove(), 3000);
    }

    getJobId(job) {
        return `${job.company}-${job.title}-${job.source}`.toLowerCase().replace(/\s+/g, '-');
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize dashboard when DOM is ready
let dashboard;
document.addEventListener('DOMContentLoaded', () => {
    dashboard = new JobDashboard();
});
