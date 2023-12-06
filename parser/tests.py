import asyncio
import json
import unittest
from typing import Any

from services.handler import Handler
from services.parser import Bs4Parser
from services.session import CustomClientSession


class TestParser(unittest.TestCase):
    html_path = 'fixtures/article.html'
    json_path = 'fixtures/article.json'
    article_html: str
    article_data: Any

    def setUp(self):
        self.parser = Bs4Parser()
        with open(self.html_path, "r", encoding='utf-8') as file:
            self.article_html = file.read()
        with open(self.json_path, 'r', encoding='utf-8') as file:
            data = file.read()
            self.article_data = json.loads(data)

    def test_parse_article(self):
        self.assertEqual(self.parser.parse_article(self.article_html), self.article_data, 'Проверьте, что метод parse_article класса Parser возвращает корректное значение')


class TestHandler(unittest.IsolatedAsyncioTestCase):
    hub_link = 'https://habr.com/ru/hubs/programming/articles/'

    @classmethod
    def setUpClass(cls) -> None:
        cls._loop = asyncio.new_event_loop()

    def setUp(self):
        self.handler = Handler(parser=Bs4Parser, session=CustomClientSession)

    def test_parse_articles(self):
        results = self._loop.run_until_complete(self.handler.parse_articles(self.hub_link))
        self.assertIsNotNone(results, 'Проверьте, что метод parse_articles класса Handler не возвращает None')
        self.assertEqual(type(results.get('hub')), str, 'Проверьте, что метод parse_articles класса Handler возвращает в ключе hub корректное значение')
        self.assertEqual(type(results.get('articles')), dict, 'Проверьте, что метод parse_articles класса Handler возвращает в ключе articles корректное значение')

    def tearDown(self) -> None:
        self._loop.close()


if __name__ == '__main__':
    unittest.main()
