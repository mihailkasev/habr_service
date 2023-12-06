import asyncio

from redis import asyncio as aioredis

from core import settings
from pubsub import RedisReader
from services.handler import Handler
from services.parser import Bs4Parser
from services.session import CustomClientSession


async def main():
    redis = aioredis.from_url(settings.REDIS['url'])
    handler = Handler(session=CustomClientSession, parser=Bs4Parser)
    redis_reader = RedisReader(redis, handler)
    pubsub = redis.pubsub()
    await pubsub.subscribe('parser')
    future = asyncio.create_task(redis_reader.reader(pubsub))
    await future

if __name__ == '__main__':
    asyncio.run(main())
