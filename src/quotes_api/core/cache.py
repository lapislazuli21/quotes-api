import redis.asyncio as redis

from .config import get_settings

# Create an async connection pool

pool = redis.ConnectionPool.from_url(get_settings().valkey_url, decode_responses=True)

def get_cache():
    """
        FastAPI dependency that provides a Valkey/Redis client
        from the connection pool.
        """
    return redis.Redis.from_pool(pool)