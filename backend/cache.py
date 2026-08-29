import os
import json
import logging

logger = logging.getLogger(__name__)

_redis_client = None
_last_redis_status = "Not attempted yet"

def get_last_cache_status():
    global _last_redis_status
    return _last_redis_status

def get_redis_client():
    global _redis_client, _last_redis_status
    if _redis_client is not None:
        _last_redis_status = "Connected"
        return _redis_client

    redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    is_default_url = redis_url == 'redis://localhost:6379/0'
    
    try:
        import redis
        kwargs = {'socket_timeout': 4.0, 'decode_responses': True}
        # Configure SSL for rediss:// URLs
        if redis_url.startswith('rediss://'):
            import ssl
            kwargs['ssl_cert_reqs'] = ssl.CERT_NONE

        client = redis.from_url(redis_url, **kwargs)
        client.ping()
        _redis_client = client
        _last_redis_status = "Connected"
        logger.info("Successfully connected to Redis instance.")
        return _redis_client
    except Exception as e:
        if is_default_url:
            _last_redis_status = "REDIS_URL env variable not configured on server (using default localhost)"
        else:
            _last_redis_status = f"Redis connection failed: {str(e)}"
        logger.warning(f"Redis cache connection unavailable ({e}). Falling back to database queries.")
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
        global _last_redis_status
        _last_redis_status = f"Fetch error: {str(e)}"
        logger.warning(f"Error fetching key '{key}' from Redis cache: {e}")
        _redis_client = None
    return None

def set_cache(key: str, data: dict, ttl: int = 300):
    try:
        client = get_redis_client()
        if client:
            client.setex(key, ttl, json.dumps(data))
            return True
    except Exception as e:
        global _last_redis_status
        _last_redis_status = f"Set error: {str(e)}"
        logger.warning(f"Error setting key '{key}' in Redis cache: {e}")
        _redis_client = None
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
        global _last_redis_status
        _last_redis_status = f"Delete error: {str(e)}"
        logger.warning(f"Error invalidating cache pattern '{pattern}' in Redis: {e}")
        _redis_client = None
    return False
