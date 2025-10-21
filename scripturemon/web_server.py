#!/usr/bin/env python3
"""
🎬 SCRIPTUREMON - WEB SERVER (Real Actions)
Serves UI with REAL system actions and data
"""

from flask import Flask, jsonify, send_from_directory, Response, request
from flask_cors import CORS
import json
import os
import subprocess
from pathlib import Path
from datetime import datetime
import time

app = Flask(__name__)
CORS(app)

# Configuration
SCRIPTUREMON_DIR = Path(__file__).parent
WORKSPACE_DIR = SCRIPTUREMON_DIR / "workspace" / "outputs"
UI_DIR = SCRIPTUREMON_DIR / "ui_design" / "digimon_style"
APP_PATH = "/Applications/Analyze Screenplay.app/Contents/MacOS/run"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def find_all_checkpoints():
    """Find all checkpoint files with REAL data"""
    checkpoints = []

    if not WORKSPACE_DIR.exists():
        return checkpoints

    for checkpoint_path in WORKSPACE_DIR.glob("*/2_logs/checkpoint.json"):
        try:
            with open(checkpoint_path, 'r') as f:
                data = json.load(f)

            analysis_dir = checkpoint_path.parent.parent
            analysis_id = analysis_dir.name

            completed = len(data.get('completed', []))
            total = data.get('total_analyses', 312)
            percentage = (completed / total * 100) if total > 0 else 0

            started_at = datetime.fromisoformat(data['started_at'])
            last_update_str = data.get('last_update', data['started_at'])
            last_update = datetime.fromisoformat(last_update_str)

            duration_seconds = (last_update - started_at).total_seconds()
            duration_hours = duration_seconds / 3600

            avg_seconds_per_analysis = (duration_seconds / completed) if completed > 0 else 0
            avg_minutes_per_analysis = avg_seconds_per_analysis / 60

            remaining = total - completed
            eta_seconds = remaining * avg_seconds_per_analysis
            eta_hours = eta_seconds / 3600

            # Determine status
            time_since_update = (datetime.now() - last_update).total_seconds()
            if percentage >= 100:
                status = "completed"
            elif time_since_update < 600:  # 10 minutes (analyses take ~5-7 min each)
                status = "running"
            else:
                status = "paused"

            # Extract screenplay name
            screenplay_name = analysis_id.replace("_all_specialists_", " ").replace("_", " ")

            # Determine model from ID or log
            model = "scripturemon-optimized"  # Default Ollama
            if "gpt" in analysis_id.lower():
                model = "gpt-5"

            checkpoints.append({
                'id': analysis_id,
                'screenplay_name': screenplay_name,
                'completed': completed,
                'total': total,
                'percentage': percentage,
                'started_at': started_at.isoformat(),
                'last_update': last_update.isoformat(),
                'duration_hours': duration_hours,
                'avg_minutes_per_analysis': avg_minutes_per_analysis,
                'eta_hours': eta_hours,
                'status': status,
                'current_specialist': data.get('current_specialist', ''),
                'current_author': data.get('current_author', ''),
                'failed': len(data.get('failed', [])),
                'model': model
            })
        except Exception as e:
            print(f"Error reading checkpoint {checkpoint_path}: {e}")
            continue

    # Sort by last_update (most recent first)
    checkpoints.sort(key=lambda x: x['last_update'], reverse=True)

    return checkpoints

def count_html_results(analysis_id):
    """Count REAL HTML files generated"""
    results_dir = WORKSPACE_DIR / analysis_id / "1_individuais"

    if not results_dir.exists():
        return 0

    html_files = list(results_dir.rglob("*.html"))
    return len(html_files)

def get_system_stats():
    """Get REAL system statistics"""
    checkpoints = find_all_checkpoints()

    total_analyses = len(checkpoints)
    running_analyses = sum(1 for c in checkpoints if c['status'] == 'running')
    completed_analyses = sum(1 for c in checkpoints if c['status'] == 'completed')
    paused_analyses = sum(1 for c in checkpoints if c['status'] == 'paused')

    total_completed_items = sum(c['completed'] for c in checkpoints)
    total_time_hours = sum(c['duration_hours'] for c in checkpoints)

    # Count REAL HTML files
    total_html_files = sum(count_html_results(c['id']) for c in checkpoints)

    return {
        'total_analyses': total_analyses,
        'running': running_analyses,
        'completed': completed_analyses,
        'paused': paused_analyses,
        'total_completed_items': total_completed_items,
        'total_time_hours': total_time_hours,
        'total_html_files': total_html_files
    }

# ============================================================================
# API ENDPOINTS - REAL DATA
# ============================================================================

@app.route('/')
def index():
    """Serve the main UI"""
    return send_from_directory(UI_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory(UI_DIR, path)

@app.route('/api/analyses/list')
def api_list_analyses():
    """List all REAL analyses from checkpoints"""
    checkpoints = find_all_checkpoints()
    return jsonify({
        'success': True,
        'analyses': checkpoints,
        'count': len(checkpoints)
    })

@app.route('/api/system/stats')
def api_system_stats():
    """Get REAL system statistics"""
    stats = get_system_stats()
    return jsonify({
        'success': True,
        'stats': stats
    })

@app.route('/api/analysis/<analysis_id>')
def api_get_analysis(analysis_id):
    """Get specific REAL analysis details"""
    checkpoints = find_all_checkpoints()

    analysis = next((c for c in checkpoints if c['id'] == analysis_id), None)

    if not analysis:
        return jsonify({
            'success': False,
            'error': 'Analysis not found'
        }), 404

    # Add HTML count
    analysis['html_count'] = count_html_results(analysis_id)

    return jsonify({
        'success': True,
        'analysis': analysis
    })

# ============================================================================
# API ENDPOINTS - REAL ACTIONS
# ============================================================================

@app.route('/api/action/new-analysis', methods=['POST'])
def api_new_analysis():
    """Launch REAL new analysis via macOS app"""
    try:
        # Open the real macOS app
        subprocess.Popen(['open', '-a', 'Analyze Screenplay'])

        return jsonify({
            'success': True,
            'message': 'Analyze Screenplay app launched'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/action/continue-analysis/<analysis_id>', methods=['POST'])
def api_continue_analysis(analysis_id):
    """Continue REAL analysis from checkpoint"""
    try:
        checkpoint_path = WORKSPACE_DIR / analysis_id / "2_logs" / "checkpoint.json"

        if not checkpoint_path.exists():
            return jsonify({
                'success': False,
                'error': 'Checkpoint not found'
            }), 404

        # Open Terminal and run continue command
        # This uses the real analyze_all_specialists.py with --resume
        cmd = f'''
tell application "Terminal"
    do script "cd {SCRIPTUREMON_DIR} && python3 analyze_all_specialists.py --resume"
    activate
end tell
'''
        subprocess.run(['osascript', '-e', cmd])

        return jsonify({
            'success': True,
            'message': f'Resuming analysis {analysis_id}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/action/open-results/<analysis_id>', methods=['POST'])
def api_open_results(analysis_id):
    """Open REAL results folder"""
    try:
        results_dir = WORKSPACE_DIR / analysis_id / "1_individuais"

        if not results_dir.exists():
            return jsonify({
                'success': False,
                'error': 'Results folder not found'
            }), 404

        # Open Finder to results
        subprocess.run(['open', str(results_dir)])

        return jsonify({
            'success': True,
            'message': f'Opening results for {analysis_id}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/action/open-consolidated/<analysis_id>', methods=['POST'])
def api_open_consolidated(analysis_id):
    """Open REAL consolidated results"""
    try:
        consolidated_dir = WORKSPACE_DIR / analysis_id / "3_consolidados"

        if not consolidated_dir.exists():
            return jsonify({
                'success': False,
                'error': 'Consolidated folder not found'
            }), 404

        # Open Finder to consolidated
        subprocess.run(['open', str(consolidated_dir)])

        return jsonify({
            'success': True,
            'message': f'Opening consolidated results for {analysis_id}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def get_current_analysis_from_log():
    """Parse log file to detect current analysis in progress"""
    log_file = SCRIPTUREMON_DIR / "full_run.log"

    if not log_file.exists():
        return None

    try:
        # Read last 50 lines
        with open(log_file, 'r') as f:
            lines = f.readlines()[-50:]

        current_specialist = None
        current_author = None

        # Look for patterns like "[ARISTOTLE] Iniciando análise..." or "📖 [ARISTOTLE]"
        for line in reversed(lines):
            if 'Iniciando análise' in line or '📖' in line:
                # Extract author name between brackets
                import re
                match = re.search(r'\[([A-Z_]+)\]', line)
                if match:
                    current_author = match.group(1).lower()
                    # Detect specialist from context (look backwards)
                    for prev_line in reversed(lines[:lines.index(line)]):
                        if 'STRUCTURE' in prev_line.upper():
                            current_specialist = 'structure'
                            break
                        elif 'CHARACTER' in prev_line.upper():
                            current_specialist = 'character'
                            break
                        elif 'DIALOGUE' in prev_line.upper():
                            current_specialist = 'dialogue'
                            break
                    break

        if current_author:
            return {
                'specialist': current_specialist or 'unknown',
                'author': current_author,
                'timestamp': datetime.now().isoformat()
            }
    except Exception as e:
        print(f"Error reading log: {e}")

    return None

@app.route('/api/stream/progress')
def api_stream_progress():
    """Server-Sent Events stream for REAL-TIME updates (includes log monitoring)"""
    def generate():
        while True:
            checkpoints = find_all_checkpoints()

            # Get current analysis from log file
            current_from_log = get_current_analysis_from_log()

            # If we have current info from log, update the first checkpoint
            if current_from_log and checkpoints:
                # Find the running analysis
                for analysis in checkpoints:
                    if analysis['status'] in ['running', 'paused']:
                        # Override with log data
                        analysis['current_specialist'] = current_from_log['specialist']
                        analysis['current_author'] = current_from_log['author']
                        analysis['status'] = 'running'  # Force running if detected in log
                        analysis['log_detected'] = True
                        break

            data = json.dumps({
                'timestamp': datetime.now().isoformat(),
                'analyses': checkpoints,
                'current_from_log': current_from_log
            })
            yield f"data: {data}\n\n"
            time.sleep(2)  # Update every 2 seconds

    return Response(generate(), mimetype='text/event-stream')

# ============================================================================
# NEW ENDPOINTS FOR FULL WEB APP
# ============================================================================

@app.route('/api/screenplays/list')
def api_list_screenplays():
    """List available PDF files in inputs directory"""
    try:
        inputs_dir = SCRIPTUREMON_DIR / "inputs"
        screenplays = []

        if inputs_dir.exists():
            for pdf_file in inputs_dir.rglob("*.pdf"):
                stat = pdf_file.stat()
                screenplays.append({
                    'name': pdf_file.name,
                    'path': str(pdf_file),
                    'size': f"{stat.st_size / (1024*1024):.2f} MB",
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                })

        return jsonify({
            'success': True,
            'screenplays': sorted(screenplays, key=lambda x: x['modified'], reverse=True)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/action/start-analysis', methods=['POST'])
def api_start_analysis():
    """Start NEW analysis with specified parameters"""
    try:
        data = request.json
        screenplay_path = data.get('screenplay_path')
        model = data.get('model', 'ollama')  # ollama, gpt-5, or both

        if not screenplay_path or not Path(screenplay_path).exists():
            return jsonify({
                'success': False,
                'error': 'Invalid screenplay path'
            }), 400

        # Build command flags
        cmd_flags = '--yes'

        if model == 'gpt-5':
            cmd_flags += ' --model gpt-5'

        # Build command
        if model == 'both':
            # Start both analyses in parallel
            cmd_ollama = f"cd '{SCRIPTUREMON_DIR}' && python3 -u analyze_all_specialists.py '{screenplay_path}' {cmd_flags}"
            cmd_gpt5 = f"cd '{SCRIPTUREMON_DIR}' && python3 -u analyze_all_specialists.py '{screenplay_path}' --model gpt-5 {cmd_flags}"

            # Open first Terminal for Ollama
            subprocess.Popen([
                'osascript', '-e',
                f'tell application "Terminal" to do script "{cmd_ollama}"'
            ])

            time.sleep(1)

            # Open second Terminal for GPT-5
            subprocess.Popen([
                'osascript', '-e',
                f'tell application "Terminal" to do script "{cmd_gpt5}"'
            ])

            return jsonify({
                'success': True,
                'message': 'Both analyses started in separate Terminal windows'
            })
        else:
            # Single analysis
            cmd = f"cd '{SCRIPTUREMON_DIR}' && python3 -u analyze_all_specialists.py '{screenplay_path}' {cmd_flags}"

            subprocess.Popen([
                'osascript', '-e',
                f'tell application "Terminal" to do script "{cmd}"'
            ])

            return jsonify({
                'success': True,
                'message': f'Analysis started with {model}'
            })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/specialists/list')
def api_list_specialists():
    """List all 24 specialists with details"""
    specialists = [
        {'id': 'character', 'name': 'DrCharacter', 'icon': '👤', 'authors': 13, 'type': 'Character Analysis'},
        {'id': 'structure', 'name': 'DrStructure', 'icon': '🏗️', 'authors': 13, 'type': 'Structure Analysis'},
        {'id': 'theme', 'name': 'DrTheme', 'icon': '🎭', 'authors': 13, 'type': 'Theme Analysis'},
        {'id': 'genre', 'name': 'DrGenre', 'icon': '🎬', 'authors': 13, 'type': 'Genre Analysis'},
        {'id': 'dialogue', 'name': 'DrDialogue', 'icon': '💬', 'authors': 13, 'type': 'Dialogue Analysis'},
        {'id': 'pacing', 'name': 'DrPacing', 'icon': '⚡', 'authors': 13, 'type': 'Pacing Analysis'},
        {'id': 'transitions', 'name': 'DrTransitions', 'icon': '🔄', 'authors': 13, 'type': 'Transitions Analysis'},
        {'id': 'opening', 'name': 'DrOpening', 'icon': '🎬', 'authors': 13, 'type': 'Opening Analysis'},
        {'id': 'climax', 'name': 'DrClimax', 'icon': '🔥', 'authors': 13, 'type': 'Climax Analysis'},
        {'id': 'resolution', 'name': 'DrResolution', 'icon': '🎯', 'authors': 13, 'type': 'Resolution Analysis'},
    ]

    authors = ['McKee', 'Field', 'Truby', 'Campbell', 'Vogler', 'Seger', 'Snyder',
               'Egri', 'Weiland', 'Aristotle', 'Cowgill', 'McKee Character', 'McKee Dialogue']

    return jsonify({
        'success': True,
        'specialists': specialists,
        'authors': authors,
        'total_analyses': len(specialists) * len(authors)
    })

@app.route('/api/system/config')
def api_system_config():
    """Get system configuration"""
    try:
        # Check if API key exists
        env_file = SCRIPTUREMON_DIR / ".env"
        has_api_key = False

        if env_file.exists():
            with open(env_file) as f:
                content = f.read()
                has_api_key = 'OPENAI_API_KEY' in content and len(content.strip()) > 0

        # Check Ollama
        ollama_running = subprocess.run(
            ['pgrep', '-x', 'ollama'],
            capture_output=True
        ).returncode == 0

        return jsonify({
            'success': True,
            'config': {
                'has_api_key': has_api_key,
                'ollama_running': ollama_running,
                'scripturemon_dir': str(SCRIPTUREMON_DIR),
                'workspace_dir': str(WORKSPACE_DIR)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("🎬 SCRIPTUREMON WEB SERVER (REAL SYSTEM)")
    print("=" * 80)
    print()
    print(f"📁 Scripturemon Dir: {SCRIPTUREMON_DIR}")
    print(f"📂 Workspace Dir:    {WORKSPACE_DIR}")
    print(f"🎨 UI Dir:           {UI_DIR}")
    print(f"📱 macOS App:        {APP_PATH}")
    print()
    print("🚀 Starting server...")
    print()
    print("📊 Access dashboard at: http://localhost:8080")
    print("🔗 API endpoints:")
    print("   DATA:")
    print("     - GET  /api/analyses/list")
    print("     - GET  /api/analysis/<id>")
    print("     - GET  /api/system/stats")
    print("     - GET  /api/stream/progress (SSE)")
    print()
    print("   ACTIONS:")
    print("     - POST /api/action/new-analysis")
    print("     - POST /api/action/continue-analysis/<id>")
    print("     - POST /api/action/open-results/<id>")
    print("     - POST /api/action/open-consolidated/<id>")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 80)
    print()

    app.run(host='127.0.0.1', port=8080, debug=False, threaded=True)
