from django.db import transaction
from django.db.utils import IntegrityError
from hubs.models import Hub, Author, Article


def create_articles(data: dict) -> None:
    """Сохраняет в базу данных статьи и их авторов.
    :param data Спарсенные данные
    """
    hub_link = data.pop('hub')
    hub = Hub.objects.get(link=hub_link)
    for title, article in data['articles'].items():
        with transaction.atomic():
            #  во избежание создания дубликатов
            try:
                author, _ = Author.objects.get_or_create(
                    username=article.get('username'),
                    link=article.get('author_link')
                )
                Article.objects.get_or_create(
                    title=title,
                    link=article.get('link'),
                    body=article.get('body'),
                    hub=hub,
                    author=author,
                    published_at=article.get('published_at')
                )
            except IntegrityError:
                pass
