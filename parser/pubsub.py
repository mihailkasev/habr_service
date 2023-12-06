import asyncio
import json
from redis.asyncio.client import Redis, PubSub

from services.handler import Handler


class RedisReader:
    def __init__(self, client: Redis, handler: Handler):
        self.client = client
        self.handler = handler

    async def reader(self, channel: PubSub) -> None:
        """Прослушивает и обрабатывает сообщения из канала Redis"""
        while True:
            message = await channel.get_message(ignore_subscribe_messages=True)
            if message:
                message_data: bytes = message.get('data')
                data = await self.handler.parse_articles(message_data.decode('utf-8'))
                raw_data = json.dumps(data, ensure_ascii=False)
                await self.client.publish('backend', raw_data)
            await asyncio.sleep(0.01)
