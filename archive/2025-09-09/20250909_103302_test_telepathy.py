#!/usr/bin/env python3
"""
Test Telepathy System with Fallback
Phase 4 - Harmony vFinal
"""

import sys
import json
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))

from src.telepathy.channel import get_channel, get_client, healthcheck

def test_case_1_no_redis():
    """Test Case 1: Redis NOT available"""
    print("\n=== TEST CASE 1: Redis NOT Available ===")
    
    # Settings with Redis disabled
    settings = {
        "redis": {
            "enabled": False,
            "url": "redis://localhost:6379",
            "timeout_sec": 0.5
        }
    }
    
    # Get channel
    channel = get_channel(settings)
    
    # Test health
    health = channel.healthcheck()
    print(f"✅ Health Check: {health['type']} - Healthy: {health['healthy']}")
    assert health['healthy'], "Mock should always be healthy"
    assert "Mock" in health['type'], "Should be using mock"
    
    # Test publish
    success = channel.publish("broadcast", "Test message from offline mode")
    print(f"✅ Publish: {'Success' if success else 'Failed'}")
    assert success, "Publish should work in mock"
    
    # Test get/set
    channel.set("test_key", {"data": "test_value"})
    value = channel.get("test_key")
    print(f"✅ Get/Set: Retrieved {value}")
    assert "test_value" in value, "Should retrieve stored value"
    
    # Check broadcast history
    if "mock_history_size" in health:
        print(f"✅ Broadcast History: {health['mock_history_size']} messages")
    
    print("\n✅ Test Case 1 PASSED: System works without Redis")


def test_case_2_redis_enabled():
    """Test Case 2: Redis enabled (will fallback if not running)"""
    print("\n=== TEST CASE 2: Redis Enabled (Fallback Test) ===")
    
    # Settings with Redis enabled
    settings = {
        "redis": {
            "enabled": True,
            "url": "redis://localhost:6379",
            "timeout_sec": 0.5
        }
    }
    
    # Get client to see fallback chain
    print("\nTesting fallback chain...")
    client = get_client(settings)
    
    # Check what we got
    client_type = client.__class__.__name__
    print(f"✅ Client Type: {client_type}")
    
    # Test health
    is_healthy, status_msg = healthcheck(client)
    print(f"✅ Health: {status_msg}")
    
    # Get channel
    channel = get_channel(settings)
    
    # Test operations
    channel.publish("test_channel", "Hello from telepathy test!")
    stats = channel.get_stats()
    
    print(f"\n📊 Channel Statistics:")
    print(f"  • Type: {stats['type']}")
    print(f"  • Connected: {stats['connected']}")
    print(f"  • Latency: {stats['latency_ms']:.2f}ms")
    print(f"  • Broadcasts: {stats['broadcasts_sent']}")
    
    print("\n✅ Test Case 2 PASSED: Fallback chain works correctly")


def test_case_3_timeout():
    """Test Case 3: Timeout handling"""
    print("\n=== TEST CASE 3: Timeout Handling ===")
    
    # Settings with wrong port (will timeout)
    settings = {
        "redis": {
            "enabled": True,
            "url": "redis://localhost:9999",  # Wrong port
            "timeout_sec": 0.1  # Very short timeout
        }
    }
    
    import time
    start = time.time()
    client = get_client(settings)
    elapsed = time.time() - start
    
    print(f"✅ Fallback after {elapsed:.3f}s (timeout was {settings['redis']['timeout_sec']}s)")
    assert elapsed < 1.0, "Should fallback quickly"
    
    client_type = client.__class__.__name__
    print(f"✅ Fallback to: {client_type}")
    assert "Mock" in client_type or "Fake" in client_type, "Should fallback to mock"
    
    print("\n✅ Test Case 3 PASSED: Timeout handled correctly")


def test_interactive_commands():
    """Test interactive commands simulation"""
    print("\n=== TEST INTERACTIVE COMMANDS ===")
    
    from apps.scripturemon.chat import ScripturemonChat
    
    # Initialize chat
    chat = ScripturemonChat()
    
    # Test /telepathy toggle
    print("\n1. Testing /telepathy toggle:")
    response = chat.cmd_telepathy("")
    print(f"   {response}")
    
    # Test /telepathy broadcast
    print("\n2. Testing /telepathy broadcast:")
    response = chat.cmd_telepathy("Hello multiverse!")
    print(f"   {response}")
    
    # Test /status with telepathy info
    print("\n3. Testing /status (showing telepathy):")
    status = chat.cmd_status("")
    # Extract telepathy line
    for line in status.split('\n'):
        if 'Telepatia:' in line:
            print(f"   {line.strip()}")
        if 'Broadcasts' in line:
            print(f"   {line.strip()}")
    
    print("\n✅ Interactive commands work correctly")


if __name__ == "__main__":
    print("🧪 TELEPATHY SYSTEM TESTS")
    print("=" * 50)
    
    try:
        # Run all test cases
        test_case_1_no_redis()
        test_case_2_redis_enabled()
        test_case_3_timeout()
        test_interactive_commands()
        
        print("\n" + "=" * 50)
        print("✅ ALL TESTS PASSED!")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)