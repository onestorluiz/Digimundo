/**
 * SCRIPTUREMON - Real System UI with Digimon World 3 Style
 * Connects to real API with functional buttons
 */

const API_BASE = 'http://localhost:8080/api';

// ============================================
// DATA FETCHING (REAL)
// ============================================

async function fetchSystemStats() {
    try {
        const response = await fetch(`${API_BASE}/system/stats`);
        const data = await response.json();

        if (data.success) {
            updateStatsBar(data.stats);
        }
    } catch (error) {
        console.error('Error fetching stats:', error);
    }
}

async function fetchAnalyses() {
    try {
        const response = await fetch(`${API_BASE}/analyses/list`);
        const data = await response.json();

        if (data.success) {
            renderAnalyses(data.analyses);
        }
    } catch (error) {
        console.error('Error fetching analyses:', error);
    }
}

// ============================================
// UI UPDATE (DIGIMON STYLE)
// ============================================

function updateStatsBar(stats) {
    document.getElementById('totalAnalyses').textContent = stats.total_analyses;
    document.getElementById('runningCount').textContent = stats.running;
    document.getElementById('totalItems').textContent = stats.total_completed_items;
    document.getElementById('totalTime').textContent = `${Math.floor(stats.total_time_hours)}h`;
}

function renderAnalyses(analyses) {
    const container = document.getElementById('analysesContainer');

    if (analyses.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📄</div>
                <div class="empty-text">No analyses running</div>
                <div class="empty-hint">Click "New Screenplay" to start</div>
            </div>
        `;
        return;
    }

    container.innerHTML = analyses.map(analysis => `
        <div class="analysis-card-digi ${analysis.status}">
            <!-- Progress Bar -->
            <div class="progress-section-digi">
                <div class="progress-label-digi">${analysis.screenplay_name}</div>
                <div class="progress-bar-container-digi">
                    <div class="progress-bar-fill-digi" style="width: ${analysis.percentage}%"></div>
                    <div class="progress-text-digi">${analysis.completed}/${analysis.total} (${analysis.percentage.toFixed(1)}%)</div>
                </div>
            </div>

            <!-- Current Status -->
            <div class="status-section-digi">
                <div class="status-row-digi">
                    <span class="status-icon-digi">🔬</span>
                    <span class="status-label-digi">Current:</span>
                    <span class="status-value-digi">${analysis.current_specialist} / ${analysis.current_author}</span>
                </div>
                <div class="status-row-digi">
                    <span class="status-icon-digi">⚡</span>
                    <span class="status-label-digi">Speed:</span>
                    <span class="status-value-digi">${analysis.avg_minutes_per_analysis.toFixed(1)} min/analysis</span>
                </div>
                <div class="status-row-digi">
                    <span class="status-icon-digi">🎯</span>
                    <span class="status-label-digi">ETA:</span>
                    <span class="status-value-digi">${formatHours(analysis.eta_hours)}</span>
                </div>
                <div class="status-row-digi">
                    <span class="status-icon-digi">🤖</span>
                    <span class="status-label-digi">Model:</span>
                    <span class="status-value-digi">${analysis.model}</span>
                </div>
            </div>

            <!-- Action Buttons -->
            <div class="actions-section-digi">
                ${analysis.status === 'running' || analysis.status === 'paused' ?
                    `<div class="action-btn-digi" onclick="continueAnalysis('${analysis.id}')">
                        <span class="icon">▶️</span>
                        <span class="text">Continue</span>
                    </div>` : ''}

                <div class="action-btn-digi" onclick="openResults('${analysis.id}')">
                    <span class="icon">📂</span>
                    <span class="text">Results</span>
                </div>

                <div class="action-btn-digi" onclick="openConsolidated('${analysis.id}')">
                    <span class="icon">📊</span>
                    <span class="text">Consolidated</span>
                </div>
            </div>
        </div>
    `).join('');
}

// ============================================
// REAL ACTIONS (Call API)
// ============================================

async function newAnalysis() {
    try {
        showStatus('Opening Analyze Screenplay app...', 'info');

        const response = await fetch(`${API_BASE}/action/new-analysis`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showStatus('App opened! Select your screenplay.', 'success');
        } else {
            showStatus(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

async function continueAnalysis(analysisId) {
    try {
        showStatus('Resuming analysis...', 'info');

        const response = await fetch(`${API_BASE}/action/continue-analysis/${analysisId}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showStatus('Terminal opened! Analysis resumed.', 'success');
        } else {
            showStatus(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

async function openResults(analysisId) {
    try {
        showStatus('Opening results folder...', 'info');

        const response = await fetch(`${API_BASE}/action/open-results/${analysisId}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showStatus('Folder opened in Finder!', 'success');
        } else {
            showStatus(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

async function openConsolidated(analysisId) {
    try {
        showStatus('Opening consolidated reports...', 'info');

        const response = await fetch(`${API_BASE}/action/open-consolidated/${analysisId}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showStatus('Consolidated reports opened!', 'success');
        } else {
            showStatus(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

function refreshData() {
    showStatus('Refreshing data...', 'info');
    fetchSystemStats();
    fetchAnalyses();
    setTimeout(() => {
        showStatus('Data refreshed!', 'success');
    }, 500);
}

// ============================================
// HELPER FUNCTIONS
// ============================================

function formatHours(hours) {
    const h = Math.floor(hours);
    const m = Math.floor((hours - h) * 60);
    return `${h}h ${m}m`;
}

function showStatus(message, type = 'info') {
    const statusEl = document.getElementById('statusMsg');
    statusEl.textContent = message;
    statusEl.className = `status-toast ${type}`;

    // Auto-hide after 3 seconds
    setTimeout(() => {
        statusEl.classList.add('hidden');
    }, 3000);
}

// ============================================
// INITIALIZATION
// ============================================

function init() {
    console.log('🎬 SCRIPTUREMON - Digimon World 3 Style Dashboard');

    // Initial load
    fetchSystemStats();
    fetchAnalyses();

    // Auto-refresh every 5 seconds
    setInterval(() => {
        fetchSystemStats();
        fetchAnalyses();
    }, 5000);
}

// Start when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
