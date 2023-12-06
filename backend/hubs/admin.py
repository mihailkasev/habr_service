from common.admin import admin
from common.admin import BaseAdmin
from .models import Hub, Author, Article


@admin.register(Hub)
class HubAdmin(BaseAdmin):
    list_display = ['name', 'url_link']


@admin.register(Author)
class AuthorAdmin(BaseAdmin):
    list_display = ['username', 'url_link']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Article)
class ArticleAdmin(BaseAdmin):
    list_display = ['title', 'author', 'hub', 'url_link']
    list_filter = ['hub', 'author']
    fields = ('link', 'published_at', 'author', 'hub')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
