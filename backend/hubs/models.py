from common.models import *


class Hub(LinkedTimedModel):
    """Модель хаба"""
    name = models.CharField(max_length=255, unique=True, db_index=True, verbose_name='название')
    parse_period = models.PositiveSmallIntegerField(verbose_name='периодичность запроса хаба в мин.')

    class Meta(LinkedTimedModel.Meta):
        verbose_name = 'Хаб'
        verbose_name_plural = 'Хабы'

    def __str__(self):
        return f'{self.name}'


class Author(LinkedTimedModel):
    """Модель автора"""
    username = models.CharField(max_length=150, unique=True, verbose_name='никнейм')

    class Meta(LinkedTimedModel.Meta):
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return f'{self.username}'


class Article(LinkedMixin, Base):
    """Модель статьи"""
    title = models.CharField(db_index=True, max_length=255, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержание статьи')
    published_at = models.DateTimeField(verbose_name='дата публикации статьи')
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='автор'
    )
    hub = models.ForeignKey(
        Hub,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='хаб'
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Favorite(TimeStampedMixin, Base):
    """Модель избранного хаба"""
    hub = models.ForeignKey(
        Hub,
        related_name='favorite',
        on_delete=models.CASCADE,
        verbose_name='избранный хаб'
    )
    user = models.ForeignKey(
        'users.User',
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )
