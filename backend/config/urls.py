from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve

from config.swagger import SCHEMA_VIEW

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            SCHEMA_VIEW.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', SCHEMA_VIEW.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$', SCHEMA_VIEW.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns.append(re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}))
    urlpatterns.append(re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}))

