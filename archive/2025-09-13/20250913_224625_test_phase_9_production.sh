#!/bin/bash

# Test Phase 9: Production Optimization
# Testa cache, monitoring, performance e load balancing

set -e

echo "========================================="
echo "PHASE 9: PRODUCTION OPTIMIZATION TESTS"
echo "========================================="
echo ""

# Colors
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

# 1. Test Cache Manager
echo "1. CACHE MANAGER"
echo "----------------"

run_test "CacheManager import" "python3 -c 'from apps.scripturemon.cache_manager import CacheManager, get_cache_manager'"

run_test "Cache operations" "python3 -c '
from apps.scripturemon.cache_manager import get_cache_manager
cache = get_cache_manager()

# Set and get
cache.set(\"test_key\", \"test_value\")
value = cache.get(\"test_key\")
assert value == \"test_value\"

# Cache stats
stats = cache.get_stats()
assert stats[\"hits\"] > 0
'"

run_test "Cache decorator" "python3 -c '
from apps.scripturemon.cache_manager import get_cache_manager
import time

cache = get_cache_manager()

@cache.cached(ttl=60)
def expensive_function(x):
    time.sleep(0.1)
    return x * 2

# First call - slow
start = time.time()
result1 = expensive_function(5)
time1 = time.time() - start

# Second call - cached, fast
start = time.time()
result2 = expensive_function(5)
time2 = time.time() - start

assert result1 == result2 == 10
assert time2 < time1  # Cached call is faster
'"

# 2. Test Monitoring
echo ""
echo "2. MONITORING SYSTEM"
echo "--------------------"

run_test "MetricsCollector import" "python3 -c 'from apps.scripturemon.monitoring import MetricsCollector, get_metrics_collector'"

run_test "Metrics collection" "python3 -c '
from apps.scripturemon.monitoring import get_metrics_collector
import time

metrics = get_metrics_collector()

# Record some metrics
metrics.record_request(\"/test\", 0.5, success=True)
metrics.increment_counter(\"pipeline_runs\")

# Get summary
summary = metrics.get_metrics_summary()
assert \"system\" in summary
assert \"application\" in summary
assert summary[\"counters\"][\"total_requests\"] > 0

# Stop collector
metrics.stop()
'"

run_test "HealthChecker" "python3 -c '
from apps.scripturemon.monitoring import get_health_checker

health = get_health_checker()
status = health.get_health_status()

assert \"overall_status\" in status
assert \"checks\" in status
assert len(status[\"checks\"]) > 0
'"

# 3. Test Performance Optimizer
echo ""
echo "3. PERFORMANCE OPTIMIZER"
echo "------------------------"

run_test "PerformanceOptimizer import" "python3 -c 'from apps.scripturemon.performance_optimizer import PerformanceOptimizer, get_optimizer'"

run_test "Parallel map" "python3 -c '
from apps.scripturemon.performance_optimizer import get_optimizer

optimizer = get_optimizer()

# Test parallel map
def square(x):
    return x * x

items = list(range(10))
results = optimizer.parallel_map(square, items)

assert results == [x*x for x in items]
'"

run_test "Batch processing" "python3 -c '
from apps.scripturemon.performance_optimizer import BatchProcessor

processor = BatchProcessor(batch_size=3)

# Add items
futures = []
for i in range(5):
    future = processor.add(i)
    futures.append(future)

# Process batch
processor._process_batch()

# All futures should be resolved
for future in futures:
    assert future.done()
'"

# 4. Test Load Balancer
echo ""
echo "4. LOAD BALANCER"
echo "----------------"

run_test "LoadBalancer import" "python3 -c 'from apps.scripturemon.load_balancer import LoadBalancer, get_load_balancer'"

run_test "Model pool management" "python3 -c '
from apps.scripturemon.load_balancer import ModelPool

pool = ModelPool()
pool.register_model(\"test_model\", capacity=2)

# Get available model
model = pool.get_available_model()
assert model == \"test_model\"

# Acquire and release
assert pool.acquire_model(\"test_model\") == True
pool.release_model(\"test_model\", execution_time=0.5)

# Check stats
stats = pool.get_stats()
assert \"test_model\" in stats
assert stats[\"test_model\"][\"total_requests\"] == 1
'"

run_test "Task submission" "python3 -c '
from apps.scripturemon.load_balancer import get_load_balancer
import time

lb = get_load_balancer()

# Submit task
task_id = lb.submit_task(
    model=\"mistral:instruct\",
    payload={\"prompt\": \"test\"},
    priority=5
)

assert task_id.startswith(\"task_\")

# Check status
status = lb.get_status()
assert \"queue_size\" in status
assert \"models\" in status

# Shutdown
lb.shutdown()
'"

# 5. Integration Test
echo ""
echo "5. INTEGRATION TEST"
echo "-------------------"

run_test "Cache with monitoring" "python3 -c '
from apps.scripturemon.cache_manager import get_cache_manager
from apps.scripturemon.monitoring import get_metrics_collector

cache = get_cache_manager()
metrics = get_metrics_collector()

# Use cache
cache.set(\"integration_test\", \"value\")
value = cache.get(\"integration_test\")

# Record in metrics
metrics.increment_counter(\"cache_hits\")

# Verify
assert value == \"value\"
assert metrics.counters[\"cache_hits\"] > 0
'"

# 6. Performance Benchmark
echo ""
echo "6. PERFORMANCE BENCHMARK"
echo "------------------------"

echo -e "${YELLOW}Running performance benchmark...${NC}"

python3 -c '
import time
from apps.scripturemon.performance_optimizer import get_optimizer
from apps.scripturemon.cache_manager import get_cache_manager

optimizer = get_optimizer()
cache = get_cache_manager()

# Benchmark parallel processing
def process_item(x):
    return x ** 2

items = list(range(100))

# Sequential
start = time.time()
seq_results = [process_item(x) for x in items]
seq_time = time.time() - start

# Parallel
start = time.time()
par_results = optimizer.parallel_map(process_item, items)
par_time = time.time() - start

print(f"✓ Sequential: {seq_time:.3f}s")
print(f"✓ Parallel: {par_time:.3f}s")
print(f"✓ Speedup: {seq_time/par_time:.2f}x")

# Cache benchmark
@cache.cached(ttl=60)
def cached_function(x):
    time.sleep(0.01)
    return x * 2

# First calls
start = time.time()
for i in range(10):
    cached_function(i)
first_time = time.time() - start

# Cached calls
start = time.time()
for i in range(10):
    cached_function(i)
cached_time = time.time() - start

print(f"✓ First calls: {first_time:.3f}s")
print(f"✓ Cached calls: {cached_time:.3f}s")
print(f"✓ Cache speedup: {first_time/cached_time:.1f}x")
' || echo -e "${RED}Benchmark failed${NC}"

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
    echo "Phase 9 Production Optimization is working correctly."
    exit 0
else
    echo ""
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
    echo "Please review the failed tests above."
    exit 1
fi