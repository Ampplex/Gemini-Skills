import time
import asyncio
from collections import defaultdict
from typing import Dict, List, Optional
from fastapi import Request
from src.core.errors import TooManyRequestsException

class RateLimiter:
    """
    A simple in-memory rate limiter using a sliding window algorithm.
    """
    def __init__(self, requests_limit: int = 100, window_seconds: int = 60):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        # Maps client IP to a list of request timestamps
        self.storage: Dict[str, List[float]] = defaultdict(list)
        self._cleanup_task: Optional[asyncio.Task] = None

    async def __call__(self, request: Request):
        """
        Dependency callable for FastAPI.
        """
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        
        # Get timestamps for this IP
        timestamps = self.storage[client_ip]
        
        # Remove timestamps outside the current window (sliding window)
        while timestamps and timestamps[0] < now - self.window_seconds:
            timestamps.pop(0)
        
        # Check if limit exceeded
        if len(timestamps) >= self.requests_limit:
            raise TooManyRequestsException(
                detail=f"Rate limit exceeded. Maximum {self.requests_limit} requests per {self.window_seconds} seconds."
            )
        
        # Add current request timestamp
        timestamps.append(now)
        return True

    async def _cleanup_loop(self):
        """
        Background loop to prune old data from memory.
        """
        try:
            while True:
                await asyncio.sleep(self.window_seconds)
                now = time.time()
                ips_to_remove = []
                
                # Iterate over a copy of keys to avoid modification during iteration
                for ip in list(self.storage.keys()):
                    timestamps = self.storage[ip]
                    while timestamps and timestamps[0] < now - self.window_seconds:
                        timestamps.pop(0)
                    
                    if not timestamps:
                        ips_to_remove.append(ip)
                
                for ip in ips_to_remove:
                    # Double check if it's still empty to avoid race conditions with new requests
                    if not self.storage[ip]:
                        del self.storage[ip]
        except asyncio.CancelledError:
            pass

    def start_cleanup(self):
        """
        Starts the background cleanup task.
        """
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())

    def stop_cleanup(self):
        """
        Stops the background cleanup task.
        """
        if self._cleanup_task:
            self._cleanup_task.cancel()
            self._cleanup_task = None

# Global instance for easy use as a dependency
limiter = RateLimiter(requests_limit=100, window_seconds=60)
