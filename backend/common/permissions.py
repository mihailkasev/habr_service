from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Permission с доступом пользователей с правами superuser к добавлению, изменению, удалению"""
    @staticmethod
    def common_permission(request):
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
        if request.user.is_superuser:
            return True
        return False

    def has_permission(self, request, view):
        return self.common_permission(request)

    def has_object_permission(self, request, view, obj):
        return self.common_permission(request)
