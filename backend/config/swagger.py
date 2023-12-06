import rest_framework.authentication
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

SCHEMA_VIEW = get_schema_view(
    openapi.Info(
        title='API парсер сервиса портала Хабр',
        default_version='v1',
        description='Динамическое API',
    ),
    public=True,
    permission_classes=[permissions.IsAdminUser],
    authentication_classes=[rest_framework.authentication.SessionAuthentication]
)
