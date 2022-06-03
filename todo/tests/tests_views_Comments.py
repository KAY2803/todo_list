from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from todo.models import ToDoList, Comment


URL = '/api/v1/comments/'


class TestCommentViews(APITestCase):
    """Класс тестирования представлений для модели Comment"""

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

        """ тест на получение списка комментариев"""
    def test_get_CommentListCreateAPIView(self):
        user = User.objects.get(username='test_user_1')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(URL)
        queryset = Comment.objects.all()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(queryset.count(), len(response.data))

    """ тест на создание комментария к заметке в списке дел"""
    def test_post_CommentListCreateAPIView(self):
        user = User.objects.get(username='test_user_1')
        note = ToDoList.objects.filter(pk=4).values_list('id', flat=True)
        client = APIClient()
        client.force_authenticate(user=user)
        data = {'comment': 'new comment to note', 'note': note}
        response = client.post(URL, data)
        queryset = Comment.objects.all()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(queryset.count(), 3)

    """ тест на проверку создания комментария к непубличной заметке"""
    def test_post_nonpublic_note_CommentListCreateAPIView(self):
        user = User.objects.get(username='test_user_1')
        note = ToDoList.objects.filter(pk=3).values_list('id', flat=True)
        client = APIClient()
        client.force_authenticate(user=user)
        data = {'comment': 'new comment to note', 'note': note}
        client.post(URL, data)
        queryset = Comment.objects.all()
        self.assertEqual(queryset.count(), 2)