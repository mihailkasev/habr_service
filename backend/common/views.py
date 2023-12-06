from rest_framework import status, mixins
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common.pagination import CustomPagination
from services.cache import cache_service


class CachedListModelMixin(ListModelMixin):
    """Mixin только для GET запроса списка экземпляров модели с кэшированием"""
    def list(self, request, *args, **kwargs):
        model_name = self.get_model_name()
        cache_key = self.cache_service.make_cache_key(model_name, request.query_params)
        try:
            data = self.cache_service.cache.get(cache_key)
            if data:
                return Response(data, status=status.HTTP_200_OK)
            response = super().list(request, *args, **kwargs)
            self.cache_service.cache.set(cache_key, response.data)
            return response
        except ConnectionError:
            super().list(request, *args, **kwargs)


class CachedRetrieveModelMixin(RetrieveModelMixin):
    """Mixin только для GET запроса экземпляра модели с кэшированием"""
    def retrieve(self, request, *args, **kwargs):
        model_name = self.get_model_name()
        cache_key = self.cache_service.make_cache_key(model_name, request.query_params, kwargs[self.lookup_field])
        try:
            data = self.cache_service.cache.get(cache_key)
            if data:
                return Response(data, status=status.HTTP_200_OK)
            instance = self.get_object()
            serializer = self.serializer_class(instance, context=self.get_serializer_context())
            self.cache_service.cache.set(cache_key, serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ConnectionError:
            instance = self.get_object()
            serializer = self.serializer_class(instance, context=self.get_serializer_context())
            return Response(serializer.data, status=status.HTTP_200_OK)


class CachedGenericViewSet(GenericViewSet):
    """GenericViewset с кэшированием"""
    cache_service = cache_service
    pagination_class = CustomPagination

    def get_model_name(self) -> str:
        model_name = self.queryset.model.__name__
        return model_name


class CachedListRetrieveViewSet(CachedListModelMixin, CachedRetrieveModelMixin, CachedGenericViewSet):
    """Вьюсет, предоставляющий только GET запросы с кэшированием"""
    pass


class CachedModelViewSet(mixins.CreateModelMixin,
                         CachedRetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         CachedListModelMixin,
                         CachedGenericViewSet):
    """Вьюсет, предоставляющий CRUD для модели с кэшированием GET запросов"""
    pass
