from common.tests import HubsAppAPITestCase
from hubs.models import Author


class AuthorTestCase(HubsAppAPITestCase):
    """APITestCase для тестирования api авторов"""
    url_pattern = 'authors'
    model = Author

    def test_get_authors(self):
        """Тест GET запроса статей"""
        self._base_test_list_api()

    def test_get_article(self):
        """Тест GET запроса статьи"""
        self._base_test_get_api()
