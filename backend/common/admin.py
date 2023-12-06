from django.contrib import admin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.safestring import mark_safe
from django_celery_beat.models import ClockedSchedule, CrontabSchedule, IntervalSchedule, PeriodicTask, SolarSchedule
from .tasks import clear_cache


class BaseAdmin(admin.ModelAdmin):
    """Базовый класс администрирования моделей"""
    readonly_fields = ['id']
    change_list_template = 'admin/cache_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [path('cache-clear/', self.clear_cache, name="cache_clear"), ] + urls
        return custom_urls

    def clear_cache(self, request):
        clear_cache.delay(self.model.__name__)
        return HttpResponseRedirect("../")

    @admin.display(empty_value="???", description='ссылка')
    def url_link(self, obj):
        link = f'<a href={obj.link}>{obj.link}</a>'
        return mark_safe(link)


admin.site.site_header = 'Хабр'
admin.site.site_title = 'Администрирование парсера Хабр'
admin.site.index_title = 'Добро пожаловать на административную панель парсер сервиса портала Хабр'
admin.site.unregister(Group)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
