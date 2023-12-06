from typing import List

from django.conf import settings
from django.core.cache import caches
from django.core.cache import cache as default_cache

from common.cache import BaseCacheService


class DebugCacheService(BaseCacheService):
    def clear_cache(self):
        self.cache.clear()


class RedisCacheService(BaseCacheService):

    @staticmethod
    def get_keys_from_bytes(raw_keys: List[bytes]) -> List[str]:
        """Декодирует список ключей"""
        return [key.decode('utf-8') for key in raw_keys]

    def clear_cache(self, model_name: str):
        """Очищает кэш по ключам, содержащим названия модели"""
        count, raw_keys = self.cache.scan(match=f'*{model_name}*')
        while count != 0:
            count, response = self.cache.scan(match=f'*{model_name}*')
            raw_keys += response
        keys = self.get_keys_from_bytes(raw_keys)
        self.cache.delete_many(keys)


if settings.DEVELOP:
    cache_service = DebugCacheService(cache=default_cache)
else:
    cache_service = RedisCacheService(cache=caches['redis'])
