import os
import json
import logging

logger = logging.getLogger(__name__)

_redis_client = None
_redis_attempted = False

def get_redis_client():
    global _redis_client, _redis_attempted
    if _redis_client is not None:
        return _redis_client
    if _redis_attempted:
        return None

    _redis_attempted = True
    redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    try:
        import redis
        client = redis.from_url(redis_url, socket_timeout=2.0, decode_responses=True)
        # Ping to test connection
        client.ping()
        _redis_client = client
        logger.info("Successfully connected to Redis cache instance.")
        return _redis_client
    except Exception as e:
        logger.warning(f"Redis cache unavailable ({e}). Falling back to database queries.")
        _redis_client = None
        return None

def get_cache(key: str):
    try:
        client = get_redis_client()
        if client:
            val = client.get(key)
            if val:
                return json.loads(val)
    except Exception as e:
        logger.warning(f"Error fetching key '{key}' from Redis cache: {e}")
    return None

def set_cache(key: str, data: dict, ttl: int = 300):
    try:
        client = get_redis_client()
        if client:
            client.setex(key, ttl, json.dumps(data))
            return True
    except Exception as e:
        logger.warning(f"Error setting key '{key}' in Redis cache: {e}")
    return False

def delete_cache_pattern(pattern: str):
    try:
        client = get_redis_client()
        if client:
            keys = client.keys(pattern)
            if keys:
                client.delete(*keys)
            return True
    except Exception as e:
        logger.warning(f"Error invalidating cache pattern '{pattern}' in Redis: {e}")
    return False
