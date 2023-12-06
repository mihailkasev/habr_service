from django.contrib.auth.models import AbstractUser

from common.models import Base


class User(Base, AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
