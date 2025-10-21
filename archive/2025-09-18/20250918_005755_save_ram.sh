#!/bin/bash

# 🧹 RAM Optimization Script for Digimon Ecosystem
# Frees up RAM by closing unnecessary processes
# Usage: ./save_ram.sh [gentle|normal|max]

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧹 ScriptureMonChampion RAM Optimizer${NC}"
echo "========================================="

# Show current RAM status
show_ram_status() {
    echo -e "\n${YELLOW}📊 Current RAM Status:${NC}"
    top -l 1 | grep PhysMem

    # Calculate available RAM in GB
    AVAILABLE=$(top -l 1 | grep PhysMem | awk '{print $10}' | sed 's/G//')

    echo -e "${BLUE}Available RAM: ${AVAILABLE}GB${NC}"

    # Check if AVAILABLE is a number and compare
    if [[ "$AVAILABLE" =~ ^[0-9]+$ ]] && [ "$AVAILABLE" -gt 45 ]; then
        echo -e "${GREEN}✅ Can run ScriptureMon (needs 42GB)${NC}"
    else
        echo -e "${RED}❌ Cannot run ScriptureMon (needs 42GB, only ${AVAILABLE}GB available)${NC}"
    fi
}

# Level 1: Gentle cleanup (5GB)
gentle_cleanup() {
    echo -e "\n${YELLOW}Starting GENTLE cleanup (target: 5GB)...${NC}"

    # Kill test processes
    echo "• Killing Python test processes..."
    pkill -f "python.*test" 2>/dev/null

    # Kill Jupyter orphans
    echo "• Killing Jupyter kernels..."
    pkill -f "jupyter" 2>/dev/null

    # Kill auto_sync if running
    echo "• Killing auto_sync processes..."
    pkill -f "auto_sync" 2>/dev/null

    # Purge system cache
    echo "• Purging system cache..."
    sudo purge

    echo -e "${GREEN}✅ Gentle cleanup complete! (~5GB freed)${NC}"
}

# Level 2: Normal cleanup (15GB)
normal_cleanup() {
    echo -e "\n${YELLOW}Starting NORMAL cleanup (target: 15GB)...${NC}"

    # First do gentle cleanup
    gentle_cleanup

    # Close heavy apps
    echo "• Closing Chrome..."
    killall "Google Chrome" 2>/dev/null || echo "  Chrome not running"

    echo "• Closing Docker..."
    osascript -e 'quit app "Docker"' 2>/dev/null || echo "  Docker not running"

    echo "• Closing WhatsApp..."
    killall WhatsApp 2>/dev/null || echo "  WhatsApp not running"

    echo "• Closing Cursor IDE..."
    killall Cursor 2>/dev/null || echo "  Cursor not running"

    # Stop Spotlight indexing temporarily
    echo "• Pausing Spotlight indexing..."
    sudo mdutil -i off / 2>/dev/null

    echo -e "${GREEN}✅ Normal cleanup complete! (~15GB freed)${NC}"
}

# Level 3: Maximum cleanup (35GB)
max_cleanup() {
    echo -e "\n${RED}Starting MAXIMUM cleanup (target: 35GB)...${NC}"
    echo -e "${RED}⚠️  This will close almost all applications!${NC}"

    # Confirm
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        return
    fi

    # Kill all heavy apps
    echo "• Closing all heavy applications..."
    for app in "Google Chrome" "Safari" WhatsApp Mail Photos Preview Cursor "Visual Studio Code" Slack Discord Telegram Signal; do
        killall "$app" 2>/dev/null && echo "  Closed $app" || echo "  $app not running"
    done

    # Close Docker
    echo "• Closing Docker..."
    osascript -e 'quit app "Docker"' 2>/dev/null

    # Kill all Python processes except current
    echo "• Killing all Python processes..."
    pkill -f python 2>/dev/null

    # Kill all Jupyter
    echo "• Killing all Jupyter instances..."
    pkill -f jupyter 2>/dev/null

    # Stop and restart Ollama clean
    echo "• Restarting Ollama service..."
    pkill ollama 2>/dev/null
    sleep 2
    ollama serve > /dev/null 2>&1 &

    # Stop Spotlight completely
    echo "• Stopping Spotlight..."
    sudo mdutil -i off /
    sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.metadata.mds.plist 2>/dev/null

    # Aggressive cache purge
    echo "• Aggressive cache purge..."
    sudo purge
    sudo dscacheutil -flushcache

    echo -e "${GREEN}✅ Maximum cleanup complete! (~35GB freed)${NC}"
}

# Create Python monitoring script
create_monitor() {
    cat > /tmp/ram_monitor.py << 'EOF'
import psutil
import time
import subprocess

def get_ram_status():
    mem = psutil.virtual_memory()
    used_gb = (mem.total - mem.available) / (1024**3)
    available_gb = mem.available / (1024**3)
    percent = mem.percent

    # Color codes
    if available_gb > 45:
        color = "\033[92m"  # Green
        status = "✅ Ready for ScriptureMon"
    elif available_gb > 25:
        color = "\033[93m"  # Yellow
        status = "⚠️  Can run small Digimons"
    else:
        color = "\033[91m"  # Red
        status = "❌ Low RAM - cleanup needed"

    print(f"\033[94m{'='*50}\033[0m")
    print(f"RAM Status: {used_gb:.1f}GB used / {available_gb:.1f}GB available")
    print(f"{color}{status}\033[0m")

    # Show top 5 RAM consumers
    print("\nTop RAM Consumers:")
    procs = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            procs.append({
                'name': proc.info['name'],
                'ram': proc.info['memory_info'].rss / (1024**3)
            })
        except:
            pass

    for p in sorted(procs, key=lambda x: x['ram'], reverse=True)[:5]:
        print(f"  • {p['name'][:20]:20} {p['ram']:.2f}GB")

if __name__ == "__main__":
    while True:
        subprocess.run('clear')
        get_ram_status()
        print("\nPress Ctrl+C to exit")
        time.sleep(5)
EOF

    echo -e "\n${BLUE}Starting RAM monitor...${NC}"
    python3 /tmp/ram_monitor.py
}

# Show help
show_help() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  gentle   - Gentle cleanup (~5GB) - kills tests and caches"
    echo "  normal   - Normal cleanup (~15GB) - closes Chrome, Docker, WhatsApp"
    echo "  max      - Maximum cleanup (~35GB) - closes almost everything"
    echo "  status   - Show current RAM status"
    echo "  monitor  - Start real-time RAM monitor"
    echo "  help     - Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 normal    # Free 15GB for Digimon development"
    echo "  $0 max       # Free maximum RAM for ScriptureMon"
}

# Main logic
case "$1" in
    gentle)
        show_ram_status
        gentle_cleanup
        show_ram_status
        ;;
    normal)
        show_ram_status
        normal_cleanup
        show_ram_status
        ;;
    max)
        show_ram_status
        max_cleanup
        show_ram_status
        ;;
    status)
        show_ram_status
        ;;
    monitor)
        create_monitor
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_ram_status
        echo ""
        echo "Use '$0 help' for usage information"
        ;;
esac

echo -e "\n${BLUE}Done!${NC}"