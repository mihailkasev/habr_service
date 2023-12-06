from abc import ABC, abstractmethod
from typing import Union

from django.core.cache.backends.redis import RedisCache
from django.utils.connection import ConnectionProxy
from redis.typing import PatternT


class CustomRedisCache(RedisCache):
    """Бекэнд для кэширования с методом удаления множества ключей по match"""
    def delete_many(self, keys, version=None):
        """Удаляет множество ключей"""
        if not keys:
            return
        self._cache.delete_many(keys)

    def scan(self, cursor: int = 0, match: Union[PatternT, None] = None, **kwargs):
        """Итерирует по коллекции ключей, совпадающих по match"""
        client = self._cache.get_client()
        return client.scan(match=match, count=1000, **kwargs)


class BaseCacheService(ABC):
    """Базовый сервис для управления кэшем"""
    def __init__(self, cache: ConnectionProxy):
        self.cache = cache

    @staticmethod
    def make_hash_for_query_params(query_params: dict) -> str:
        """Создает хэш для параметров запроса"""
        return str(hash(frozenset(query_params.items())))

    def make_cache_key(self, model_name: str, query_params: dict = None, pk: str = None) -> str:
        """Создает ключ в кэше на основе названия модели и параметров запроса"""
        if query_params:
            url_hash = self.make_hash_for_query_params(query_params)
            model_name += f"_{url_hash}"
        if pk:
            model_name += f"_{pk}"
        return model_name

    @abstractmethod
    def clear_cache(self, *args, **kwargs) -> None:
        """Очищает кэш"""
        ...
