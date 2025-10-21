/**
 * SCRIPTUREMON v11.0 - Complete Web Dashboard
 * Digimon World 3 PS2 Style with Full App Functionality
 */

const API_BASE = 'http://localhost:8080/api';

// ============================================================================
// STATE MANAGEMENT
// ============================================================================

const appState = {
    currentScreen: 'mainMenu',
    selectedScreenplay: null,
    selectedModel: 'ollama',
    screenplays: [],
    analyses: [],
    specialists: [],
    systemConfig: {},
    refreshInterval: null
};

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🎬 SCRIPTUREMON v11.0 - Initializing...');

    // Load initial data
    await loadAllData();

    // Setup auto-refresh for monitoring screen
    setupAutoRefresh();

    // Setup event listeners
    setupEventListeners();

    console.log('✅ System ready!');
});

async function loadAllData() {
    await Promise.all([
        fetchSystemStats(),
        fetchScreenplays(),
        fetchSpecialists(),
        fetchSystemConfig()
    ]);
}

// ============================================================================
// NAVIGATION
// ============================================================================

function navigateTo(screenId) {
    console.log(`Navigating to: ${screenId}`);

    // Hide all screens
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.add('hidden');
    });

    // Show target screen
    const targetScreen = document.getElementById(screenId);
    if (targetScreen) {
        targetScreen.classList.remove('hidden');
        appState.currentScreen = screenId;

        // Load screen-specific data
        onScreenEnter(screenId);
    }
}

function onScreenEnter(screenId) {
    switch(screenId) {
        case 'mainMenu':
            fetchSystemStats();
            break;
        case 'screenplaySelect':
            loadScreenplaySelect();
            break;
        case 'monitoring':
            startMonitoring();
            break;
        case 'specialistView':
            loadSpecialistView();
            break;
        case 'settings':
            loadSettings();
            break;
    }
}

// ============================================================================
// API CALLS
// ============================================================================

async function fetchSystemStats() {
    try {
        const response = await fetch(`${API_BASE}/system/stats`);
        const data = await response.json();

        if (data.success) {
            updateAllStatsDisplays(data.stats);
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
            appState.analyses = data.analyses;
            if (appState.currentScreen === 'monitoring') {
                renderAnalyses(data.analyses);
            }
        }
    } catch (error) {
        console.error('Error fetching analyses:', error);
    }
}

async function fetchScreenplays() {
    try {
        const response = await fetch(`${API_BASE}/screenplays/list`);
        const data = await response.json();

        if (data.success) {
            appState.screenplays = data.screenplays;
        }
    } catch (error) {
        console.error('Error fetching screenplays:', error);
    }
}

async function fetchSpecialists() {
    try {
        const response = await fetch(`${API_BASE}/specialists/list`);
        const data = await response.json();

        if (data.success) {
            appState.specialists = data.specialists;
        }
    } catch (error) {
        console.error('Error fetching specialists:', error);
    }
}

async function fetchSystemConfig() {
    try {
        const response = await fetch(`${API_BASE}/system/config`);
        const data = await response.json();

        if (data.success) {
            appState.systemConfig = data.config;
        }
    } catch (error) {
        console.error('Error fetching system config:', error);
    }
}

// ============================================================================
// STATS UPDATE
// ============================================================================

function updateAllStatsDisplays(stats) {
    // Main menu stats
    safeSetText('menuTotalAnalyses', stats.total_analyses);
    safeSetText('menuRunningCount', stats.running);
    safeSetText('menuTotalItems', stats.total_completed_items);
    safeSetText('menuTotalTime', `${Math.floor(stats.total_time_hours)}h`);

    // Monitoring screen stats
    safeSetText('totalAnalyses', stats.total_analyses);
    safeSetText('runningCount', stats.running);
    safeSetText('totalItems', stats.total_completed_items);
    safeSetText('totalTime', `${Math.floor(stats.total_time_hours)}h`);
}

function safeSetText(id, text) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = text;
    }
}

// ============================================================================
// SCREENPLAY SELECTION SCREEN
// ============================================================================

function loadScreenplaySelect() {
    const container = document.getElementById('screenplayListContainer');

    if (appState.screenplays.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📄</div>
                <div class="empty-text">No screenplays found</div>
                <div class="empty-hint">Add PDF files to the inputs directory</div>
            </div>
        `;
        return;
    }

    container.innerHTML = appState.screenplays.map((screenplay, index) => `
        <div class="screenplay-item ${index === 0 ? 'selected' : ''}"
             data-path="${screenplay.path}"
             onclick="selectScreenplay('${screenplay.path}')">
            <span class="screenplay-icon">📄</span>
            <div class="screenplay-info">
                <div class="screenplay-name">${screenplay.name}</div>
                <div class="screenplay-meta">${screenplay.size} • ${new Date(screenplay.modified).toLocaleDateString()}</div>
            </div>
            <span class="screenplay-check">✓</span>
        </div>
    `).join('');

    // Select first screenplay by default
    if (appState.screenplays.length > 0) {
        appState.selectedScreenplay = appState.screenplays[0].path;
    }
}

function selectScreenplay(path) {
    appState.selectedScreenplay = path;

    // Update UI
    document.querySelectorAll('.screenplay-item').forEach(item => {
        item.classList.remove('selected');
        if (item.dataset.path === path) {
            item.classList.add('selected');
        }
    });
}

// ============================================================================
// MODEL SELECTION
// ============================================================================

function setupEventListeners() {
    // Model selection
    document.querySelectorAll('.model-option').forEach(option => {
        option.addEventListener('click', function() {
            const model = this.dataset.model;
            selectModel(model);
        });
    });
}

function selectModel(model) {
    appState.selectedModel = model;

    // Update UI
    document.querySelectorAll('.model-option').forEach(option => {
        option.classList.remove('selected');
        if (option.dataset.model === model) {
            option.classList.add('selected');
        }
    });
}

// ============================================================================
// START NEW ANALYSIS
// ============================================================================

async function startNewAnalysis() {
    if (!appState.selectedScreenplay) {
        showStatus('Please select a screenplay first', 'error');
        return;
    }

    showStatus('Starting analysis...', 'info');

    try {
        const response = await fetch(`${API_BASE}/action/start-analysis`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                screenplay_path: appState.selectedScreenplay,
                model: appState.selectedModel
            })
        });

        const data = await response.json();

        if (data.success) {
            showStatus(data.message, 'success');

            // Navigate to monitoring after 2 seconds
            setTimeout(() => {
                navigateTo('monitoring');
            }, 2000);
        } else {
            showStatus(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// ============================================================================
// MONITORING SCREEN
// ============================================================================

function startMonitoring() {
    // Initial load
    fetchAnalyses();
    fetchSystemStats();

    // Auto-refresh every 5 seconds
    if (appState.refreshInterval) {
        clearInterval(appState.refreshInterval);
    }

    appState.refreshInterval = setInterval(() => {
        if (appState.currentScreen === 'monitoring') {
            fetchAnalyses();
            fetchSystemStats();
        }
    }, 5000);
}

function setupAutoRefresh() {
    // This is called on init, monitoring screen manages its own refresh
}

function renderAnalyses(analyses) {
    const container = document.getElementById('analysesContainer');

    if (analyses.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📄</div>
                <div class="empty-text">No analyses running</div>
                <div class="empty-hint">Start a new analysis from the main menu</div>
            </div>
        `;
        return;
    }

    container.innerHTML = analyses.map(analysis => `
        <div class="analysis-card-digi ${analysis.status}">
            <!-- Progress Bar -->
            <div class="progress-section-digi">
                <div class="progress-label-digi">${escapeHtml(analysis.screenplay_name)}</div>
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
                    <span class="status-value-digi">${escapeHtml(analysis.current_specialist)} / ${escapeHtml(analysis.current_author)}</span>
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
                    <span class="status-value-digi">${escapeHtml(analysis.model)}</span>
                </div>
            </div>

            <!-- Action Buttons -->
            <div class="actions-section-digi">
                ${analysis.status === 'running' || analysis.status === 'paused' ?
                    `<div class="action-btn-digi" onclick="continueAnalysis('${analysis.id}')">
                        <span class="icon">▶️</span>
                        <span class="text">Continue</span>
                    </div>` : ''
                }
                <div class="action-btn-digi" onclick="openResults('${analysis.id}')">
                    <span class="icon">📊</span>
                    <span class="text">Results</span>
                </div>
                <div class="action-btn-digi" onclick="openConsolidated('${analysis.id}')">
                    <span class="icon">📄</span>
                    <span class="text">Reports</span>
                </div>
            </div>
        </div>
    `).join('');
}

// ============================================================================
// ANALYSIS ACTIONS
// ============================================================================

async function continueAnalysis(analysisId) {
    showStatus('Resuming analysis...', 'info');

    try {
        const response = await fetch(`${API_BASE}/action/continue-analysis/${analysisId}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showStatus(data.message, 'success');
        } else {
            showStatus(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

async function openResults(analysisId) {
    showStatus('Opening results folder...', 'info');

    try {
        const response = await fetch(`${API_BASE}/action/open-results/${analysisId}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showStatus(data.message, 'success');
        } else {
            showStatus(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

async function openConsolidated(analysisId) {
    showStatus('Opening consolidated reports...', 'info');

    try {
        const response = await fetch(`${API_BASE}/action/open-consolidated/${analysisId}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showStatus(data.message, 'success');
        } else {
            showStatus(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// ============================================================================
// SPECIALIST VIEW SCREEN
// ============================================================================

function loadSpecialistView() {
    const container = document.getElementById('specialistGridContainer');

    if (appState.specialists.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">🔬</div>
                <div class="empty-text">Loading specialists...</div>
            </div>
        `;
        return;
    }

    container.innerHTML = appState.specialists.map((specialist, index) => `
        <div class="specialist-card ${index === 0 ? 'selected' : ''}"
             onclick="selectSpecialist('${specialist.id}')">
            <div class="specialist-icon-large">${specialist.icon}</div>
            <div class="specialist-name">${specialist.name}</div>
            <div class="specialist-level">Lv ${specialist.authors}</div>
        </div>
    `).join('');

    // Show first specialist info
    if (appState.specialists.length > 0) {
        selectSpecialist(appState.specialists[0].id);
    }
}

function selectSpecialist(specialistId) {
    const specialist = appState.specialists.find(s => s.id === specialistId);
    if (!specialist) return;

    // Update selected state
    document.querySelectorAll('.specialist-card').forEach(card => {
        card.classList.remove('selected');
    });
    event.currentTarget?.classList.add('selected');

    // Show specialist info
    const infoContainer = document.getElementById('specialistInfoContainer');
    infoContainer.innerHTML = `
        <div class="specialist-detail">
            <div class="specialist-portrait">${specialist.icon}</div>
            <div class="specialist-title">${specialist.name}</div>
            <div class="specialist-type">${specialist.type}</div>

            <div class="specialist-stats-detail">
                <div class="stat-row">
                    <span class="stat-name">Authors:</span>
                    <span class="stat-value">${specialist.authors}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-name">Total Analyses:</span>
                    <span class="stat-value">${specialist.authors} per screenplay</span>
                </div>
            </div>

            <div class="specialist-desc">
                Analyzes ${specialist.type.toLowerCase()} using ${specialist.authors} different theoretical frameworks.
            </div>
        </div>
    `;
}

// ============================================================================
// SETTINGS SCREEN
// ============================================================================

function loadSettings() {
    // System status
    const statusContainer = document.getElementById('systemStatusContainer');
    statusContainer.innerHTML = `
        <div class="settings-item">
            <span class="settings-icon">${appState.systemConfig.ollama_running ? '✅' : '❌'}</span>
            <span class="settings-label">Ollama Status</span>
            <span class="settings-value">${appState.systemConfig.ollama_running ? 'Running' : 'Not Running'}</span>
        </div>
        <div class="settings-item">
            <span class="settings-icon">${appState.systemConfig.has_api_key ? '✅' : '❌'}</span>
            <span class="settings-label">OpenAI API Key</span>
            <span class="settings-value">${appState.systemConfig.has_api_key ? 'Configured' : 'Not Configured'}</span>
        </div>
        <div class="settings-item">
            <span class="settings-icon">📊</span>
            <span class="settings-label">Total Analyses</span>
            <span class="settings-value">${appState.analyses.length}</span>
        </div>
        <div class="settings-item">
            <span class="settings-icon">📄</span>
            <span class="settings-label">Screenplays Available</span>
            <span class="settings-value">${appState.screenplays.length}</span>
        </div>
    `;

    // System paths
    const pathsContainer = document.getElementById('systemPathsContainer');
    pathsContainer.innerHTML = `
        <div class="settings-item">
            <span class="settings-icon">📁</span>
            <span class="settings-label">Scripturemon Dir</span>
            <span class="settings-value small">${appState.systemConfig.scripturemon_dir || 'N/A'}</span>
        </div>
        <div class="settings-item">
            <span class="settings-icon">📂</span>
            <span class="settings-label">Workspace Dir</span>
            <span class="settings-value small">${appState.systemConfig.workspace_dir || 'N/A'}</span>
        </div>
    `;
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function formatHours(hours) {
    if (hours < 1) {
        return `${Math.round(hours * 60)} min`;
    } else if (hours < 24) {
        return `${hours.toFixed(1)}h`;
    } else {
        return `${Math.floor(hours / 24)}d ${Math.round(hours % 24)}h`;
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
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

function refreshData() {
    showStatus('Refreshing data...', 'info');
    loadAllData();
}

// ============================================================================
// LEGACY FUNCTION (for compatibility)
// ============================================================================

function newAnalysis() {
    navigateTo('screenplaySelect');
}

console.log('🎬 SCRIPTUREMON v11.0 - Script loaded successfully!');
