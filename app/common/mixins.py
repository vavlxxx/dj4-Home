from typing import Any
from django.core.cache import cache


class CacheMixin:
    def set_get_cache(
        self,
        query: Any,
        key: Any,
        ttl: int,
    ):
        data = cache.get(key)
        if not data:
            data = query
            cache.set(key, data, ttl)
        return data
