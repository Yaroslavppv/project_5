from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    """
    Проверяет, входит ли текущий пользователь в группу 'Moderators'.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.groups.filter(name='Moderators').exists()
        return False


class IsOwner(BasePermission):
    """
    Проверяет, является ли пользователь владельцем конкретного объекта.
    """
    def has_object_permission(self, request, obj):
        return obj.owner == request.user

