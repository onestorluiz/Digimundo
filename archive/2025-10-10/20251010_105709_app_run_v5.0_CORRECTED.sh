#!/bin/bash
#
# 🎬 Scripturemon - Professional Screenplay Analyzer
# Native macOS app with FASE 3 compatibility
#
# Version: 5.0 (CORRECTED)
# System: analyze.py + personalized prompts + nivel 10
#
# CHANGELOG v5.0:
#   ✅ Fixed: Now calls analyze.py (not analyze_with_checkpoints.py)
#   ✅ Fixed: Added --use-personalized-prompts flag
#   ✅ Fixed: Proper --authors parameter for both modes
#   ✅ Added: PDF validation dialog before analysis
#   ✅ Added: Better notifications with estimated time
#

set -euo pipefail

# ============================================================================
# CONFIGURATION
# ============================================================================

readonly SCRIPTUREMON_DIR="/Users/clubproducoes/Digimundo/scripturemon"
readonly SESSIONS_DIR="$SCRIPTUREMON_DIR/workspace/sessions"
readonly REQUIRED_MODEL="scripturemon-optimized"
readonly APP_NAME="Scripturemon v5.0"

# All 13 authors for complete analysis
readonly ALL_AUTHORS="aristotle campbell cowgill dialogue egri field mckee mckee_character mckee_dialogue seger snyder truby vogler"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

error_exit() {
    local message="$1"
    osascript -e "display dialog \"❌ Erro\n\n$message\" buttons {\"OK\"} default button 1 with icon stop with title \"$APP_NAME\""
    exit 1
}

notify() {
    local title="$1"
    local subtitle="$2"
    local message="${3:-}"
    osascript -e "display notification \"$message\" with title \"🎬 $title\" subtitle \"$subtitle\"" 2>/dev/null || true
}

# ============================================================================
# VALIDATION
# ============================================================================

validate_environment() {
    # Check scripturemon directory
    if [ ! -d "$SCRIPTUREMON_DIR" ]; then
        error_exit "Scripturemon directory not found:\n$SCRIPTUREMON_DIR"
    fi

    # ✅ Check analyze.py (not analyze_with_checkpoints.py!)
    if [ ! -f "$SCRIPTUREMON_DIR/analyze.py" ]; then
        error_exit "analyze.py not found!"
    fi

    # Check Ollama
    if ! command -v ollama >/dev/null 2>&1; then
        error_exit "Ollama not installed!\n\nInstall from: https://ollama.ai"
    fi

    if ! pgrep -x "ollama" >/dev/null; then
        error_exit "Ollama not running!\n\nPlease start Ollama first."
    fi

    # Check model
    if ! ollama list | awk '{print $1}' | grep -qE "^${REQUIRED_MODEL}(:|$)"; then
        error_exit "Model '$REQUIRED_MODEL' not found!\n\nAvailable models:\n$(ollama list | tail -n +2 | awk '{print $1}')"
    fi

    # Check Python
    if ! command -v python3 >/dev/null 2>&1; then
        error_exit "Python 3 not found!"
    fi

    # Create directories
    mkdir -p "$SESSIONS_DIR"
}

# ============================================================================
# PDF VALIDATION (NEW in v5.0)
# ============================================================================

validate_pdf() {
    local pdf_file="$1"

    if [ ! -f "$pdf_file" ]; then
        error_exit "PDF not found:\n$pdf_file"
    fi

    # Get file info
    local size=$(du -h "$pdf_file" | cut -f1)
    local modified=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$pdf_file")
    local basename_file=$(basename "$pdf_file")

    # Show confirmation dialog
    local response=$(osascript << EOF
tell application "System Events"
    activate
    set choice to button returned of (display dialog "📄 CONFIRM SCREENPLAY\n\nFile: $basename_file\nSize: $size\nModified: $modified\n\nProceed with FASE 3 analysis?" buttons {"Cancel", "Confirm"} default button 2 with title "$APP_NAME")
    return choice
end tell
EOF
)

    if [ "$response" != "Confirm" ]; then
        return 1
    fi

    return 0
}

# ============================================================================
# NEW ANALYSIS
# ============================================================================

get_screenplay_file() {
    local default_path="${1:-}"

    if [ -n "$default_path" ] && [ -f "$default_path" ]; then
        echo "$default_path"
        return
    fi

    # File picker dialog
    local screenplay_file=$(osascript << 'EOF'
tell application "System Events"
    activate
    set theFile to choose file with prompt "Select screenplay file (PDF or TXT):" of type {"public.pdf", "public.plain-text"}
    return POSIX path of theFile
end tell
EOF
)

    echo "$screenplay_file"
}

choose_analysis_mode() {
    local response=$(osascript << EOF
tell application "System Events"
    activate
    set choice to button returned of (display dialog "🎯 CHOOSE ANALYSIS MODE\n\n✅ DIALOGUE ONLY (Recommended)\n   • Single author analysis\n   • Time: 5-7 minutes\n   • Perfect for testing\n   • FASE 3 quality (16.0/10)\n\n🌟 ALL 13 AUTHORS\n   • McKee, Truby, Field, Campbell...\n   • Time: 90-120 minutes  \n   • Complete multi-perspective\n   • FASE 3 quality (15.5-18.0/10)\n\nWhich mode?" buttons {"Cancel", "Dialogue Only", "All 13"} default button 2 with title "$APP_NAME")
    return choice
end tell
EOF
)

    echo "$response"
}

confirm_analysis() {
    local file="$1"
    local mode="$2"

    if [ "$mode" = "Dialogue Only" ]; then
        mode_desc="1 author (Dialogue)"
        time_est="5-7 minutes"
        quality="16.0/10 real score"
    else
        mode_desc="13 authors (McKee, Truby, Field...)"
        time_est="90-120 minutes"
        quality="15.5-18.0/10 real scores"
    fi

    osascript << EOF
tell application "System Events"
    activate
    display dialog "✅ FASE 3 SYSTEM READY\n\n📄 File: $(basename "$file")\n🎯 Mode: $mode_desc\n⏱️  Time: $time_est\n📊 Quality: $quality\n\n🔥 Features:\n   • Deep context (128k tokens)\n   • Personalized prompts\n   • Nivel 10 validation\n   • Cenas + Quotes + Rewrites\n\nThis will open Terminal and start analysis." buttons {"Cancel", "Start Analysis"} default button 2 with title "$APP_NAME"
end tell
EOF
}

start_new_analysis() {
    local screenplay_file="$1"
    local analysis_mode="$2"

    # ✅ Validate PDF before starting
    if ! validate_pdf "$screenplay_file"; then
        notify "Analysis Cancelled" "User cancelled PDF validation"
        exit 0
    fi

    # Determine authors list
    local authors_list=""
    if [ "$analysis_mode" = "All 13" ]; then
        authors_list="$ALL_AUTHORS"
        notify "Starting Analysis" "All 13 authors - FASE 3" "Estimated time: 90-120 minutes"
    else
        authors_list="dialogue"
        notify "Starting Analysis" "Dialogue author - FASE 3" "Estimated time: 5-7 minutes"
    fi

    # ✅ CORRECTED: Use analyze.py with FASE 3 parameters
    # Key changes from v4.0:
    #   - analyze.py (not analyze_with_checkpoints.py!)
    #   - --authors <list> (not --all flag!)
    #   - --use-personalized-prompts (CRITICAL!)
    #   - python3 -u for unbuffered output
    osascript << EOF
tell application "Terminal"
    activate
    do script "cd '$SCRIPTUREMON_DIR' && python3 -u analyze.py '$screenplay_file' --authors $authors_list --deep --use-personalized-prompts"
end tell
EOF

    notify "Analysis Started" "Check Terminal for progress" "FASE 3 system active"
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    # Validate environment
    validate_environment

    # New analysis flow
    local screenplay_file=$(get_screenplay_file "${1:-}")

    if [ -z "$screenplay_file" ]; then
        exit 0
    fi

    if [ ! -f "$screenplay_file" ]; then
        error_exit "File not found:\n$screenplay_file"
    fi

    # Choose mode
    local analysis_mode=$(choose_analysis_mode)

    if [ "$analysis_mode" = "Cancel" ] || [ -z "$analysis_mode" ]; then
        exit 0
    fi

    # Confirm
    if ! confirm_analysis "$screenplay_file" "$analysis_mode"; then
        exit 0
    fi

    # Start analysis
    start_new_analysis "$screenplay_file" "$analysis_mode"
}

main "$@"
