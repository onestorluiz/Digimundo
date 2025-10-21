#!/bin/bash

# Test Phase 7: Ollama Integration
# Tests heavy models (19GB+) with Mac Studio M3 Ultra 96GB RAM

set -e

echo "========================================="
echo "PHASE 7: OLLAMA INTEGRATION TESTS"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run test
run_test() {
    local test_name="$1"
    local test_command="$2"

    echo -n "Testing $test_name... "

    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC}"
        ((TESTS_FAILED++))
    fi
}

# 1. Check Ollama installation
echo "1. OLLAMA ENVIRONMENT CHECK"
echo "----------------------------"

run_test "Ollama service" "ollama list"

# 2. Test heavy models availability
echo ""
echo "2. HEAVY MODELS CHECK (19GB+)"
echo "------------------------------"

# Check for our custom models
REQUIRED_MODELS=(
    "scripturemon-gpu-stable:latest"
    "deepseek-r1:32b"
)

for model in "${REQUIRED_MODELS[@]}"; do
    if ollama list | grep -q "$model"; then
        echo -e "${GREEN}✓${NC} $model available"
        ((TESTS_PASSED++))
    else
        echo -e "${YELLOW}⚠${NC} $model not found (will use fallback)"
    fi
done

# 3. Test OllamaCore singleton
echo ""
echo "3. OLLAMA CORE FUNCTIONALITY"
echo "-----------------------------"

run_test "OllamaCore import" "python3 -c 'from apps.scripturemon.ollama_core import OllamaCore'"

run_test "OllamaCore singleton" "python3 -c '
from apps.scripturemon.ollama_core import OllamaCore
core1 = OllamaCore()
core2 = OllamaCore()
assert core1 is core2, \"Singleton pattern failed\"
'"

run_test "Model availability check" "python3 -c '
from apps.scripturemon.ollama_core import OllamaCore
core = OllamaCore()
models = core.check_available_models()
assert len(models) > 0, \"No models available\"
print(f\"Found {len(models)} models\")
'"

# 4. Test Quadruple System
echo ""
echo "4. QUADRUPLE MODEL SYSTEM"
echo "-------------------------"

run_test "OllamaQuadruple import" "python3 -c 'from apps.scripturemon.ollama_quadruple import OllamaQuadruple'"

run_test "Quadruple initialization" "python3 -c '
from apps.scripturemon.ollama_quadruple import OllamaQuadruple
quad = OllamaQuadruple()
assert quad.executor is not None, \"Executor not initialized\"
'"

# 5. Test simple analysis (with timeout for heavy models)
echo ""
echo "5. HEAVY MODEL ANALYSIS TEST"
echo "-----------------------------"

echo -e "${YELLOW}Note: Heavy model tests may take 30-60 seconds...${NC}"

run_test "Single model analysis (timeout 120s)" "timeout 120 python3 -c '
from apps.scripturemon.ollama_core import OllamaCore
core = OllamaCore()
result = core.analyze_text(\"Teste rápido de análise\", timeout=120)
assert result is not None, \"Analysis failed\"
assert \"error\" not in result.lower(), f\"Error in result: {result}\"
print(f\"Analysis completed: {len(result)} chars\")
'"

# 6. Test memory integration
echo ""
echo "6. MEMORY SYSTEM INTEGRATION"
echo "-----------------------------"

run_test "Memory manager import" "python3 -c 'from apps.scripturemon.memory_simple import SimpleMemoryManager'"

run_test "Memory persistence" "python3 -c '
from apps.scripturemon.memory_simple import SimpleMemoryManager
import tempfile
import os

with tempfile.TemporaryDirectory() as tmpdir:
    # Test save
    mem1 = SimpleMemoryManager(tmpdir)
    mem1.add_memory(\"test\", \"Test memory entry\")
    mem1.save_memories()

    # Test load
    mem2 = SimpleMemoryManager(tmpdir)
    memories = mem2.get_memories(\"test\")
    assert len(memories) > 0, \"Memory not persisted\"
    assert memories[0][\"content\"] == \"Test memory entry\", \"Memory content mismatch\"
'"

# 7. Test backup system
echo ""
echo "7. BACKUP SYSTEM"
echo "----------------"

run_test "Backup manager import" "python3 -c 'from apps.scripturemon.backup_manager import BackupManager'"

run_test "Backup creation" "python3 -c '
from apps.scripturemon.backup_manager import BackupManager
import tempfile

with tempfile.TemporaryDirectory() as tmpdir:
    backup = BackupManager(tmpdir)

    # Create test data
    test_data = {\"test\": \"data\", \"score\": 62}

    # Create backup
    backup_file = backup.create_backup(test_data, \"test_backup\")
    assert backup_file is not None, \"Backup creation failed\"

    # List backups
    backups = backup.list_backups()
    assert len(backups) > 0, \"No backups found\"
'"

# 8. Test pipeline integration
echo ""
echo "8. PIPELINE INTEGRATION"
echo "-----------------------"

run_test "Pipeline orchestrator import" "python3 -c 'from apps.scripturemon.pipeline_orchestrator import PipelineOrchestrator'"

run_test "Pipeline with Ollama" "python3 -c '
from apps.scripturemon.pipeline_orchestrator import PipelineOrchestrator
orch = PipelineOrchestrator()

# Simple test text
test_text = \"INT. CASA - DIA\\nJoão entra na sala.\"

# Process through pipeline
result = orch.process_screenplay(test_text, use_ollama=True)
assert result is not None, \"Pipeline processing failed\"
assert \"score\" in result, \"No score in result\"
assert result[\"score\"] == 62, f\"Expected score 62, got {result.get(\"score\")}\"
'"

# 9. Test chat interface
echo ""
echo "9. CHAT INTERFACE"
echo "-----------------"

run_test "Chat simple import" "python3 -c 'from apps.chat.chat_simple import ChatSimple'"

run_test "Chat initialization" "python3 -c '
from apps.chat.chat_simple import ChatSimple
chat = ChatSimple()
assert chat.ollama is not None, \"Ollama not initialized in chat\"
'"

# 10. Performance test with heavy models
echo ""
echo "10. PERFORMANCE BENCHMARK"
echo "-------------------------"

echo -e "${YELLOW}Running performance test with 19GB model...${NC}"

python3 -c '
import time
from apps.scripturemon.ollama_core import OllamaCore

core = OllamaCore()
text = "Analise este roteiro: INT. CASA - NOITE. Um personagem solitário contempla sua vida."

# Test with timeout
start = time.time()
try:
    result = core.analyze_text(text, timeout=120)
    elapsed = time.time() - start

    if result and "error" not in result.lower():
        print(f"✓ Heavy model responded in {elapsed:.1f}s")
        print(f"  Response size: {len(result)} characters")
    else:
        print(f"⚠ Model returned error or empty response")
except Exception as e:
    print(f"✗ Performance test failed: {e}")
' || echo -e "${RED}Performance test failed${NC}"

# Final report
echo ""
echo "========================================="
echo "TEST RESULTS"
echo "========================================="
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ ALL TESTS PASSED!${NC}"
    echo "Phase 7 Ollama integration is working correctly."
    exit 0
else
    echo ""
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
    echo "Please review the failed tests above."
    exit 1
fi