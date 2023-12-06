from django.urls import include, path, re_path
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

from hubs.views import HubViewSet, ArticleViewSet, AuthorViewSet

router = DefaultRouter()
router.register('hubs', HubViewSet, 'hubs')
router.register('authors', AuthorViewSet, 'authors')
router.register('articles', ArticleViewSet, 'articles')

user_router = DefaultRouter()
user_router.register(r"auth/users", UserViewSet, basename="users")


def is_route_selected(url_pattern):
    excluded_urls = [
        "auth/users/activation/",
        "auth/users/resend_activation/",
        "auth/users/set_username/",
        "auth/users/reset_username/",
        "auth/users/reset_username_confirm/",
    ]

    for u in excluded_urls:
        match = url_pattern.resolve(u)
        if match:
            return False
    return True


selected_user_routes = list(filter(is_route_selected, user_router.urls))

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.jwt')),
] + selected_user_routes
