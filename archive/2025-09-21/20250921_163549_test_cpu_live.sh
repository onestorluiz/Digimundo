#!/bin/bash
# Live CPU test for Token Turbo models

echo "🚀 TESTING TOKEN TURBO CPU USAGE - M3 Ultra (28 CPU, 60 GPU, 32 Neural)"
echo "================================================================"

TEST_PROMPT="Analyze the hero's journey in The Matrix screenplay."

# Function to monitor CPU
monitor_cpu() {
    local model=$1
    echo -e "\n📊 Testing: $model"
    echo "Starting at: $(date +%H:%M:%S)"

    # Start ollama in background
    echo "$TEST_PROMPT" | ollama run "$model" &
    OLLAMA_PID=$!

    # Monitor CPU for 30 seconds
    echo "CPU Usage during processing:"
    for i in {1..10}; do
        CPU=$(top -l 1 -stats pid,command,cpu | grep ollama | awk '{sum+=$3} END {print sum}')
        echo "  $(date +%H:%M:%S) - CPU: ${CPU}%"
        sleep 3
    done

    # Wait for completion
    wait $OLLAMA_PID
    echo "Finished at: $(date +%H:%M:%S)"
}

# Test each model
echo -e "\n============================================================"
echo "TEST 1: GPU 30 (More CPU expected)"
monitor_cpu "token-turbo-gpu30"

echo -e "\n============================================================"
echo "TEST 2: GPU 40 (Balanced)"
monitor_cpu "token-turbo-gpu40"

echo -e "\n============================================================"
echo "TEST 3: GPU 50 (Current ECO)"
monitor_cpu "mixtral-token-turbo:latest"

echo -e "\n============================================================"
echo "TEST 4: GPU 60 (More GPU)"
monitor_cpu "token-turbo-gpu60"

echo -e "\n============================================================"
echo "✅ TEST COMPLETE"