from celery import shared_task

from services.cache import cache_service


@shared_task
def clear_cache(model_name: str) -> None:
    """Задача на очищение кэша"""
    cache_service.clear_cache(model_name)
