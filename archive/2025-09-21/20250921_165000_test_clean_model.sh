#!/bin/bash

echo "🧪 TESTING CLEAN TOKEN TURBO"
echo "================================"

# Test the clean model
echo "Starting test at $(date +%H:%M:%S)"
echo "Test prompt: Analyze hero journey" | ollama run token-turbo-clean &
OLLAMA_PID=$!

# Monitor CPU for 20 seconds
echo "Monitoring CPU usage:"
for i in 1 2 3 4 5 6 7 8 9 10; do
    sleep 2
    CPU=$(ps aux | grep ollama | grep -v grep | awk '{sum+=$3} END {printf "%.1f", sum}')
    echo "  $(date +%H:%M:%S): CPU = ${CPU:-0}%"
done

# Kill if still running
kill $OLLAMA_PID 2>/dev/null

echo "================================"
echo "Test complete"