from rest_framework import serializers

from todo.models import ToDoList, Comment


class NoteSerializer(serializers.ModelSerializer):
    """Класс для сериализации заметок"""

    class Meta:
        model = ToDoList
        fields = '__all__'
        read_only_fields = ('author',)


class CommentSerializer(serializers.ModelSerializer):
    """Класс для сериализации комментариев"""

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author',)

    def validate_note(self, value):
        """Проверка валидности заметка на предмет ее публичности для создания комментария"""
        q = ToDoList.objects.filter(public=True).values_list('id', flat=True)
        if value.id not in q:
            raise serializers.ValidationError("Недостаточно прав для добавления комментария")
        return value