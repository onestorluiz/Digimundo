#!/usr/bin/env python3
"""
Test Telepathy Event Emitter
"""
import json
import os
import time
from pathlib import Path
from datetime import datetime

def test_telepathy():
    """Test Redis telepathy if available"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "redis_ok": False,
        "events_emitted": 0,
        "fallback": False,
        "errors": []
    }
    
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    
    try:
        import redis
        
        # Parse Redis URL
        if redis_url.startswith("redis://"):
            parts = redis_url.replace("redis://", "").split(":")
            host = parts[0]
            port = int(parts[1].split("/")[0]) if len(parts) > 1 else 6379
        else:
            host = "localhost"
            port = 6379
        
        # Connect with short timeout
        client = redis.Redis(
            host=host,
            port=port,
            decode_responses=True,
            socket_connect_timeout=0.5,
            socket_timeout=0.5
        )
        
        # Test connection
        client.ping()
        results["redis_ok"] = True
        
        # Emit test events
        events = [
            {"type": "memory_promoted", "mem": "test_123", "level": "L2"},
            {"type": "rag_cite", "doc": "test.pdf", "chunk": 5}
        ]
        
        for event in events:
            try:
                # Compact event
                compact_event = json.dumps(event, separators=(',', ':'))
                
                # Publish to channel
                client.publish("telepathy:events", compact_event)
                results["events_emitted"] += 1
                
                # Also use stream for persistence
                client.xadd(
                    "telepathy:stream",
                    {"event": compact_event},
                    maxlen=1000  # Keep last 1000 events
                )
                
            except Exception as e:
                results["errors"].append(f"Event emit error: {str(e)}")
        
    except ImportError:
        results["fallback"] = True
        results["errors"].append("Redis module not available")
        
    except Exception as e:
        results["fallback"] = True
        results["errors"].append(f"Redis connection failed: {str(e)}")
    
    # Save results
    output_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/reports/integrate_align_v32")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "telemetry.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Telepathy test: {'✅' if results['redis_ok'] else '❌'}")
    print(f"  Events emitted: {results['events_emitted']}")
    print(f"  Fallback: {results['fallback']}")
    
    return results

if __name__ == "__main__":
    test_telepathy()