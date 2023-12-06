import asyncio
from typing import Type, Dict

from aiohttp import ClientSession, ClientTimeout

from core.parser import Parser
from core.settings import CONNECTION_PARAMS
from utils import create_link


class Handler:
    def __init__(self, session: Type[ClientSession], parser: Type[Parser]):
        self.session = session
        self.parser = parser

    async def parse_articles(self, hub_link: str) -> Dict[str, str | Dict[str, str]]:
        """
        Парсит данные с указанного хаба
        :param hub_link Адрес хаба
        :return Словарь с адресом хаба и собранными статьями
        """
        data = {'hub': hub_link, 'articles': dict()}
        async with self.session(timeout=ClientTimeout(**CONNECTION_PARAMS)) as session:
            async with session.get(hub_link) as response:
                html = await response.text()
            tasks = []
            for article in self.parser.parse_hub(html):
                link = create_link(article.get('href'))
                title = article.text
                data['articles'].update({title: {'link': link}})
                request = session.get(link)
                tasks.append(asyncio.create_task(request))
            responses = await asyncio.gather(*tasks)
            htmls = [await r.text() for r in responses]
            for html in htmls:
                article_data = self.parser.parse_article(html)
                data['articles'][article_data['title']].update(article_data)
        return data

