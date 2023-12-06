from typing import Dict, List

from bs4 import BeautifulSoup, Tag
from utils import create_link


class Bs4Parser:
    handler = BeautifulSoup

    @classmethod
    def parse_hub(cls, html: str) -> List[Tag]:
        return cls.handler(html, 'html.parser').find_all('a', class_='tm-title__link', href=True)

    @classmethod
    def parse_article(cls, html: str) -> Dict[str, str]:
        article_data = dict()
        soup = cls.handler(html, 'html.parser')
        article_data['title'] = soup.find('h1', class_='tm-title tm-title_h1').next.text
        author = soup.find('a', class_='tm-user-info__username')
        article_data['username'] = author.text.strip()
        article_data['author_link'] = create_link(author.get('href'))
        article_data['published_at'] = soup.find('span', class_='tm-article-datetime-published').next.get('datetime')
        article_data['body'] = str(soup.find('div', class_='tm-article-body'))
        return article_data
