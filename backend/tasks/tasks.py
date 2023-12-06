from celery import shared_task

from consumer.pubsub import redis_connection


@shared_task
def request_hub(link: str):
    redis_connection.publish('parser', link)
