import json
import time
import fakeredis
from typing import Any, Dict, List

class TelepathyBus:
    def __init__(self, use_digilang: bool = False):
        self.redis = fakeredis.FakeRedis(decode_responses=True)
        self.use_digilang = use_digilang
        self.metrics = {
            'messages_sent': 0,
            'bytes_sent': 0,
            'messages_received': 0,
            'bytes_received': 0,
            'latencies': []
        }
        
        if use_digilang:
            from ..digilang.api import serialize_message, deserialize_message
            self.serialize = serialize_message
            self.deserialize = deserialize_message
        else:
            self.serialize = lambda x: json.dumps(x)
            self.deserialize = lambda x: json.loads(x)
    
    def publish(self, channel: str, message: Any) -> float:
        """Publish message and return latency"""
        start = time.time()
        serialized = self.serialize(message)
        
        self.redis.publish(channel, serialized)
        
        latency = time.time() - start
        self.metrics['messages_sent'] += 1
        self.metrics['bytes_sent'] += len(serialized.encode('utf-8'))
        self.metrics['latencies'].append(latency)
        
        return latency
    
    def get_metrics(self) -> Dict:
        """Get telepathy metrics"""
        if self.metrics['latencies']:
            avg_latency = sum(self.metrics['latencies']) / len(self.metrics['latencies'])
            p95_latency = sorted(self.metrics['latencies'])[int(len(self.metrics['latencies']) * 0.95)]
        else:
            avg_latency = p95_latency = 0
        
        return {
            'messages_sent': self.metrics['messages_sent'],
            'bytes_sent': self.metrics['bytes_sent'],
            'avg_bytes_per_msg': self.metrics['bytes_sent'] / max(1, self.metrics['messages_sent']),
            'avg_latency_ms': avg_latency * 1000,
            'p95_latency_ms': p95_latency * 1000
        }
