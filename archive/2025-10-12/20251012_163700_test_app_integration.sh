#!/bin/bash
#
# 🔍 SCRIPTUREMON APP - COMPLETE DEBUGGING SCRIPT
# Tests all components of the macOS app and system integration
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
readonly SCRIPTUREMON_DIR="/Users/clubproducoes/Digimundo/scripturemon"
readonly APP_PATH="/Applications/Analyze Screenplay.app"
readonly REQUIRED_MODEL="scripturemon-optimized"

# Test counters
TESTS_TOTAL=0
TESTS_PASSED=0
TESTS_FAILED=0

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

header() {
    echo
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${BLUE}$1${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

test_start() {
    ((TESTS_TOTAL++))
    echo -n "  Testing: $1 ... "
}

test_pass() {
    ((TESTS_PASSED++))
    echo -e "${GREEN}✅ PASS${NC}"
    if [ -n "${1:-}" ]; then
        echo "          └─ $1"
    fi
}

test_fail() {
    ((TESTS_FAILED++))
    echo -e "${RED}❌ FAIL${NC}"
    if [ -n "${1:-}" ]; then
        echo "          └─ $1"
    fi
}

test_warn() {
    echo -e "${YELLOW}⚠️  WARN${NC}"
    if [ -n "${1:-}" ]; then
        echo "          └─ $1"
    fi
}

# ============================================================================
# TEST 1: PATHS AND DIRECTORIES
# ============================================================================

test_paths_and_directories() {
    header "TEST 1: PATHS AND DIRECTORIES"

    # Test scripturemon directory
    test_start "Scripturemon directory exists"
    if [ -d "$SCRIPTUREMON_DIR" ]; then
        test_pass "$SCRIPTUREMON_DIR"
    else
        test_fail "Directory not found: $SCRIPTUREMON_DIR"
    fi

    # Test macOS app
    test_start "macOS app exists"
    if [ -d "$APP_PATH" ]; then
        test_pass "$APP_PATH"
    else
        test_fail "App not found: $APP_PATH"
    fi

    # Test workspace directory
    test_start "Workspace directory exists"
    if [ -d "$SCRIPTUREMON_DIR/workspace" ]; then
        test_pass "$SCRIPTUREMON_DIR/workspace"
    else
        test_fail "Workspace not found"
    fi

    # Test outputs directory
    test_start "Outputs directory exists"
    if [ -d "$SCRIPTUREMON_DIR/workspace/outputs" ]; then
        test_pass "$SCRIPTUREMON_DIR/workspace/outputs"
    else
        test_warn "Will be created on first analysis"
    fi

    # Test inputs directory
    test_start "Inputs directory exists"
    if [ -d "$SCRIPTUREMON_DIR/inputs" ]; then
        test_pass "$SCRIPTUREMON_DIR/inputs"
    else
        test_fail "Inputs directory not found"
    fi
}

# ============================================================================
# TEST 2: APP STRUCTURE
# ============================================================================

test_app_structure() {
    header "TEST 2: APP STRUCTURE"

    # Test run script
    test_start "App run script exists"
    if [ -f "$APP_PATH/Contents/MacOS/run" ]; then
        local version=$(head -20 "$APP_PATH/Contents/MacOS/run" | grep "Version:" | cut -d':' -f2 | xargs)
        test_pass "Version: $version"
    else
        test_fail "Run script not found"
    fi

    # Test run script is executable
    test_start "Run script is executable"
    if [ -x "$APP_PATH/Contents/MacOS/run" ]; then
        test_pass
    else
        test_fail "Run script not executable"
    fi

    # Test Info.plist
    test_start "Info.plist exists"
    if [ -f "$APP_PATH/Contents/Info.plist" ]; then
        local bundle_id=$(/usr/libexec/PlistBuddy -c "Print CFBundleIdentifier" "$APP_PATH/Contents/Info.plist" 2>/dev/null || echo "unknown")
        test_pass "Bundle ID: $bundle_id"
    else
        test_fail "Info.plist not found"
    fi

    # Test PDF handler registration
    test_start "PDF handler configured"
    if /usr/libexec/PlistBuddy -c "Print CFBundleDocumentTypes:0:CFBundleTypeExtensions:0" "$APP_PATH/Contents/Info.plist" 2>/dev/null | grep -q "pdf"; then
        test_pass "PDF handler registered"
    else
        test_warn "PDF handler not registered"
    fi
}

# ============================================================================
# TEST 3: PYTHON SCRIPTS
# ============================================================================

test_python_scripts() {
    header "TEST 3: PYTHON SCRIPTS"

    cd "$SCRIPTUREMON_DIR" || exit 1

    # Test analyze_all_specialists.py
    test_start "analyze_all_specialists.py exists"
    if [ -f "analyze_all_specialists.py" ]; then
        local lines=$(wc -l < "analyze_all_specialists.py")
        test_pass "$lines lines"
    else
        test_fail "Main script not found"
    fi

    # Test new features scripts
    local scripts=(
        "dashboard.py"
        "compare_analyses.py"
        "usage_stats.py"
        "benchmark_performance.py"
        "cleanup_checkpoints.py"
        "analysis_history.py"
        "setup_wizard.py"
        "partial_analysis.py"
        "model_comparison.py"
        "analysis_preview.py"
    )

    test_start "New features scripts (10 files)"
    local found=0
    for script in "${scripts[@]}"; do
        [ -f "$script" ] && ((found++))
    done
    if [ $found -eq 10 ]; then
        test_pass "All 10 scripts present"
    elif [ $found -gt 5 ]; then
        test_warn "$found/10 scripts found"
    else
        test_fail "Only $found/10 scripts found"
    fi
}

# ============================================================================
# TEST 4: DEPENDENCIES
# ============================================================================

test_dependencies() {
    header "TEST 4: DEPENDENCIES"

    # Test Python
    test_start "Python 3 available"
    if command -v python3 >/dev/null 2>&1; then
        local py_version=$(python3 --version 2>&1 | cut -d' ' -f2)
        test_pass "Version: $py_version"
    else
        test_fail "Python 3 not found"
    fi

    # Test Ollama
    test_start "Ollama installed"
    if command -v ollama >/dev/null 2>&1; then
        local ollama_path=$(which ollama)
        test_pass "Path: $ollama_path"
    else
        test_fail "Ollama not found"
    fi

    # Test Ollama running
    test_start "Ollama service running"
    if pgrep -x "ollama" >/dev/null; then
        test_pass "PID: $(pgrep -x ollama)"
    else
        test_fail "Ollama not running"
    fi

    # Test model
    test_start "Model '$REQUIRED_MODEL' available"
    if ollama list | awk '{print $1}' | grep -qE "^${REQUIRED_MODEL}(:|$)"; then
        local model_size=$(ollama list | grep "$REQUIRED_MODEL" | awk '{print $3,$4}' | head -1)
        test_pass "Size: $model_size"
    else
        test_fail "Model not found"
    fi
}

# ============================================================================
# TEST 5: API KEYS AND CONFIG
# ============================================================================

test_api_keys() {
    header "TEST 5: API KEYS AND CONFIG"

    cd "$SCRIPTUREMON_DIR" || exit 1

    # Test .env file
    test_start ".env file exists"
    if [ -f ".env" ]; then
        test_pass
    else
        test_warn "No .env file (GPT-5 will not work)"
    fi

    # Test API key
    test_start "OPENAI_API_KEY configured"
    if [ -f ".env" ]; then
        source ".env" 2>/dev/null || true
        if [ -n "${OPENAI_API_KEY:-}" ]; then
            local key_preview="${OPENAI_API_KEY:0:10}...${OPENAI_API_KEY: -5}"
            test_pass "Key: $key_preview"
        else
            test_warn "No API key in .env"
        fi
    else
        test_warn "No .env file"
    fi
}

# ============================================================================
# TEST 6: CHECKPOINT SYSTEM
# ============================================================================

test_checkpoint_system() {
    header "TEST 6: CHECKPOINT SYSTEM"

    cd "$SCRIPTUREMON_DIR" || exit 1

    # Count checkpoints
    test_start "Find incomplete analyses"
    local checkpoint_count=0
    for checkpoint_dir in workspace/outputs/*_all_specialists_*/2_logs; do
        if [ -f "$checkpoint_dir/checkpoint.json" ]; then
            ((checkpoint_count++))
        fi
    done

    if [ $checkpoint_count -gt 0 ]; then
        test_pass "Found $checkpoint_count checkpoint(s)"
    else
        test_warn "No checkpoints found (normal for new installation)"
    fi

    # Test checkpoint format
    if [ $checkpoint_count -gt 0 ]; then
        test_start "Checkpoint format validation"
        local first_checkpoint=$(find workspace/outputs -name "checkpoint.json" -type f | head -1)
        if [ -n "$first_checkpoint" ]; then
            if python3 -c "import json; json.load(open('$first_checkpoint'))" 2>/dev/null; then
                local completed=$(python3 -c "import json; print(len(json.load(open('$first_checkpoint')).get('completed', [])))")
                local total=$(python3 -c "import json; print(json.load(open('$first_checkpoint')).get('total_analyses', 0))")
                test_pass "Valid JSON ($completed/$total completed)"
            else
                test_fail "Invalid JSON format"
            fi
        fi
    fi
}

# ============================================================================
# TEST 7: INTEGRATION WITH NEW FEATURES
# ============================================================================

test_new_features_integration() {
    header "TEST 7: INTEGRATION WITH NEW FEATURES"

    cd "$SCRIPTUREMON_DIR" || exit 1

    # Test if analyze_all_specialists.py has usage_stats import
    test_start "Usage stats integration"
    if grep -q "from usage_stats import UsageStats" analyze_all_specialists.py 2>/dev/null; then
        test_pass "Integrated in analyze_all_specialists.py"
    else
        test_warn "Not integrated (tracking will not work)"
    fi

    # Test if analyze_all_specialists.py has send_notification function
    test_start "macOS notifications integration"
    if grep -q "def send_notification" analyze_all_specialists.py 2>/dev/null; then
        test_pass "Notification system integrated"
    else
        test_warn "Not integrated"
    fi

    # Test if analyze_all_specialists.py has cost tracking
    test_start "Cost tracking integration"
    if grep -q "cost_per_analysis" analyze_all_specialists.py 2>/dev/null; then
        test_pass "Cost tracking integrated"
    else
        test_warn "Not integrated"
    fi
}

# ============================================================================
# TEST 8: CLI TOOLS EXECUTION
# ============================================================================

test_cli_tools() {
    header "TEST 8: CLI TOOLS EXECUTION"

    cd "$SCRIPTUREMON_DIR" || exit 1

    # Test dashboard
    test_start "dashboard.py syntax"
    if python3 -m py_compile dashboard.py 2>/dev/null; then
        test_pass
    else
        test_fail "Syntax error in dashboard.py"
    fi

    # Test compare_analyses
    test_start "compare_analyses.py syntax"
    if python3 -m py_compile compare_analyses.py 2>/dev/null; then
        test_pass
    else
        test_fail "Syntax error in compare_analyses.py"
    fi

    # Test analysis_preview
    test_start "analysis_preview.py syntax"
    if python3 -m py_compile analysis_preview.py 2>/dev/null; then
        test_pass
    else
        test_fail "Syntax error in analysis_preview.py"
    fi
}

# ============================================================================
# TEST 9: macOS NOTIFICATIONS
# ============================================================================

test_macos_notifications() {
    header "TEST 9: macOS NOTIFICATIONS"

    # Test osascript availability
    test_start "osascript available"
    if command -v osascript >/dev/null 2>&1; then
        test_pass
    else
        test_fail "osascript not found"
    fi

    # Test notification send
    test_start "Send test notification"
    if osascript -e 'display notification "Scripturemon debugging test" with title "🎬 Test" subtitle "App Integration"' 2>/dev/null; then
        test_pass "Notification sent successfully"
    else
        test_fail "Could not send notification"
    fi
}

# ============================================================================
# TEST 10: PERMISSIONS
# ============================================================================

test_permissions() {
    header "TEST 10: PERMISSIONS"

    cd "$SCRIPTUREMON_DIR" || exit 1

    # Test write permission in workspace
    test_start "Write permission in workspace"
    if touch workspace/.test_write 2>/dev/null; then
        rm -f workspace/.test_write
        test_pass
    else
        test_fail "Cannot write to workspace/"
    fi

    # Test execute permission on scripts
    test_start "Execute permission on dashboard.py"
    if [ -x "dashboard.py" ]; then
        test_pass
    else
        test_warn "Not executable (chmod +x recommended)"
    fi
}

# ============================================================================
# SUMMARY
# ============================================================================

show_summary() {
    header "TEST SUMMARY"

    local pass_rate=0
    if [ $TESTS_TOTAL -gt 0 ]; then
        pass_rate=$((TESTS_PASSED * 100 / TESTS_TOTAL))
    fi

    echo
    echo "  Total Tests:  $TESTS_TOTAL"
    echo -e "  ${GREEN}Passed:       $TESTS_PASSED${NC}"
    echo -e "  ${RED}Failed:       $TESTS_FAILED${NC}"
    echo "  Pass Rate:    ${pass_rate}%"
    echo

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${GREEN}  ✅ ALL TESTS PASSED - APP IS FULLY OPERATIONAL${NC}"
        echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    elif [ $pass_rate -ge 80 ]; then
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${YELLOW}  ⚠️  MOST TESTS PASSED - MINOR ISSUES DETECTED${NC}"
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    else
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${RED}  ❌ MULTIPLE FAILURES - APP MAY NOT WORK CORRECTLY${NC}"
        echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    fi

    echo
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    clear
    echo
    echo "🔍 SCRIPTUREMON APP - COMPLETE DEBUGGING TEST"
    echo "Testing all components and system integration..."
    echo

    test_paths_and_directories
    test_app_structure
    test_python_scripts
    test_dependencies
    test_api_keys
    test_checkpoint_system
    test_new_features_integration
    test_cli_tools
    test_macos_notifications
    test_permissions

    show_summary

    echo "💡 Next steps:"
    echo "   - Fix any failed tests"
    echo "   - Run: python3 dashboard.py --snapshot --simple"
    echo "   - Test app: open '/Applications/Analyze Screenplay.app'"
    echo
}

main "$@"
