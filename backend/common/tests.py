from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import path, include, reverse
from rest_framework import status
from rest_framework.test import APITestCase

from common.models import Base

User = get_user_model()


class BaseAPITestCase(APITestCase):
    """Базовый APITestCase для тестирования api проекта"""
    fixtures = ['test_data.json']
    DATA: dict
    urlpatterns = [
        path('api/', include('api.urls')),
    ]
    url_pattern: str
    model: Base
    lookup_field: str

    @classmethod
    def setUpTestData(cls):
        """Подготавливает данные"""
        cls.user_from_fixtures = User.objects.first()

    def _jwt_auth(self, user):
        """Получает JWT токен и добавляет его в хэдер"""
        auth = self.client.post(
            '/api/auth/jwt/create/',
            {'username': user.username, 'password': settings.ADMIN['password']},
            format='json'
        )
        token = auth.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))

    def auth(self):
        """Проходит полную аутентификацию"""
        user = self.user_from_fixtures
        self._jwt_auth(user=user)

    def _base_test_create_api(self):
        """"""
        self.auth()
        response = self.client.post(reverse(f'{self.url_pattern}-list'), data=self.DATA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         f'Проверьте, что POST запрос на /api/{self.url_pattern}/ возвращает корректный status code')
        params = {self.lookup_field: self.DATA[self.lookup_field]}
        instance = self.model.objects.get(**params)
        self.assertTrue(instance, f'Проверьте, что POST запрос на /api/{self.url_pattern}/ создает необходимый объект')


class HubsAppAPITestCase(BaseAPITestCase):
    """APITestCase для тестирования api приложения hubs"""
    lookup_field = 'link'

    def _base_test_list_api(self):
        self.auth()
        response = self.client.get(reverse(f'{self.url_pattern}-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Проверьте, что `/api/{self.url_pattern}/` возвращает статус 200')
        response_result = response.json().get('results')
        self.assertEqual(type(response_result), list, f'Проверьте, что `/api/{self.url_pattern}/` возвращает статус 200')

    def _base_test_get_api(self):
        self.auth()
        instance = self.model.objects.first()
        response = self.client.get(reverse(f'{self.url_pattern}-detail', args=(instance.id, )))
        self.assertEqual(response.json().get('id'), str(instance.id), f'Проверьте, что `/api/{self.url_pattern}/` возвращает корректные данные')

    def _base_test_put_api(self, method: str = 'detail'):
        self.auth()
        instance = self.model.objects.values('id', self.lookup_field).first()
        response = self.client.put(reverse(f'{self.url_pattern}-detail', args=(instance.get('id'), )), data=self.DATA)
        response_instance = response.json()
        self.assertNotEqual(response_instance.get(self.lookup_field), instance.get(self.lookup_field),
                            f'Проверьте, что PUT запрос на /api/{self.url_pattern}/ обновляет объект')

    def _base_test_patch_api(self):
        self.auth()
        instance = self.model.objects.values('id', self.lookup_field).first()
        data = {self.lookup_field: self.DATA[self.lookup_field]}
        response = self.client.patch(reverse(f'{self.url_pattern}-detail', args=(instance.get('id'),)), data=data)
        response_hub = response.json()
        self.assertNotEqual(response_hub.get(self.lookup_field), instance.get(self.lookup_field),
                            f'Проверьте, что PATCH запрос на /api/{self.url_pattern}/ обновляет поле объекта')

    def _base_test_delete_api(self):
        self.auth()
        instance = self.model.objects.values('id', self.lookup_field).first()
        response = self.client.delete(reverse(f'{self.url_pattern}-detail', args=(instance.get('id'),)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                         f'Проверьте, что DELETE запрос на /api/{self.url_pattern}/<id>/ возвращает корректный status code')
        params = {self.lookup_field: instance.get(self.lookup_field)}
        deleted_instance = self.model.objects.filter(**params).exists()
        self.assertFalse(deleted_instance, f'Проверьте, что DELETE запрос на /api/{self.url_pattern}/<id>/ удаляет объект из базы данных')
