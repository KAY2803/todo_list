import datetime

from django.contrib.auth.models import User
from django.db import models


class ToDoList(models.Model):
    """Класс модели ToDoList"""

    class Meta:
        """Сортировка заметок по умолчанию по дате создания и важности"""
        ordering = ['note_date__date', '-importance']

    class NoteStatus(models.IntegerChoices):
        ACTIVE = 1, 'Активно'
        DELAY = 2, 'Отложено'
        DONE = 3, 'Выполнено'

    note = models.CharField(max_length=100, null=False, verbose_name='Заметка')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    status = models.IntegerField(choices=NoteStatus.choices, default=1, verbose_name='Статус')
    importance = models.BooleanField(default=False, verbose_name='Важно')
    public = models.BooleanField(default=False, verbose_name='Публичная')
    note_date = models.DateTimeField(default=(datetime.datetime.now() + datetime.timedelta(days=1)),
                                     verbose_name='Дата и время'
                                     )


class Comment(models.Model):
    """Класс модели Comment"""
    comment = models.CharField(max_length=50, null=False, verbose_name='Комментарий')
    note = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


