from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from django.conf import settings


class Command(BaseCommand):
    help = "Создает суперпользователя, если такого нет."
    User = get_user_model()

    def handle(self, *args, **options):
        if self.User.objects.filter(is_superuser=True).exists():
            print('Суперпользователь уже существует.')
            return
        self.User.objects.create_superuser(
            username=settings.ADMIN['username'],
            email=settings.ADMIN['email'],
            password=settings.ADMIN['password']
        )
        print('Создан суперпользователь.')
