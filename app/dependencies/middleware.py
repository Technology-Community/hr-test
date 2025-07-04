import logging
import time
from typing import Callable

import redis.asyncio as redis
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

from app.configs import get_app_config

logger = logging.getLogger(__name__)
config = get_app_config()


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log HTTP requests and responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log details."""
        start_time = time.time()

        # Log request
        logger.info(f"🔵 {request.method} {request.url.path}")

        # Process request
        response = await call_next(request)

        # Log response
        process_time = time.time() - start_time
        logger.info(f"🟢 {response.status_code} - {process_time:.3f}s")

        # Add timing header
        response.headers["X-Process-Time"] = str(process_time)

        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Add security headers to response."""
        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to implement rate limiting using Redis."""

    def __init__(self, app):
        super().__init__(app)
        self.redis_client: redis.Redis | None = None
        self.rate_limit = config.rate_limit
        self.window = 60  # 1 minute in seconds

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Check rate limit before processing request."""
        # Initialize Redis client on first request
        if self.redis_client is None:
            self.redis_client = redis.Redis(
                host=config.redis_host,
                port=config.redis_port,
                db=config.redis_db,
                decode_responses=True,
            )

        # Get client identifier (IP address)
        client_ip = request.client.host if request.client else "unknown"
        key = f"rate_limit:{client_ip}"

        try:
            # Get current count
            current = await self.redis_client.get(key)

            if current is None:
                # First request in window
                await self.redis_client.setex(key, self.window, 1)
                remaining = self.rate_limit - 1
            else:
                current_count = int(current)
                if current_count >= self.rate_limit:
                    # Rate limit exceeded
                    logger.warning(f"🔴 Rate limit exceeded for {client_ip}")
                    return Response(
                        content='{"success":false,"message":"Rate limit exceeded. Please try again later.","error_code":"RATE_LIMIT_EXCEEDED"}',
                        status_code=HTTP_429_TOO_MANY_REQUESTS,
                        media_type="application/json",
                        headers={
                            "X-RateLimit-Limit": str(self.rate_limit),
                            "X-RateLimit-Remaining": "0",
                            "X-RateLimit-Reset": str(self.window),
                        },
                    )
                # Increment counter
                await self.redis_client.incr(key)
                remaining = self.rate_limit - current_count - 1

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.rate_limit)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(self.window)

            return response

        except redis.RedisError as e:
            # If Redis is unavailable, log error and allow request
            logger.error(f"Redis error in rate limiting: {e}")
            return await call_next(request)
