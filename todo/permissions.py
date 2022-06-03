from rest_framework import permissions


class GetPublicNote(permissions.BasePermission):
    """Класс для установки разрешения на доступ к публичным заметкам"""
    def has_object_permission(self, request, view, obj):
        if obj.author_id != request.user.id:
            return obj.public is True
        return True
