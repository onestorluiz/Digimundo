"""
Telepathy Network - Redis pub/sub with robust fallback
Auto-fixed for production reliability
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

# Try to import Redis, fallback to mock if unavailable
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available, using in-memory fallback")

class TelepathyNetwork:
    """Telepathy network with automatic fallback"""
    
    def __init__(self):
        self.redis_client = None
        self.fallback_store = {}  # In-memory fallback
        self._init_redis()
    
    def _init_redis(self):
        """Initialize Redis connection with fallback - FASE 3 adaptive mode"""
        self.mode = "offline"  # Default to offline
        self.redis_url = None
        self.fallback_reason = None
        
        if not REDIS_AVAILABLE:
            logger.warning("Redis module not available, using in-memory telepathy fallback")
            self.fallback_reason = "Redis module not installed"
            return
        
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        try:
            self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
            # Test connection
            self.redis_client.ping()
            self.mode = "redis"
            logger.info(f"✅ Telepathy Network: ONLINE ({self.redis_url})")
        except Exception as e:
            logger.warning(f"⚠️ Redis connection failed: {e}, using offline fallback")
            self.redis_client = None
            self.mode = "offline"
            self.fallback_reason = str(e)
    
    def publish(self, channel: str, data: Dict[Any, Any]) -> bool:
        """Publish message with fallback"""
        try:
            message = json.dumps(data)
            
            if self.redis_client:
                self.redis_client.publish(channel, message)
                return True
            else:
                # Fallback: store in memory
                if channel not in self.fallback_store:
                    self.fallback_store[channel] = []
                self.fallback_store[channel].append({
                    "data": data,
                    "timestamp": datetime.utcnow().isoformat()
                })
                # Keep only last 100 messages per channel
                self.fallback_store[channel] = self.fallback_store[channel][-100:]
                return True
                
        except Exception as e:
            logger.error(f"Publish failed: {e}")
            return False
    
    def subscribe(self, channel: str):
        """Subscribe to channel with fallback"""
        if self.redis_client:
            pubsub = self.redis_client.pubsub()
            pubsub.subscribe(channel)
            return pubsub
        else:
            # Return mock pubsub for fallback
            return MockPubSub(self.fallback_store, channel)
    
    def get_status(self) -> Dict[str, Any]:
        """Get telepathy network status - FASE 3 enhanced"""
        status = {
            "mode": self.mode,
            "redis_available": REDIS_AVAILABLE,
            "redis_connected": self.redis_client is not None,
            "fallback_active": self.redis_client is None,
            "fallback_channels": list(self.fallback_store.keys()) if self.fallback_store else []
        }
        
        # Add URL or reason based on mode
        if self.mode == "redis":
            status["url"] = self.redis_url
        else:
            status["reason"] = self.fallback_reason or "Redis not available"
        
        return status
    
    def get_active_peers(self) -> List[str]:
        """Get list of active peers - FASE 5 requirement"""
        # In offline mode, no real peers
        if self.mode == "offline":
            return []
        
        # In Redis mode, simulate peer discovery
        # (In production, this would query actual peer registry)
        return ["localhost:6379"] if self.mode == "redis" else []

class MockPubSub:
    """Mock PubSub for fallback mode"""
    
    def __init__(self, store: Dict, channel: str):
        self.store = store
        self.channel = channel
        self.index = 0
    
    def listen(self):
        """Mock listen generator"""
        while True:
            if self.channel in self.store and self.index < len(self.store[self.channel]):
                msg = self.store[self.channel][self.index]
                self.index += 1
                yield {
                    "type": "message",
                    "channel": self.channel,
                    "data": json.dumps(msg["data"])
                }
            else:
                yield {"type": "ping"}

# Singleton instance
_telepathy = None

def get_telepathy() -> TelepathyNetwork:
    """Get singleton telepathy instance"""
    global _telepathy
    if _telepathy is None:
        _telepathy = TelepathyNetwork()
    return _telepathy
