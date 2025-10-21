#!/bin/bash
################################################################################
# SCRIPTUREMON DASHBOARD - Stop Script
# Stops the web server
################################################################################

PID_FILE="/tmp/scripturemon_web_server.pid"

echo ""
echo "🛑 STOPPING SCRIPTUREMON DASHBOARD"
echo "=========================================="
echo ""

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        kill "$PID"
        rm "$PID_FILE"
        echo "✓ Server stopped (PID: $PID)"
    else
        echo "⚠️  Server not running (PID file exists but process not found)"
        rm "$PID_FILE"
    fi
else
    # Try to find and kill by process name
    if pkill -f "python3 web_server.py"; then
        echo "✓ Server stopped"
    else
        echo "⚠️  No running server found"
    fi
fi

echo ""
