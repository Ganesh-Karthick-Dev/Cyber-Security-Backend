from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import time
from typing import Dict, Tuple
from app.core.config import settings
from app.utils.responses import APIResponse


class RateLimiter:
    """
    Rate limiting middleware - similar to Express.js rate limiting
    Prevents API abuse and DDoS attacks
    """
    
    def __init__(self, requests_per_window: int = None, window_seconds: int = None):
        self.requests_per_window = requests_per_window or settings.rate_limit_requests
        self.window_seconds = window_seconds or settings.rate_limit_window
        self.clients: Dict[str, Tuple[int, float]] = {}  # {ip: (request_count, window_start)}
    
    def is_allowed(self, client_ip: str) -> bool:
        """Check if client is allowed to make request"""
        current_time = time.time()
        
        if client_ip not in self.clients:
            self.clients[client_ip] = (1, current_time)
            return True
        
        request_count, window_start = self.clients[client_ip]
        
        # Check if window has expired
        if current_time - window_start >= self.window_seconds:
            self.clients[client_ip] = (1, current_time)
            return True
        
        # Check if within rate limit
        if request_count < self.requests_per_window:
            self.clients[client_ip] = (request_count + 1, window_start)
            return True
        
        return False
    
    def get_client_ip(self, request: Request) -> str:
        """Extract client IP from request"""
        # Check for forwarded IP first (behind proxy)
        forwarded_ip = request.headers.get("X-Forwarded-For")
        if forwarded_ip:
            return forwarded_ip.split(",")[0].strip()
        
        # Check for real IP header
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fall back to client host
        return request.client.host if request.client else "unknown"


# Global rate limiter instance
rate_limiter = RateLimiter()


async def rate_limit_middleware(request: Request, call_next):
    """
    Rate limiting middleware function
    Add this to your FastAPI app to enable rate limiting
    """
    client_ip = rate_limiter.get_client_ip(request)
    
    if not rate_limiter.is_allowed(client_ip):
        return APIResponse.error(
            message="Rate limit exceeded. Please try again later.",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )
    
    response = await call_next(request)
    return response