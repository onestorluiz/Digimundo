#!/usr/bin/env python3
"""
V3.1 - Redis Pub/Sub throughput test
"""
import json
import time
import os
from pathlib import Path
import threading

def test_pubsub(num_messages=1000):
    """Test Redis pub/sub throughput"""
    import redis
    
    url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    r = redis.Redis.from_url(url, socket_connect_timeout=0.5)
    
    # Setup subscriber in thread
    received = []
    
    def subscriber():
        ps = r.pubsub()
        ps.subscribe('test_channel')
        count = 0
        for msg in ps.listen():
            if msg['type'] == 'message':
                received.append(time.perf_counter())
                count += 1
                if count >= num_messages:
                    break
        ps.unsubscribe('test_channel')
    
    # Start subscriber
    sub_thread = threading.Thread(target=subscriber)
    sub_thread.start()
    time.sleep(0.5)  # Let subscriber setup
    
    # Publish messages
    start = time.perf_counter()
    sent_times = []
    
    for i in range(num_messages):
        t = time.perf_counter()
        r.publish('test_channel', f'msg_{i}')
        sent_times.append(t)
    
    # Wait for subscriber
    sub_thread.join(timeout=5)
    
    # Calculate metrics
    if len(received) > 0:
        latencies = [(received[i] - sent_times[i]) * 1000 for i in range(min(len(received), len(sent_times)))]
        latencies.sort()
        
        p95_idx = int(len(latencies) * 0.95)
        p99_idx = int(len(latencies) * 0.99)
        
        total_time = received[-1] - sent_times[0]
        msgs_per_sec = len(received) / total_time if total_time > 0 else 0
        
        return {
            "ok": True,
            "messages_sent": num_messages,
            "messages_received": len(received),
            "avg_latency_ms": round(sum(latencies) / len(latencies), 3),
            "p95_latency_ms": round(latencies[p95_idx] if p95_idx < len(latencies) else latencies[-1], 3),
            "p99_latency_ms": round(latencies[p99_idx] if p99_idx < len(latencies) else latencies[-1], 3),
            "msgs_per_sec": round(msgs_per_sec, 1),
            "within_budget": latencies[p95_idx] < 10 if p95_idx < len(latencies) else False
        }
    else:
        return {
            "ok": False,
            "error": "No messages received"
        }

def main():
    output_path = Path("reports/fix_v3/real_run/telepathy_pubsub_v31.json")
    
    try:
        result = test_pubsub()
    except Exception as e:
        result = {"ok": False, "error": str(e)}
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2))
    print(f"[telepathy_pubsub] gravado: {output_path}")

if __name__ == "__main__":
    main()