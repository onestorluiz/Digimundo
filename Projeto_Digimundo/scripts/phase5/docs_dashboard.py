#!/usr/bin/env python3
"""
📊 REAL-TIME DOCUMENTATION HEALTH DASHBOARD

Nível: ALÉM DO ALÉM DO VALE DO SILÍCIO

Este sistema:
1. Serve dashboard web em tempo real
2. Mostra status de validação atualizado a cada 30s
3. Exibe métricas, drift predictions, e histórico
4. API REST para integração
5. Auto-refresh sem reload

Usage:
    python3 scripts/phase5/docs_dashboard.py
    python3 scripts/phase5/docs_dashboard.py --port 8080
    python3 scripts/phase5/docs_dashboard.py --no-browser

Access: http://localhost:3000
"""

import subprocess
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from flask import Flask, render_template_string, jsonify
import webbrowser
import threading
import time

app = Flask(__name__)

# HTML Template
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>📊 Documentation Health Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        h1 {
            font-size: 2.5em;
            color: #667eea;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #666;
            font-size: 1.1em;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .card:hover {
            transform: translateY(-5px);
        }
        .card h2 {
            font-size: 1.3em;
            color: #667eea;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .metric {
            font-size: 3em;
            font-weight: bold;
            margin: 15px 0;
        }
        .metric.green { color: #10b981; }
        .metric.yellow { color: #f59e0b; }
        .metric.red { color: #ef4444; }
        .status {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9em;
        }
        .status.healthy {
            background: #d1fae5;
            color: #065f46;
        }
        .status.warning {
            background: #fef3c7;
            color: #92400e;
        }
        .status.critical {
            background: #fee2e2;
            color: #991b1b;
        }
        .progress-bar {
            width: 100%;
            height: 30px;
            background: #e5e7eb;
            border-radius: 15px;
            overflow: hidden;
            margin: 15px 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #10b981, #34d399);
            transition: width 0.5s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        .metric-row {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #e5e7eb;
        }
        .metric-row:last-child {
            border-bottom: none;
        }
        .metric-label {
            color: #666;
        }
        .metric-value {
            font-weight: 600;
            color: #333;
        }
        .timestamp {
            text-align: center;
            color: #666;
            margin-top: 20px;
            font-size: 0.9em;
        }
        .refresh-indicator {
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            padding: 10px 20px;
            border-radius: 25px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .spinner {
            width: 20px;
            height: 20px;
            border: 3px solid #e5e7eb;
            border-top-color: #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .recommendations {
            background: #fef3c7;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #f59e0b;
        }
        .recommendations h3 {
            color: #92400e;
            margin-bottom: 10px;
        }
        .recommendations ul {
            list-style: none;
        }
        .recommendations li {
            padding: 8px 0;
            color: #78350f;
        }
        .recommendations li:before {
            content: "→ ";
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Documentation Health Dashboard</h1>
            <p class="subtitle">Real-time monitoring of documentation quality and metrics</p>
        </header>

        <div class="grid">
            <div class="card">
                <h2>🎯 Overall Health</h2>
                <div class="metric" id="health-score">--</div>
                <div class="status" id="health-status">Loading...</div>
                <div class="progress-bar">
                    <div class="progress-fill" id="health-progress" style="width: 0%">0%</div>
                </div>
            </div>

            <div class="card">
                <h2>🔮 Drift Prediction</h2>
                <div class="metric" id="drift-prob">--</div>
                <div class="status" id="drift-status">Loading...</div>
                <p style="margin-top: 15px; color: #666;">
                    Estimated drift in: <strong id="drift-days">--</strong> days
                </p>
            </div>

            <div class="card">
                <h2>⏱️ Last Validation</h2>
                <div class="metric" id="last-validation">--</div>
                <p style="color: #666; margin-top: 10px;">
                    Next check in: <strong id="next-check">30s</strong>
                </p>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h2>📈 Metrics</h2>
                <div class="metric-row">
                    <span class="metric-label">Duplications</span>
                    <span class="metric-value" id="duplications">--</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Dead Files</span>
                    <span class="metric-value" id="dead-files">--</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Dead Code %</span>
                    <span class="metric-value" id="dead-pct">--</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">ORM Consistency</span>
                    <span class="metric-value" id="orm-pct">--</span>
                </div>
            </div>

            <div class="card" style="grid-column: span 2;">
                <h2>💡 Recommendations</h2>
                <div class="recommendations" id="recommendations">
                    <p>Loading recommendations...</p>
                </div>
            </div>
        </div>

        <div class="timestamp">
            Last updated: <strong id="timestamp">--</strong>
        </div>
    </div>

    <div class="refresh-indicator">
        <div class="spinner"></div>
        <span>Auto-refreshing...</span>
    </div>

    <script>
        let countdown = 30;

        async function fetchData() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();

                // Update health
                document.getElementById('health-score').textContent = data.health_score + '%';
                document.getElementById('health-progress').style.width = data.health_score + '%';
                document.getElementById('health-progress').textContent = data.health_score + '%';

                const healthStatus = document.getElementById('health-status');
                healthStatus.textContent = data.health_status;
                healthStatus.className = 'status ' + data.health_class;

                // Update drift prediction
                document.getElementById('drift-prob').textContent = data.drift_probability + '%';
                document.getElementById('drift-days').textContent = data.drift_days;

                const driftStatus = document.getElementById('drift-status');
                driftStatus.textContent = data.drift_urgency;
                driftStatus.className = 'status ' + data.drift_class;

                // Update metrics
                document.getElementById('duplications').textContent = data.metrics.duplications.toLocaleString();
                document.getElementById('dead-files').textContent = data.metrics.dead_files;
                document.getElementById('dead-pct').textContent = data.metrics.dead_percentage + '%';
                document.getElementById('orm-pct').textContent = data.metrics.orm_percentage + '%';

                // Update last validation
                document.getElementById('last-validation').textContent = data.last_validation;
                document.getElementById('timestamp').textContent = data.timestamp;

                // Update recommendations
                const recDiv = document.getElementById('recommendations');
                if (data.recommendations.length > 0) {
                    recDiv.innerHTML = '<h3>Recommended Actions</h3><ul>' +
                        data.recommendations.map(r => '<li>' + r + '</li>').join('') +
                        '</ul>';
                } else {
                    recDiv.innerHTML = '<p>✅ All systems healthy - no actions needed!</p>';
                }

            } catch (error) {
                console.error('Failed to fetch data:', error);
            }
        }

        function updateCountdown() {
            countdown--;
            if (countdown <= 0) {
                countdown = 30;
                fetchData();
            }
            document.getElementById('next-check').textContent = countdown + 's';
        }

        // Initial fetch
        fetchData();

        // Auto-refresh every 30 seconds
        setInterval(fetchData, 30000);

        // Update countdown every second
        setInterval(updateCountdown, 1000);
    </script>
</body>
</html>
"""


class DashboardServer:
    """Documentation health dashboard server"""

    def __init__(self, port: int = 3000):
        self.port = port
        self.project_root = self._detect_project_root()
        self.docs_dir = self.project_root.parent / 'docs' / 'fase_5'

    def _detect_project_root(self) -> Path:
        """Auto-detect project root"""
        current = Path.cwd()

        if (current / 'app').exists() and (current / 'tests').exists():
            return current

        if (current / 'cineprod-flask').exists():
            return current / 'cineprod-flask'

        if current.name == 'scripts':
            parent = current.parent.parent
            if (parent / 'cineprod-flask').exists():
                return parent / 'cineprod-flask'

        return current

    def get_latest_validation(self) -> Dict:
        """Get latest validation report"""
        reports = sorted(self.docs_dir.glob('VALIDATION_REPORT_*.md'), reverse=True)

        if not reports:
            return None

        report_path = reports[0]
        content = report_path.read_text()

        # Parse report
        metrics = {}

        dup_match = re.search(r'Duplications\s*\|\s*(\d+)', content)
        if dup_match:
            metrics['duplications'] = int(dup_match.group(1))

        dead_match = re.search(r'Dead Files\s*\|\s*(\d+)\s*\(([\d.]+)%\)', content)
        if dead_match:
            metrics['dead_files'] = int(dead_match.group(1))
            metrics['dead_percentage'] = float(dead_match.group(2))

        orm_match = re.search(r'ORM Consistency\s*\|\s*([\d.]+)%', content)
        if orm_match:
            metrics['orm_percentage'] = float(orm_match.group(1))

        # Get timestamp from filename
        timestamp_str = report_path.stem.replace('VALIDATION_REPORT_', '')
        timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')

        return {
            'metrics': metrics,
            'timestamp': timestamp,
            'passed': 'PASSED' in content
        }

    def get_latest_prediction(self) -> Dict:
        """Get latest drift prediction"""
        predictions = sorted(self.docs_dir.glob('DRIFT_PREDICTION_*.json'), reverse=True)

        if not predictions:
            return None

        prediction_path = predictions[0]
        return json.loads(prediction_path.read_text())

    def get_status(self) -> Dict:
        """Get current dashboard status"""
        validation = self.get_latest_validation()
        prediction = self.get_latest_prediction()

        if not validation:
            return {
                'health_score': 0,
                'health_status': 'Unknown',
                'health_class': 'critical',
                'drift_probability': 0,
                'drift_days': '?',
                'drift_urgency': 'Unknown',
                'drift_class': 'warning',
                'metrics': {
                    'duplications': 0,
                    'dead_files': 0,
                    'dead_percentage': 0,
                    'orm_percentage': 0
                },
                'last_validation': 'Never',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'recommendations': ['Run validation: python3 scripts/phase5/validate_documentation.py']
            }

        # Calculate health score
        health_score = 100.0 if validation['passed'] else 50.0

        # Time since last validation
        time_since = datetime.now() - validation['timestamp']
        hours_since = time_since.total_seconds() / 3600

        if hours_since > 24:
            health_score -= 20
        elif hours_since > 12:
            health_score -= 10

        health_score = max(0, min(100, health_score))

        # Health status
        if health_score >= 90:
            health_status = 'Healthy'
            health_class = 'healthy'
        elif health_score >= 70:
            health_status = 'Warning'
            health_class = 'warning'
        else:
            health_status = 'Critical'
            health_class = 'critical'

        # Drift info
        if prediction:
            drift_prob = prediction['prediction']['probability']
            drift_days = prediction['prediction']['estimated_days']
            drift_urgency = prediction['prediction']['urgency']
            recommendations = prediction['prediction']['recommendations']

            if drift_urgency == 'HIGH':
                drift_class = 'critical'
            elif drift_urgency == 'MEDIUM':
                drift_class = 'warning'
            else:
                drift_class = 'healthy'
        else:
            drift_prob = 0
            drift_days = '?'
            drift_urgency = 'Unknown'
            drift_class = 'warning'
            recommendations = []

        # Last validation time
        last_val_time = validation['timestamp'].strftime('%H:%M:%S')

        return {
            'health_score': int(health_score),
            'health_status': health_status,
            'health_class': health_class,
            'drift_probability': int(drift_prob),
            'drift_days': drift_days,
            'drift_urgency': drift_urgency,
            'drift_class': drift_class,
            'metrics': validation['metrics'],
            'last_validation': last_val_time,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'recommendations': recommendations
        }


# Global dashboard instance
dashboard = None


@app.route('/')
def index():
    """Serve dashboard HTML"""
    return render_template_string(DASHBOARD_HTML)


@app.route('/api/status')
def api_status():
    """API endpoint for status"""
    return jsonify(dashboard.get_status())


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Documentation health dashboard')
    parser.add_argument('--port', type=int, default=3000, help='Port to run on')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser')

    args = parser.parse_args()

    global dashboard
    dashboard = DashboardServer(port=args.port)

    # Open browser after 1 second
    if not args.no_browser:
        def open_browser():
            time.sleep(1)
            webbrowser.open(f'http://localhost:{args.port}')

        threading.Thread(target=open_browser, daemon=True).start()

    print(f"🚀 Dashboard running at: http://localhost:{args.port}")
    print(f"📊 Auto-refreshes every 30 seconds")
    print(f"Press Ctrl+C to stop")

    app.run(host='0.0.0.0', port=args.port, debug=False)


if __name__ == '__main__':
    main()
