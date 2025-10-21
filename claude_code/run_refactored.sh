#!/bin/bash
#
# 🎬 Scripturemon v3.0 - Professional Screenplay Analyzer
# Native macOS app with checkpoints, resume, and quality improvement
#
# Author: Digimundo
# Version: 3.0 (REFACTORED)
# Features:
#   - 22 Specialists (Triple-Core)
#   - Checkpoint system (never lose work)
#   - Interactive menu (resume/retry/improve)
#   - Benchmark-based quality improvement
#

set -euo pipefail

# ============================================================================
# CONFIGURATION
# ============================================================================

readonly SCRIPTUREMON_DIR="/Users/clubproducoes/Digimundo/scripturemon-clean"
readonly BENCHMARK_DIR="/Users/clubproducoes/Digimundo/claude_code"
readonly SESSIONS_DIR="$SCRIPTUREMON_DIR/workspace/sessions"
readonly TEMP_DIR="/tmp/scripturemon"
readonly LOG_DIR="$SCRIPTUREMON_DIR/logs"
readonly REQUIRED_MODEL="scripturemon-optimized"
readonly APP_NAME="Scripturemon v3.0"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

# Show error dialog and exit
error_exit() {
    local message="$1"
    osascript -e "display dialog \"❌ Erro\n\n$message\" buttons {\"OK\"} default button 1 with icon stop with title \"$APP_NAME\""
    exit 1
}

# Show notification
notify() {
    local title="$1"
    local subtitle="$2"
    local message="${3:-}"
    osascript -e "display notification \"$message\" with title \"🎬 $title\" subtitle \"$subtitle\"" 2>/dev/null || true
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# ============================================================================
# VALIDATION
# ============================================================================

validate_environment() {
    # Check scripturemon-clean directory
    if [ ! -d "$SCRIPTUREMON_DIR" ]; then
        error_exit "Diretório scripturemon-clean não encontrado:\n$SCRIPTUREMON_DIR"
    fi

    # Check ScreenplayAnalyzer exists
    if [ ! -f "$SCRIPTUREMON_DIR/triple_core/orchestrators/screenplay_analyzer.py" ]; then
        error_exit "ScreenplayAnalyzer não encontrado!"
    fi

    # Check Ollama
    if ! command_exists ollama; then
        error_exit "Ollama não está instalado!\n\nInstale em: https://ollama.ai"
    fi

    if ! pgrep -x "ollama" >/dev/null; then
        error_exit "Ollama não está rodando!\n\nInicie o Ollama primeiro."
    fi

    # Check model
    if ! ollama list | awk '{print $1}' | grep -qE "^${REQUIRED_MODEL}(:|$)"; then
        error_exit "Modelo '$REQUIRED_MODEL' não encontrado!\n\nModelos disponíveis:\n$(ollama list | tail -n +2 | awk '{print $1}')"
    fi

    # Check Python
    if ! command_exists python3; then
        error_exit "Python 3 não encontrado!"
    fi

    # Create sessions directory
    mkdir -p "$SESSIONS_DIR"
    mkdir -p "$LOG_DIR"
}

# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

# Find existing sessions
find_sessions() {
    if [ ! -d "$SESSIONS_DIR" ]; then
        return
    fi

    # Find sessions with checkpoints
    find "$SESSIONS_DIR" -name "checkpoint.json" -type f 2>/dev/null | while read checkpoint; do
        session_dir=$(dirname "$checkpoint")
        session_name=$(basename "$session_dir")

        # Read checkpoint info
        if [ -f "$checkpoint" ]; then
            # Use Python to parse JSON safely
            python3 << EOF
import json
import sys
try:
    with open('$checkpoint', 'r') as f:
        data = json.load(f)
    completed = len(data.get('completed_specialists', []))
    total = 22
    screenplay = data.get('screenplay_path', 'Unknown')
    last_update = data.get('last_checkpoint', 'Unknown')
    print(f"{session_name}|{completed}/{total}|{screenplay}|{last_update}")
except Exception as e:
    pass
EOF
        fi
    done
}

# Show interactive menu
show_menu() {
    local sessions=$(find_sessions)

    if [ -z "$sessions" ]; then
        # No existing sessions - just start new
        return 1
    fi

    # Build session list for dialog
    local session_list=""
    local session_count=0

    while IFS='|' read -r name progress screenplay timestamp; do
        session_count=$((session_count + 1))
        local short_screenplay=$(basename "$screenplay")
        session_list="${session_list}${session_count}. ${short_screenplay}\n   Progress: ${progress}\n   Updated: ${timestamp}\n\n"
    done <<< "$sessions"

    # Show menu dialog
    local choice=$(osascript << EOF
tell application "System Events"
    activate
    set choice to button returned of (display dialog "📂 SESSÕES EXISTENTES ENCONTRADAS\n\n${session_list}" buttons {"Nova Análise", "Gerenciar Sessões"} default button 1 with title "$APP_NAME")
    return choice
end tell
EOF
2>/dev/null)

    if [ "$choice" = "Gerenciar Sessões" ]; then
        show_session_manager "$sessions"
        return 0
    else
        return 1  # Start new analysis
    fi
}

# Show session manager
show_session_manager() {
    local sessions="$1"

    # Build buttons array with session numbers
    local buttons=()
    local session_info=()
    local session_count=0

    while IFS='|' read -r name progress screenplay timestamp; do
        session_count=$((session_count + 1))
        buttons+=("Sessão ${session_count}")
        session_info+=("${name}|${progress}|${screenplay}|${timestamp}")
    done <<< "$sessions"

    # Show session selection
    local selected=$(osascript << EOF
tell application "System Events"
    activate
    set sessionList to {}
$(  local idx=1
    while IFS='|' read -r name progress screenplay timestamp; do
        local short_screenplay=$(basename "$screenplay")
        echo "    set end of sessionList to \"${idx}. ${short_screenplay} (${progress})\""
        idx=$((idx + 1))
    done <<< "$sessions"
)
    set choice to choose from list sessionList with prompt "Escolha uma sessão:" with title "$APP_NAME"
    if choice is false then
        return ""
    else
        return item 1 of choice
    end if
end tell
EOF
2>/dev/null)

    if [ -z "$selected" ]; then
        exit 0  # User cancelled
    fi

    # Extract session number
    local session_num=$(echo "$selected" | grep -oE '^[0-9]+' | head -1)

    if [ -z "$session_num" ]; then
        exit 0
    fi

    # Get session info
    local selected_info=$(echo "$sessions" | sed -n "${session_num}p")
    IFS='|' read -r name progress screenplay timestamp <<< "$selected_info"

    # Show action menu
    show_session_actions "$name" "$screenplay" "$progress"
}

# Show session actions
show_session_actions() {
    local session_name="$1"
    local screenplay="$2"
    local progress="$3"

    local short_screenplay=$(basename "$screenplay")

    local action=$(osascript << EOF
tell application "System Events"
    activate
    set choice to button returned of (display dialog "📂 Sessão: ${session_name}\n\n📄 Roteiro: ${short_screenplay}\n📊 Progresso: ${progress}\n\nO que deseja fazer?" buttons {"Cancelar", "Continuar", "Retry Falhados", "Improve Qualidade"} default button 2 with title "$APP_NAME")
    return choice
end tell
EOF
2>/dev/null)

    case "$action" in
        "Continuar")
            resume_session "$session_name" "continue"
            ;;
        "Retry Falhados")
            resume_session "$session_name" "retry_failed"
            ;;
        "Improve Qualidade")
            resume_session "$session_name" "improve_quality"
            ;;
        *)
            exit 0
            ;;
    esac
}

# Resume session
resume_session() {
    local session_name="$1"
    local mode="$2"
    local session_dir="$SESSIONS_DIR/$session_name"

    notify "$APP_NAME" "Resumindo Sessão" "Modo: $mode"

    # Create resume script
    local script_path="$TEMP_DIR/resume_${session_name}_$(date +%s).py"
    mkdir -p "$TEMP_DIR"

    cat > "$script_path" << PYEOF
#!/usr/bin/env python3
import sys
sys.path.insert(0, '$SCRIPTUREMON_DIR')

from triple_core.orchestrators.screenplay_analyzer import ScreenplayAnalyzer
from triple_core.utils.checkpoint_manager import CheckpointManager
import json

print("═" * 80)
print("🔄 RESUMINDO SESSÃO: $session_name")
print("═" * 80)
print()

# Load checkpoint
checkpoint_file = '$session_dir/checkpoint.json'
with open(checkpoint_file, 'r') as f:
    checkpoint = json.load(f)

screenplay_path = checkpoint['screenplay_path']
completed = checkpoint.get('completed_specialists', [])

print(f"📄 Roteiro: {screenplay_path}")
print(f"✅ Completados: {len(completed)}/22")
print()

# Initialize checkpoint manager
checkpoint_mgr = CheckpointManager('$session_dir')

# Initialize analyzer
analyzer = ScreenplayAnalyzer(
    llm_model='scripturemon-optimized',
    deep_context=True,
    checkpoint_manager=checkpoint_mgr
)

# Determine specialists to run based on mode
mode = '$mode'

if mode == 'continue':
    # Run all not completed
    specialists_to_run = None  # analyzer will figure it out
    print("▶️  Modo: Continuar de onde parou")
elif mode == 'retry_failed':
    # Run only failed specialists
    specialists_to_run = checkpoint_mgr.get_failed_specialists()
    print(f"▶️  Modo: Retry {len(specialists_to_run)} falhados")
elif mode == 'improve_quality':
    # Run only low quality specialists
    specialists_to_run = checkpoint_mgr.get_low_quality_specialists(threshold=7.0)
    print(f"▶️  Modo: Improve {len(specialists_to_run)} com qualidade <7.0")
else:
    specialists_to_run = None

print()
print("═" * 80)
print("🚀 INICIANDO ANÁLISE...")
print("═" * 80)
print()

# Run analysis
result = analyzer.analyze_screenplay(
    screenplay_path=screenplay_path,
    output_dir='$SCRIPTUREMON_DIR/workspace/outputs/analysis',
    resume=True,
    specialists_to_run=specialists_to_run
)

print()
print("═" * 80)
print("✅ SESSÃO COMPLETA!")
print("═" * 80)
print()
print(f"📄 HTML: {result['html_report_path']}")
print(f"📄 Markdown: {result['markdown_report_path']}")
print(f"🎯 Overall Score: {result['overall_quality'].overall_score:.1f}/100")
print()

PYEOF

    chmod +x "$script_path"

    # Open Terminal and run
    local log_file="$LOG_DIR/resume_${session_name}_$(date +%Y%m%d_%H%M%S).log"
    osascript -e "tell application \"Terminal\" to do script \"python3 '$script_path' 2>&1 | tee '$log_file'\"" >/dev/null 2>&1

    exit 0
}

# ============================================================================
# NEW ANALYSIS
# ============================================================================

# Get screenplay file
get_screenplay_file() {
    if [ -n "${1:-}" ]; then
        echo "$1"
        return
    fi

    local file=$(osascript << EOF
tell application "System Events"
    activate
    try
        set theFile to choose file with prompt "📄 Escolha o roteiro PDF:" of type {"pdf"}
        return POSIX path of theFile
    on error
        return ""
    end try
end tell
EOF
2>/dev/null)

    if [ -z "$file" ]; then
        exit 0
    fi

    echo "$file"
}

# Validate screenplay
validate_screenplay() {
    local file="$1"

    if [[ ! "$file" =~ \.pdf$ ]]; then
        error_exit "Arquivo precisa ser PDF!\n\nArquivo: $(basename "$file")"
    fi

    if [ ! -f "$file" ]; then
        error_exit "Arquivo não encontrado!"
    fi

    if [ ! -r "$file" ]; then
        error_exit "Não foi possível ler o arquivo!"
    fi
}

# Confirm analysis
confirm_analysis() {
    local file="$1"
    local filename=$(basename "$file")

    local response=$(osascript << EOF
tell application "System Events"
    activate
    set choice to button returned of (display dialog "📄 Roteiro: ${filename}\n\n🎯 Análise: 22 Specialists (Triple-Core)\n⏱️  Tempo estimado: 1-2 horas\n💾 Checkpoints: Automáticos (pode resumir)\n\n🚀 Pronto para analisar?" buttons {"Cancelar", "Analisar"} default button 2 with title "$APP_NAME")
    return choice
end tell
EOF
2>/dev/null)

    if [ "$response" != "Analisar" ]; then
        exit 0
    fi
}

# Create new analysis
start_new_analysis() {
    local screenplay_file="$1"
    local screenplay_name=$(basename "$screenplay_file" .pdf)
    local session_name="${screenplay_name}_$(date +%Y%m%d_%H%M%S)"
    local session_dir="$SESSIONS_DIR/$session_name"

    mkdir -p "$session_dir"

    notify "$APP_NAME" "Análise Iniciada" "22 Specialists com Checkpoints"

    # Create analysis script
    local script_path="$TEMP_DIR/analyze_${session_name}.py"
    mkdir -p "$TEMP_DIR"

    cat > "$script_path" << PYEOF
#!/usr/bin/env python3
import sys
sys.path.insert(0, '$SCRIPTUREMON_DIR')

from triple_core.orchestrators.screenplay_analyzer import ScreenplayAnalyzer
from triple_core.utils.checkpoint_manager import CheckpointManager

print("═" * 80)
print("🎬 SCRIPTUREMON v3.0 - TRIPLE-CORE ANALYZER")
print("═" * 80)
print()
print("📄 Roteiro: ${screenplay_name}")
print("📂 Sessão: ${session_name}")
print("⏰ Início: $(date '+%d/%m/%Y %H:%M:%S')")
print()
print("🔥 Novidades v3.0:")
print("   ✅ 22 Specialists (Character, Dialogue, Structure, etc.)")
print("   ✅ Checkpoints automáticos (nunca perde trabalho)")
print("   ✅ Resume/Retry/Improve (menu interativo)")
print("   ✅ Qualidade benchmark-driven (10/10)")
print()
print("═" * 80)
print("🚀 INICIANDO ANÁLISE...")
print("═" * 80)
print()

# Initialize checkpoint manager
checkpoint_mgr = CheckpointManager('$session_dir')

# Initialize analyzer
analyzer = ScreenplayAnalyzer(
    llm_model='scripturemon-optimized',
    deep_context=True,
    checkpoint_manager=checkpoint_mgr
)

# Run analysis
result = analyzer.analyze_screenplay(
    screenplay_path='$screenplay_file',
    output_dir='$SCRIPTUREMON_DIR/workspace/outputs/analysis',
    resume=False  # New analysis
)

print()
print("═" * 80)
print("✅ ANÁLISE COMPLETA!")
print("═" * 80)
print()
print(f"📄 HTML: {result['html_report_path']}")
print(f"📄 Markdown: {result['markdown_report_path']}")
print(f"🎯 Overall Score: {result['overall_quality'].overall_score:.1f}/100")
print(f"💾 Sessão: ${session_name}")
print()
print("💡 Para melhorar qualidade baixa:")
print("   Re-execute o app e escolha 'Improve Qualidade'")
print()

# Success notification
import subprocess
subprocess.run([
    'osascript', '-e',
    'display notification "✅ Análise completa! Score: {:.1f}/100" with title "🎉 Scripturemon v3.0" subtitle "${screenplay_name}" sound name "Glass"'.format(result['overall_quality'].overall_score)
], check=False)

PYEOF

    chmod +x "$script_path"

    # Open Terminal and run
    local log_file="$LOG_DIR/analyze_${session_name}.log"
    osascript -e "tell application \"Terminal\" to do script \"python3 '$script_path' 2>&1 | tee '$log_file'\"" >/dev/null 2>&1

    exit 0
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    # Validate environment
    validate_environment

    # Show menu if existing sessions
    if show_menu; then
        # Menu handled everything, exit
        exit 0
    fi

    # No existing sessions or user chose new analysis
    local screenplay_file=$(get_screenplay_file "${1:-}")
    validate_screenplay "$screenplay_file"
    confirm_analysis "$screenplay_file"
    start_new_analysis "$screenplay_file"
}

main "$@"
