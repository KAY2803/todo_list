from django.contrib.auth.models import User
from django.test import TestCase

from todo import filters
from todo.models import ToDoList, Comment


class TestFilters(TestCase):
    """Класс тестирования фильтров"""

    @classmethod
    def setUpTestData(cls):
        """Классовый метод создания тестовой базы"""
        test_user_1 = User(username="test_user_1", password="fake_password1",)
        test_user_2 = User(username="test_user_2", password="fake_password2",)
        test_user_1, test_user_2 = User.objects.bulk_create([test_user_1, test_user_2])

        note_1 = ToDoList(note="note_1", author=test_user_1, status=1, importance=True, public=True)
        note_2 = ToDoList(note="note_2", author=test_user_1, status=2, importance=False, public=False)
        note_3 = ToDoList(note="note_3", author=test_user_2, status=3, importance=True, public=False)
        note_4 = ToDoList(note="note_4", author=test_user_2, status=1, importance=False, public=True)
        note_1, note_2, note_3, note_4 = ToDoList.objects.bulk_create([note_1, note_2, note_3, note_4])

        comment_1 = Comment(comment='comment_1', note=note_1, author=test_user_1)
        comment_2 = Comment(comment='comment_2', note=note_4, author=test_user_2)
        comment_1, comment_2 = Comment.objects.bulk_create([comment_1, comment_2])

    def test_NoteFilter_values(self):
        """Тест фильтра по статусу, важности и публичности заметки"""
        queryset = ToDoList.objects.all()
        GET = {'public': False}
        f = filters.NoteFilter(GET, queryset)
        self.assertEqual(len(f.qs), 2)

        exp = [2, 3]
        act = []
        for i in f.qs:
            act.append(i.status)
        self.assertTrue(act[0] in exp, act[1] in exp)

        GET = {'importance': False}
        f = filters.NoteFilter(GET, queryset)
        self.assertEqual(len(f.qs), 2)

        exp = [2, 4]
        act = []
        for i in f.qs:
            act.append(i.status)
        self.assertTrue(act[0] in exp, act[1] in exp)

        GET = {'status': 1}
        f = filters.NoteFilter(GET, queryset)
        self.assertEqual(len(f.qs), 2)

        exp = [1, 4]
        act = []
        for i in f.qs:
            act.append(i.id)
        self.assertTrue(act[0] in exp, act[1] in exp)
