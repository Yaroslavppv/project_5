from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    """Проверка: входит ли пользователь в группу модераторов"""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.groups.filter(name='Moderators').exists()
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.groups.filter(name='Moderators').exists()
        return False


class IsOwner(BasePermission):
    """Проверка: является ли пользователь владельцем объекта"""
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
