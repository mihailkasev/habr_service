from django.db.models import Exists, OuterRef, Value
from django_filters.rest_framework import FilterSet, filters

from hubs.models import Hub, Favorite


class HubFilter(FilterSet):
    """Фильтр для хабов"""
    is_favorite = filters.BooleanFilter(method='filter_is_favorite', label='только избранные хабы')

    def filter_is_favorite(self, queryset, name, value):

        user = self.request.user
        if value is True:
            qs = queryset.annotate(
                is_favorite=Exists(
                    Favorite.objects.filter(user=user, hub=OuterRef('pk'))
                )).filter(is_favorite=Value(True))
            return qs
        return queryset

    class Meta:
        fields = ()
        model = Hub
