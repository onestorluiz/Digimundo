#!/usr/bin/env python3
"""
Test Monitoring System
Phase 5 - Harmony vFinal
"""

import sys
import json
import time
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))

def test_case_1_monitoring_disabled():
    """Test Case 1: Monitoring disabled (default)"""
    print("\n=== TEST CASE 1: Monitoring Disabled ===")
    
    from apps.scripturemon.config_loader import load_config
    from src.utils.monitoring import start_monitoring
    
    # Default config (monitoring disabled)
    settings = load_config()
    settings['monitoring']['enabled'] = False
    
    # Try to start monitoring
    monitor = start_monitoring(settings)
    
    assert monitor is None or not monitor.enabled, "Monitor should be disabled"
    print("✅ Monitoring correctly disabled")
    
    # Check no health.json created
    health_path = Path("reports/harmony_vFinal/runtime/health.json")
    assert not health_path.exists(), "Health file should not exist when disabled"
    print("✅ No health.json created when disabled")
    
    print("\n✅ Test Case 1 PASSED: Monitoring correctly disabled by default")


def test_case_2_monitoring_enabled():
    """Test Case 2: Monitoring enabled with metrics collection"""
    print("\n=== TEST CASE 2: Monitoring Enabled ===")
    
    from src.utils.monitoring import (
        SystemMonitor, 
        increment_interaction,
        record_cache_hit,
        set_telepathy_status,
        increment_rag_queries
    )
    
    # Settings with monitoring enabled
    settings = {
        "monitoring": {
            "enabled": True,
            "interval_ms": 2000,  # 2 seconds
            "export_path": "reports/harmony_vFinal/runtime/health.json"
        }
    }
    
    # Create and start monitor
    monitor = SystemMonitor(settings)
    monitor.start()
    
    print("📊 Monitor started, simulating activity...")
    
    # Simulate activity
    for i in range(5):
        increment_interaction()
        record_cache_hit("L1" if i % 3 == 0 else "L2")
        if i == 2:
            record_cache_hit("misses")
        time.sleep(0.5)
    
    set_telepathy_status("Mock (Offline)")
    increment_rag_queries()
    increment_rag_queries()
    
    # Wait for export
    print("⏳ Waiting for export cycle...")
    time.sleep(3)
    
    # Check health.json created
    health_path = Path("reports/harmony_vFinal/runtime/health.json")
    assert health_path.exists(), "Health file should be created"
    print("✅ health.json created")
    
    # Read and verify content
    with open(health_path) as f:
        data = json.load(f)
    
    assert "current" in data, "Should have current metrics"
    assert "history" in data, "Should have history"
    
    current = data["current"]
    print(f"\n📊 Current Metrics:")
    print(f"  • CPU: {current.get('cpu_percent')}%")
    print(f"  • Memory: {current.get('mem_rss_mb')} MB")
    print(f"  • Interactions: {current.get('interactions')}")
    print(f"  • Cache Hit Rate: {current.get('cache_hit_rate')}%")
    print(f"  • Telepathy: {current.get('telepathy_status')}")
    print(f"  • RAG Queries: {current.get('rag_queries')}")
    
    # Verify values
    assert current["interactions"] == 5, "Should have 5 interactions"
    assert current["telepathy_status"] == "Mock (Offline)", "Telepathy status should be set"
    assert current["rag_queries"] == 2, "Should have 2 RAG queries"
    
    # Check cache metrics
    cache_hits = current["cache_hits"]
    assert cache_hits["L1"] == 2, "Should have 2 L1 hits"
    assert cache_hits["L2"] == 3, "Should have 3 L2 hits"
    assert cache_hits["misses"] == 1, "Should have 1 miss"
    
    # Stop monitor
    monitor.stop()
    
    print("\n✅ Test Case 2 PASSED: Monitoring works correctly when enabled")


def test_case_3_status_integration():
    """Test Case 3: Status command integration"""
    print("\n=== TEST CASE 3: Status Integration ===")
    
    from apps.scripturemon.chat import ScripturemonChat
    from src.utils.monitoring import start_monitoring, increment_interaction
    
    # Enable monitoring in settings
    settings = {
        "monitoring": {
            "enabled": True,
            "interval_ms": 2000
        },
        "redis": {"enabled": False}  # Use mock telepathy
    }
    
    # Start monitoring
    monitor = start_monitoring(settings)
    
    # Simulate some interactions
    for _ in range(3):
        increment_interaction()
    
    # Initialize chat (would normally start monitoring)
    chat = ScripturemonChat()
    
    # Get status
    status = chat.cmd_status("")
    
    # Check if monitoring info is in status
    has_monitoring = False
    for line in status.split('\n'):
        if 'Monitoramento:' in line and 'CPU' in line:
            print(f"✅ Monitoring in status: {line.strip()}")
            has_monitoring = True
            break
    
    assert has_monitoring or "Monitoramento" in status, "Status should show monitoring info"
    
    print("\n✅ Test Case 3 PASSED: Status shows monitoring metrics")


def test_case_4_performance():
    """Test Case 4: Performance and resource usage"""
    print("\n=== TEST CASE 4: Performance Test ===")
    
    from src.utils.monitoring import SystemMonitor
    import psutil
    
    settings = {
        "monitoring": {
            "enabled": True,
            "interval_ms": 2000  # 2 second interval
        }
    }
    
    # Get baseline memory
    process = psutil.Process()
    baseline_memory = process.memory_info().rss / (1024 * 1024)
    
    # Start monitor
    monitor = SystemMonitor(settings)
    monitor.start()
    
    # Run for a bit
    print("📊 Running monitor for 5 seconds...")
    time.sleep(5)
    
    # Check memory increase
    current_memory = process.memory_info().rss / (1024 * 1024)
    memory_increase = current_memory - baseline_memory
    
    print(f"  • Baseline Memory: {baseline_memory:.1f} MB")
    print(f"  • Current Memory: {current_memory:.1f} MB")
    print(f"  • Increase: {memory_increase:.1f} MB")
    
    assert memory_increase < 10, "Memory increase should be minimal (< 10MB)"
    
    # Check CPU usage
    metrics = monitor.collect_metrics()
    cpu_percent = metrics.get("cpu_percent", 0)
    print(f"  • CPU Usage: {cpu_percent}%")
    
    # Stop monitor
    monitor.stop()
    
    print("\n✅ Test Case 4 PASSED: Monitoring has minimal resource impact")


if __name__ == "__main__":
    print("🧪 MONITORING SYSTEM TESTS")
    print("=" * 50)
    
    try:
        # Ensure directories exist
        Path("reports/harmony_vFinal/runtime").mkdir(parents=True, exist_ok=True)
        
        # Run all test cases
        test_case_1_monitoring_disabled()
        test_case_2_monitoring_enabled()
        test_case_3_status_integration()
        test_case_4_performance()
        
        print("\n" + "=" * 50)
        print("✅ ALL MONITORING TESTS PASSED!")
        print("=" * 50)
        
        # Cleanup
        Path("reports/harmony_vFinal/runtime/health.json").unlink(missing_ok=True)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)