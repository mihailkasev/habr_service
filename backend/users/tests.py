from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse, path, include
from rest_framework import status

from common.tests import BaseAPITestCase


class UserTestCase(BaseAPITestCase):
    model = get_user_model()
    urlpatterns = [
        path('api/auth/', include('api.urls')),
    ]
    url_pattern = 'users'
    lookup_field = 'email'
    DATA = {'username': 'testuser', 'email': 'test@gmail.com', 'password': 'newpass1API'}

    def test_get_users(self):
        """Тест GET запроса пользователей"""
        self.auth()
        response = self.client.get(reverse(f'{self.url_pattern}-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Проверьте, что `/api/auth/{self.url_pattern}/` возвращает статус 200')
        response_result = response.json()
        self.assertEqual(type(response_result), list,
                         f'Проверьте, что `/api/auth/{self.url_pattern}/` возвращает статус 200')

    def test_get_current_user(self):
        """Тест GET запроса текущего пользователя"""
        self.auth()
        response = self.client.get(reverse(f'{self.url_pattern}-me'))
        self.assertEqual(response.json().get('id'), str(self.user_from_fixtures.id), f'Проверьте, что GET запрос на /api/auth/{self.url_pattern}/me/ возвращает текущего пользователя')

    def test_create_user(self):
        """Тест создания пользователя"""
        self._base_test_create_api()

    def test_put_user(self):
        """Тест обновления текущего пользователя"""
        self.auth()
        response = self.client.put(reverse(f'{self.url_pattern}-me'), data=self.DATA)
        response_user = response.json()
        self.assertNotEqual(response_user.get(self.lookup_field), self.user_from_fixtures.email,
                            f'Проверьте, что PUT запрос на /api/auth/{self.url_pattern}/me/ обновляет объект')

    def test_patch_user(self):
        """Тест частичного обновления текущего пользователя"""
        self.auth()
        data = {self.lookup_field: self.DATA[self.lookup_field]}
        response = self.client.patch(reverse(f'{self.url_pattern}-me'), data=data)
        response_user = response.json()
        self.assertNotEqual(response_user.get(self.lookup_field), self.user_from_fixtures.username,
                            f'Проверьте, что PUT запрос на /api/auth/{self.url_pattern}/me/ обновляет объект')

    def test_delete_user(self):
        """Тест удаления текущего пользователя"""
        self.auth()
        response = self.client.delete(reverse(f'{self.url_pattern}-me'), data={'current_password': settings.ADMIN['password']})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                         f'Проверьте, что DELETE запрос на /api/auth/{self.url_pattern}/me/ возвращает корректный status code')
        params = {self.lookup_field: self.user_from_fixtures.username}
        deleted_instance = self.model.objects.filter(**params).exists()
        self.assertFalse(deleted_instance,
                         f'Проверьте, что DELETE запрос на /api/auth/{self.url_pattern}/me/ удаляет объект из базы данных')
