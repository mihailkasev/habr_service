from typing import Protocol


class Parser(Protocol):
    @classmethod
    def parse_hub(cls, html: str):
        """Парсит данные с главной страницы хаба"""

    @classmethod
    def parse_article(cls, html: str):
        """Парсит данные со страницы статьи"""
