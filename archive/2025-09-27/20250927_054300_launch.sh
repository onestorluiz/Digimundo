#!/bin/bash
#
# OMEGA-ASCENT v4.0.0 Launch Script
# Sistema Digivolve Digimon - MEGA++ Stage
#

echo "=========================================="
echo "   OMEGA-ASCENT v4.0.0 - MEGA++ STAGE"
echo "   Advanced Screenplay Analysis System"
echo "=========================================="

# Check Python version
python3 --version

# Check if screenplay argument provided
if [ $# -eq 0 ]; then
    echo "Usage: ./launch.sh <screenplay.txt> [options]"
    echo ""
    echo "Options:"
    echo "  --fast     Fast mode (reduced features)"
    echo "  --debug    Debug mode (verbose output)"
    echo "  --bench    Run with benchmarking"
    echo ""
    exit 1
fi

# Set environment
export PYTHONPATH="$(pwd):$PYTHONPATH"
export OMEGA_VERSION="4.0.0"
export OMEGA_STAGE="mega++"

# Run OMEGA-ASCENT
echo ""
echo "🚀 Launching OMEGA-ASCENT..."
echo ""

python3 omega_cli.py "$@"

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Analysis complete!"
    echo "📁 Results saved to output/"
else
    echo ""
    echo "❌ Analysis failed. Check logs for details."
    exit 1
fi
