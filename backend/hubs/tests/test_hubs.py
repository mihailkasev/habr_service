from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from common.tests import HubsAppAPITestCase
from hubs.models import Hub, Favorite

client = APIClient()
User = get_user_model()


class HubsTestCase(HubsAppAPITestCase):
    model = Hub
    url_pattern = 'hubs'
    DATA = {'name': 'Карьера в IT-индустрии', 'link': 'https://habr.com/ru/hubs/career/articles/', 'parse_period': 4}

    def test_get_hubs(self):
        """Тест GET запроса хабов"""
        self._base_test_list_api()

    def test_get_hub(self):
        """Тест GET запроса хаба"""
        self._base_test_get_api()

    def test_create_hub(self):
        """Тест создания хаба"""
        self._base_test_create_api()

    def test_put_hub(self):
        """Тест обновления хаба"""
        self._base_test_put_api()

    def test_patch_hub(self):
        """Тест частичного обновления хаба"""
        self._base_test_patch_api()

    def test_delete_hub(self):
        """Тест удаления хаба"""
        self._base_test_delete_api()

    def test_favorite_hub(self):
        """Тест добавления хаба в избранные"""
        self.auth()
        hub = Hub.objects.first()
        response = self.client.post(reverse(f'{self.url_pattern}-favorite', args=(hub.id, )))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Проверьте, что POST запрос на /api/hubs/{id}/favorite/ добавляет хаб в избранное')
        favorite_hub = Favorite.objects.get(user=self.user_from_fixtures, hub=hub)
        self.assertIsNotNone(favorite_hub, 'Проверьте, что хаб находится в избранный у пользователя')

    def test_remove_favorite_hub(self):
        """Тест удаления хаба из избранных"""
        self.auth()
        hub = self.model.objects.values('id', self.lookup_field).first()
        Favorite.objects.create(user=self.user_from_fixtures, hub=hub)
        response = self.client.delete(reverse(f'{self.url_pattern}-favorite', args=(hub.id, )))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, f'Проверьте, что DELETE запрос на /api/{self.url_pattern}/<id>/favorite/ возвращает корректный status code')
        params = {self.lookup_field: hub.get(self.lookup_field)}
        deleted_instance = self.model.objects.filter(**params).exists()
        self.assertFalse(deleted_instance,
                         f'Проверьте, что DELETE запрос на /api/{self.url_pattern}/<id>/favorite/ удаляет хаб из избранных')
