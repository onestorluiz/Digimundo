"""
⚡🛡️ RATE LIMITER SUPREME - SILICON VALLEY GRADE
Advanced rate limiting for distributed orchestration with multiple algorithms
and perfect harmony with Script Doctor systems.
"""
import asyncio
import time
import logging
from typing import Dict, Optional, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
import hashlib
import redis
from threading import Lock
logger = logging.getLogger(__name__)

class RateLimitAlgorithm(Enum):
    """Rate limiting algorithms"""
    TOKEN_BUCKET = 'token_bucket'
    LEAKY_BUCKET = 'leaky_bucket'
    SLIDING_WINDOW = 'sliding_window'
    FIXED_WINDOW = 'fixed_window'
    ADAPTIVE = 'adaptive'

@dataclass
class RateLimitConfig:
    """Rate limit configuration"""
    requests_per_second: float = 100.0
    burst_size: int = 200
    window_size: float = 60.0
    algorithm: RateLimitAlgorithm = RateLimitAlgorithm.TOKEN_BUCKET
    distributed: bool = False
    redis_host: str = 'localhost'
    redis_port: int = 6379

class TokenBucket:
    """Token bucket algorithm implementation"""

    def __init__(self, rate: float, capacity: int):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = Lock()

    def consume(self, tokens: int=1) -> bool:
        """Try to consume tokens"""
        with self.lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    def _refill(self):
        """Refill bucket based on time passed"""
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now

class LeakyBucket:
    """Leaky bucket algorithm implementation"""

    def __init__(self, rate: float, capacity: int):
        self.rate = rate
        self.capacity = capacity
        self.queue = deque()
        self.last_leak = time.time()
        self.lock = Lock()

    def add_request(self, request_id: str) -> bool:
        """Add request to bucket"""
        with self.lock:
            self._leak()
            if len(self.queue) < self.capacity:
                self.queue.append((request_id, time.time()))
                return True
            return False

    def _leak(self):
        """Leak requests from bucket"""
        now = time.time()
        elapsed = now - self.last_leak
        requests_to_leak = int(elapsed * self.rate)
        for _ in range(min(requests_to_leak, len(self.queue))):
            if self.queue:
                self.queue.popleft()
        self.last_leak = now

class SlidingWindow:
    """Sliding window algorithm implementation"""

    def __init__(self, window_size: float, max_requests: int):
        self.window_size = window_size
        self.max_requests = max_requests
        self.requests = deque()
        self.lock = Lock()

    def allow_request(self) -> bool:
        """Check if request is allowed"""
        with self.lock:
            now = time.time()
            window_start = now - self.window_size
            while self.requests and self.requests[0] < window_start:
                self.requests.popleft()
            if len(self.requests) < self.max_requests:
                self.requests.append(now)
                return True
            return False

class RateLimiterSupreme:
    """
    Supreme rate limiter with multiple algorithms and distributed support.
    Perfect harmony with Script Doctor consciousness.
    """

    def __init__(self, config: Optional[RateLimitConfig]=None):
        self.config = config or RateLimitConfig()
        self.algorithm = self.config.algorithm
        self.limiters: Dict[str, any] = {}
        self.total_requests = 0
        self.rejected_requests = 0
        self.client_stats = defaultdict(lambda: {'allowed': 0, 'rejected': 0})
        self.redis_client = None
        if self.config.distributed:
            try:
                self.redis_client = redis.Redis(host=self.config.redis_host, port=self.config.redis_port, decode_responses=True)
                self.redis_client.ping()
                logger.info('🔗 Connected to Redis for distributed rate limiting')
            except Exception as e:
                logger.warning(f'⚠️ Redis connection failed: {e}. Using local rate limiting.')
                self.redis_client = None
        logger.info(f'⚡ RateLimiterSupreme initialized with {self.algorithm.value} algorithm')

    def _get_limiter(self, client_id: str):
        """Get or create limiter for client"""
        if client_id not in self.limiters:
            if self.algorithm == RateLimitAlgorithm.TOKEN_BUCKET:
                self.limiters[client_id] = TokenBucket(self.config.requests_per_second, self.config.burst_size)
            elif self.algorithm == RateLimitAlgorithm.LEAKY_BUCKET:
                self.limiters[client_id] = LeakyBucket(self.config.requests_per_second, self.config.burst_size)
            elif self.algorithm == RateLimitAlgorithm.SLIDING_WINDOW:
                self.limiters[client_id] = SlidingWindow(self.config.window_size, int(self.config.requests_per_second * self.config.window_size))
            else:
                self.limiters[client_id] = TokenBucket(self.config.requests_per_second, self.config.burst_size)
        return self.limiters[client_id]

    async def check_rate_limit(self, client_id: str, tokens: int=1) -> Tuple[bool, Optional[float]]:
        """
        Check if request is within rate limit.
        Returns (allowed, retry_after_seconds)
        """
        self.total_requests += 1
        if self.redis_client:
            allowed = await self._check_distributed(client_id, tokens)
        else:
            allowed = self._check_local(client_id, tokens)
        if allowed:
            self.client_stats[client_id]['allowed'] += 1
        else:
            self.rejected_requests += 1
            self.client_stats[client_id]['rejected'] += 1
        retry_after = None
        if not allowed:
            retry_after = 1.0 / self.config.requests_per_second
        return (allowed, retry_after)

    def _check_local(self, client_id: str, tokens: int) -> bool:
        """Check rate limit locally"""
        limiter = self._get_limiter(client_id)
        if self.algorithm == RateLimitAlgorithm.TOKEN_BUCKET:
            return limiter.consume(tokens)
        elif self.algorithm == RateLimitAlgorithm.LEAKY_BUCKET:
            request_id = f'{client_id}:{time.time()}'
            return limiter.add_request(request_id)
        elif self.algorithm == RateLimitAlgorithm.SLIDING_WINDOW:
            return limiter.allow_request()
        else:
            return True

    def _check_distributed(self, client_id: str, tokens: int) -> bool:
        """Check rate limit using Redis for distribution"""
        try:
            key = f'rate_limit:{client_id}'
            pipe = self.redis_client.pipeline()
            if self.algorithm == RateLimitAlgorithm.SLIDING_WINDOW:
                now = time.time()
                window_start = now - self.config.window_size
                pipe.zremrangebyscore(key, 0, window_start)
                pipe.zcard(key)
                pipe.zadd(key, {str(now): now})
                pipe.expire(key, int(self.config.window_size) + 1)
                results = pipe.execute()
                count = results[1]
                max_requests = int(self.config.requests_per_second * self.config.window_size)
                return count < max_requests
            else:
                current = self.redis_client.get(key)
                if current is None:
                    self.redis_client.setex(key, int(self.config.window_size), self.config.burst_size)
                    return True
                current_tokens = int(current)
                if current_tokens >= tokens:
                    self.redis_client.decrby(key, tokens)
                    return True
                return False
        except Exception as e:
            logger.error(f'❌ Distributed rate limit check failed: {e}')
            return self._check_local(client_id, tokens)

    def get_statistics(self) -> Dict:
        """Get rate limiter statistics"""
        return {'total_requests': self.total_requests, 'rejected_requests': self.rejected_requests, 'rejection_rate': self.rejected_requests / max(1, self.total_requests), 'active_clients': len(self.client_stats), 'algorithm': self.algorithm.value, 'distributed': self.redis_client is not None, 'client_stats': dict(self.client_stats)}

    def reset_client(self, client_id: str):
        """Reset rate limit for specific client"""
        if client_id in self.limiters:
            del self.limiters[client_id]
        if self.redis_client:
            key = f'rate_limit:{client_id}'
            self.redis_client.delete(key)
        if client_id in self.client_stats:
            del self.client_stats[client_id]
        logger.info(f'🔄 Reset rate limit for client: {client_id}')

    def adaptive_adjust(self):
        """Adaptively adjust rate limits based on system load"""
        if self.algorithm != RateLimitAlgorithm.ADAPTIVE:
            return
        rejection_rate = self.rejected_requests / max(1, self.total_requests)
        if rejection_rate > 0.2:
            self.config.requests_per_second *= 1.1
            self.config.burst_size = int(self.config.burst_size * 1.1)
            logger.info(f'📈 Increased rate limits: {self.config.requests_per_second:.1f} req/s')
        elif rejection_rate < 0.05:
            self.config.requests_per_second *= 0.95
            self.config.burst_size = int(self.config.burst_size * 0.95)
            logger.info(f'📉 Decreased rate limits: {self.config.requests_per_second:.1f} req/s')

class RateLimitedOrchestrator:
    """Rate limited wrapper for distributed orchestration"""

    def __init__(self, orchestrator, rate_limiter: RateLimiterSupreme):
        self.orchestrator = orchestrator
        self.rate_limiter = rate_limiter

    async def submit_task(self, client_id: str, task_name: str, *args, **kwargs):
        """Submit task with rate limiting"""
        allowed, retry_after = await self.rate_limiter.check_rate_limit(client_id)
        if not allowed:
            raise Exception(f'Rate limit exceeded. Retry after {retry_after:.1f} seconds')
        return await self.orchestrator.submit_task(task_name, *args, **kwargs)

async def test_rate_limiter():
    """Test rate limiter functionality"""
    logger.info('🧪 Testing RateLimiterSupreme...')
    config = RateLimitConfig(requests_per_second=10, burst_size=15, algorithm=RateLimitAlgorithm.TOKEN_BUCKET)
    limiter = RateLimiterSupreme(config)
    clients = ['client_1', 'client_2', 'client_3']
    results = {'allowed': 0, 'rejected': 0}
    for _ in range(50):
        for client in clients:
            allowed, retry = await limiter.check_rate_limit(client)
            if allowed:
                results['allowed'] += 1
            else:
                results['rejected'] += 1
        await asyncio.sleep(0.05)
    stats = limiter.get_statistics()
    logger.info(f'✅ Test complete:')
    logger.info(f"  Allowed: {results['allowed']}")
    logger.info(f"  Rejected: {results['rejected']}")
    logger.info(f"  Rejection rate: {stats['rejection_rate']:.1%}")
    return stats
if __name__ == '__main__':
    asyncio.run(test_rate_limiter())
    logger.info('⚡ RateLimiterSupreme implementation complete!')