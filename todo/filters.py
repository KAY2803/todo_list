from django_filters import rest_framework as filters

from todo.models import ToDoList


class NoteFilter(filters.FilterSet):
    """Класс для фильтрации заметок"""

    class Meta:
        model = ToDoList
        fields = ['status', 'importance', 'public']
