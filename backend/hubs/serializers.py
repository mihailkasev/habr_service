from uuid import uuid4

from djoser.serializers import UserSerializer
from rest_framework.serializers import ModelSerializer, UUIDField

from hubs.models import Author, Hub, Article, Favorite


class ShortArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'link', 'published_at')


class AuthorSerializer(ModelSerializer):
    articles = ShortArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('id', 'username', 'link', 'articles')


class ShortAuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'username', 'link')


class HubSerializer(ModelSerializer):
    id = UUIDField(read_only=True, default=uuid4)
    articles = ShortArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Hub
        fields = ('id', 'name', 'link', 'parse_period', 'articles')


class ShortHubSerializer(ModelSerializer):
    class Meta:
        model = Hub
        fields = ('id', 'name', 'link', 'parse_period')


class ArticleSerializer(ModelSerializer):
    hub = ShortHubSerializer(read_only=True)
    author = ShortAuthorSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'link', 'hub', 'author', 'published_at', 'body')


class FavoriteSerializer(ModelSerializer):
    hub = ShortHubSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ('hub', 'user')
