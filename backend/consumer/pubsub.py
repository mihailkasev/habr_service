import json
import time
import redis
from redis.client import PubSub
from django.conf import settings

from hubs.services import create_articles


def reader(channel: PubSub):
    """Прослушивает заданный канал и обрабатывает сообщения"""
    while True:
        message = channel.get_message(ignore_subscribe_messages=True)
        if message:
            decoded_message = json.loads(message.get('data'))
            create_articles(decoded_message)
        time.sleep(0.001)


redis_connection = redis.Redis(settings.REDIS['host'], settings.REDIS['port'])
pubsub = redis_connection.pubsub()
pubsub.subscribe('backend')
