import uuid

from django.db import models
from django.db.models import Manager


class Base(models.Model):
    """Базовая модель"""
    id = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4, unique=True, verbose_name='id')
    objects: Manager

    class Meta:
        abstract = True


class LinkedMixin(Base):
    """Mixin с ссылкой"""
    link = models.URLField(unique=True, verbose_name='ссылка')

    class Meta:
        abstract = True


class TimeStampedMixin(Base):
    """Mixin с временными отметками"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата обновления')

    class Meta:
        abstract = True


class LinkedTimedModel(LinkedMixin, TimeStampedMixin):
    """Модель с ссылкой и временными отметками"""
    class Meta:
        abstract = True
        ordering = ('-created_at', )
