from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.permissions import AdminOrReadOnly
from common.views import CachedModelViewSet, CachedListRetrieveViewSet
from hubs.filters import HubFilter
from hubs.models import Hub, Author, Article, Favorite
from hubs.serializers import HubSerializer, FavoriteSerializer, AuthorSerializer, ArticleSerializer


class HubViewSet(CachedModelViewSet):
    """ViewSet для представления Хаба"""
    queryset = Hub.objects.prefetch_related('articles').all()
    serializer_class = HubSerializer
    permission_classes = [AdminOrReadOnly]
    filterset_class = HubFilter

    @action(methods=['POST', 'DELETE'], detail=True, description='Добавить в избранное', permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        if request.method != 'POST':
            favorite = get_object_or_404(
                Favorite,
                user=request.user,
                hub=get_object_or_404(Hub, pk=pk)
            )
            self.perform_destroy(favorite)
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = FavoriteSerializer(
            data={
                'user': request.user.id,
                'hub': get_object_or_404(Hub, pk=pk).id
            },
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AuthorViewSet(CachedListRetrieveViewSet):
    """ViewSet для представления Автора"""
    queryset = Author.objects.prefetch_related('articles').all()
    serializer_class = AuthorSerializer


class ArticleViewSet(CachedListRetrieveViewSet):
    """ViewSet для представления Статьи"""
    queryset = Article.objects.select_related('author', 'hub').order_by('-published_at').all()
    serializer_class = ArticleSerializer
