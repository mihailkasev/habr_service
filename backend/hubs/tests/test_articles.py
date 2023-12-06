from django.utils import timezone

from common.tests import HubsAppAPITestCase
from hubs.services import create_articles
from hubs.models import Hub, Article, Author


class ArticleTestCase(HubsAppAPITestCase):
    """APITestCase для тестирования api статей"""
    model = Article
    url_pattern = 'articles'

    DATA = {
        'articles': {
            'Тестовый заголовок': {
                'link': 'https://habr.com/articles/1/',
                'published_at': timezone.now(),
                'username': 'test_author',
                'author_link': 'https://habr.com/users/test_author/',
                'body': 'html test'
            },
            'Тестовый заголовок 2': {
                'link': 'https://habr.com/articles/2/',
                'published_at': timezone.now(),
                'username': 'test_author2',
                'author_link': 'https://habr.com/users/test_author2/',
                'body': 'html test2'
            }
        }
    }

    def test_get_articles(self):
        """Тест GET запроса статей"""
        self._base_test_list_api()

    def test_get_article(self):
        """Тест GET запроса статьи"""
        self._base_test_get_api()

    def test_create_articles(self):
        """Тест создания статей с их авторами"""
        hub = Hub.objects.first()
        data = {
            'hub': hub.link
        }
        data.update(self.DATA)
        create_articles(data)
        articles = data['articles']
        new_articles = self.model.objects.filter(link__in=(articles['Тестовый заголовок']['link'], articles['Тестовый заголовок 2']['link'])).all()
        message = 'Проверьте, что create_articles создает статьи и авторов'
        self.assertTrue(list(new_articles), message)
        new_authors = Author.objects.filter(link__in=(articles['Тестовый заголовок']['author_link'], articles['Тестовый заголовок']['author_link'])).all()
        self.assertTrue(list(new_authors), message)
