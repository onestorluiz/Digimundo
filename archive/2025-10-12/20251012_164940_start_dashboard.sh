#!/bin/bash
################################################################################
# SCRIPTUREMON DASHBOARD - Startup Script
# Starts the web server and opens the Digimon-style UI
################################################################################

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_FILE="/tmp/scripturemon_web_server.log"
PID_FILE="/tmp/scripturemon_web_server.pid"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo "🎬 SCRIPTUREMON DASHBOARD"
echo "=========================================="
echo ""

# Check if server is already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Server already running (PID: $OLD_PID)${NC}"
        echo ""
        echo "📊 Dashboard: http://localhost:8080"
        echo "📄 Logs:      tail -f $LOG_FILE"
        echo ""
        read -p "Stop and restart? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${BLUE}🛑 Stopping old server...${NC}"
            kill "$OLD_PID" 2>/dev/null
            sleep 2
        else
            open http://localhost:8080
            exit 0
        fi
    fi
fi

# Start server
echo -e "${BLUE}🚀 Starting web server...${NC}"
cd "$SCRIPT_DIR"
python3 web_server.py > "$LOG_FILE" 2>&1 &
SERVER_PID=$!
echo "$SERVER_PID" > "$PID_FILE"

# Wait for server to start
sleep 2

# Check if server started successfully
if ps -p "$SERVER_PID" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Server started successfully!${NC}"
    echo ""
    echo "=========================================="
    echo -e "${GREEN}📊 Dashboard:${NC} http://localhost:8080"
    echo -e "${BLUE}📄 Logs:${NC}      tail -f $LOG_FILE"
    echo -e "${YELLOW}🛑 Stop:${NC}      kill $SERVER_PID"
    echo "=========================================="
    echo ""

    # Open browser
    echo "🌐 Opening dashboard in browser..."
    sleep 1
    open http://localhost:8080

    echo ""
    echo -e "${GREEN}✓ Dashboard is live!${NC}"
    echo ""
else
    echo -e "${RED}❌ Failed to start server${NC}"
    echo "Check logs: tail $LOG_FILE"
    exit 1
fi
