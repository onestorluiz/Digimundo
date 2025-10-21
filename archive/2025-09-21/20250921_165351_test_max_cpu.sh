#!/bin/bash

echo "🚀 TESTING MAX CPU TOKEN TURBO"
echo "================================"
echo "Config: 24 threads, GPU 40, Batch 4096"
echo ""

# Test the max CPU model
echo "Starting test at $(date +%H:%M:%S)"
echo "Analyze the hero's journey in The Matrix screenplay with detailed examples" | ollama run token-turbo-max-cpu &
OLLAMA_PID=$!

# Monitor CPU for 30 seconds
echo "Monitoring CPU usage:"
for i in {1..15}; do
    sleep 2
    CPU=$(ps aux | grep ollama | grep -v grep | awk '{sum+=$3} END {printf "%.1f", sum}')
    MEM=$(ps aux | grep ollama | grep -v grep | awk '{sum+=$4} END {printf "%.1f", sum}')
    echo "  $(date +%H:%M:%S): CPU = ${CPU:-0}% | RAM = ${MEM:-0}%"
done

# Kill if still running
kill $OLLAMA_PID 2>/dev/null

echo "================================"
echo "Test complete"