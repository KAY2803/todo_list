from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class UpdateDelNote(permissions.BasePermission):
    """Класс для установки разрешения на изменение и удаление только своих заметок"""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if obj.author_id != request.user.id:
                return obj.public
            return True
        else:
            return obj.author_id == request.user.id
