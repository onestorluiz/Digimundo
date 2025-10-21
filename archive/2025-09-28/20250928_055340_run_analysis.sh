#!/bin/bash
# Script principal para executar análise Scripturemon Ultimate

if [ $# -lt 1 ]; then
    echo "Usage: ./run_analysis.sh <screenplay_file> [title]"
    echo "Example: ./run_analysis.sh myscript.txt 'My Movie'"
    exit 1
fi

SCREENPLAY_FILE="$1"
TITLE="${2:-$(basename "$SCREENPLAY_FILE" .txt)}"

echo "🎬 SCRIPTUREMON ULTIMATE ANALYSIS"
echo "================================"
echo "📄 Screenplay: $SCREENPLAY_FILE"
echo "🎯 Title: $TITLE"
echo ""

# Run the main system
python3 src/core/scripturemon_ultimate_system.py "$SCREENPLAY_FILE" "$TITLE"

echo ""
echo "✅ Analysis complete! Check analysis_reports/ for the full report."