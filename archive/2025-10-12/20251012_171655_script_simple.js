/**
 * SCRIPTUREMON - Real System UI
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
// UI UPDATE
// ============================================

function updateStatsBar(stats) {
    document.getElementById('totalAnalyses').textContent = stats.total_analyses;
    document.getElementById('runningCount').textContent = stats.running;
    document.getElementById('completedCount').textContent = stats.completed;
    document.getElementById('totalItems').textContent = stats.total_completed_items;
    document.getElementById('totalTime').textContent = `${Math.floor(stats.total_time_hours)}h`;
}

function renderAnalyses(analyses) {
    const container = document.getElementById('analysesList');

    if (analyses.length === 0) {
        container.innerHTML = '<p class="empty-msg">Nenhuma análise encontrada</p>';
        return;
    }

    container.innerHTML = analyses.map(analysis => `
        <div class="analysis-card ${analysis.status}">
            <div class="analysis-header">
                <h3 class="analysis-name">${analysis.screenplay_name}</h3>
                <span class="status-badge ${analysis.status}">${getStatusText(analysis.status)}</span>
            </div>

            <div class="progress-section">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${analysis.percentage}%"></div>
                </div>
                <span class="progress-text">${analysis.completed}/${analysis.total} (${analysis.percentage.toFixed(1)}%)</span>
            </div>

            <div class="analysis-info">
                <div class="info-row">
                    <span class="info-label">Atual:</span>
                    <span class="info-value">${analysis.current_specialist} / ${analysis.current_author}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Velocidade:</span>
                    <span class="info-value">${analysis.avg_minutes_per_analysis.toFixed(1)} min/análise</span>
                </div>
                <div class="info-row">
                    <span class="info-label">ETA:</span>
                    <span class="info-value">${formatHours(analysis.eta_hours)}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Modelo:</span>
                    <span class="info-value">${analysis.model}</span>
                </div>
            </div>

            <div class="analysis-actions">
                ${analysis.status === 'running' || analysis.status === 'paused' ?
                    `<button class="action-btn small" onclick="continueAnalysis('${analysis.id}')">
                        <span class="btn-icon">▶️</span>
                        <span class="btn-text">Continuar</span>
                    </button>` : ''}

                <button class="action-btn small secondary" onclick="openResults('${analysis.id}')">
                    <span class="btn-icon">📂</span>
                    <span class="btn-text">Resultados</span>
                </button>

                <button class="action-btn small secondary" onclick="openConsolidated('${analysis.id}')">
                    <span class="btn-icon">📊</span>
                    <span class="btn-text">Consolidados</span>
                </button>
            </div>
        </div>
    `).join('');
}

// ============================================
// REAL ACTIONS (Call API)
// ============================================

async function newAnalysis() {
    try {
        showStatus('Abrindo aplicativo Analyze Screenplay...', 'info');

        const response = await fetch(`${API_BASE}/action/new-analysis`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showStatus('Aplicativo aberto! Selecione o roteiro.', 'success');
        } else {
            showStatus(`Erro: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Erro ao abrir app: ${error.message}`, 'error');
    }
}

async function continueAnalysis(analysisId) {
    try {
        showStatus('Retomando análise...', 'info');

        const response = await fetch(`${API_BASE}/action/continue-analysis/${analysisId}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showStatus('Terminal aberto! Análise retomada.', 'success');
        } else {
            showStatus(`Erro: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Erro ao continuar: ${error.message}`, 'error');
    }
}

async function openResults(analysisId) {
    try {
        showStatus('Abrindo pasta de resultados...', 'info');

        const response = await fetch(`${API_BASE}/action/open-results/${analysisId}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showStatus('Pasta aberta no Finder!', 'success');
        } else {
            showStatus(`Erro: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Erro ao abrir: ${error.message}`, 'error');
    }
}

async function openConsolidated(analysisId) {
    try {
        showStatus('Abrindo consolidados...', 'info');

        const response = await fetch(`${API_BASE}/action/open-consolidated/${analysisId}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showStatus('Consolidados abertos!', 'success');
        } else {
            showStatus(`Erro: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Erro ao abrir: ${error.message}`, 'error');
    }
}

function refreshData() {
    showStatus('Atualizando dados...', 'info');
    fetchSystemStats();
    fetchAnalyses();
    setTimeout(() => {
        showStatus('Dados atualizados!', 'success');
    }, 500);
}

// ============================================
// HELPER FUNCTIONS
// ============================================

function getStatusText(status) {
    const statusMap = {
        'running': '🟢 Rodando',
        'paused': '🟡 Pausada',
        'completed': '✅ Completa'
    };
    return statusMap[status] || status;
}

function formatHours(hours) {
    const h = Math.floor(hours);
    const m = Math.floor((hours - h) * 60);
    return `${h}h ${m}m`;
}

function showStatus(message, type = 'info') {
    const statusEl = document.getElementById('statusMsg');
    statusEl.textContent = message;
    statusEl.className = `status-msg ${type}`;

    // Auto-hide after 3 seconds
    setTimeout(() => {
        statusEl.classList.add('hidden');
    }, 3000);
}

// ============================================
// INITIALIZATION
// ============================================

function init() {
    console.log('🎬 SCRIPTUREMON UI - Real System');

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
