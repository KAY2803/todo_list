from rest_framework import serializers

from todo.models import ToDoList


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = '__all__'
        read_only_fields = ('author',)