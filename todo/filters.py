from django_filters import rest_framework as filters
from django_filters import MultipleChoiceFilter

from todo.models import ToDoList


class NoteFilter(filters.FilterSet):
    """Класс для фильтрации заметок"""

    class Meta:
        model = ToDoList
        fields = ['status', 'importance', 'public']

    class multi_filter(filters.FilterSet):
        tags = MultipleChoiceFilter(field_name=['status', 'importance', 'public'], queryset = ToDoList.objects.all())