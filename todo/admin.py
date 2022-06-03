from django.contrib import admin
from todo.models import ToDoList


@admin.register(ToDoList)
class ToDoListAdmin(admin.ModelAdmin):
    list_filter = ('status', 'importance', 'public',)


